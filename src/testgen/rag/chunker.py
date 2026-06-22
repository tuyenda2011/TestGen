from __future__ import annotations

import ast
from dataclasses import dataclass

from testgen.analyzer.tree_sitter_adapter import parse_source_structure


@dataclass(frozen=True)
class StructuredChunk:
    text: str
    metadata: dict[str, object]


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    if not text or not text.strip():
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    chunks: list[str] = []
    start = 0
    text_length = len(text)
    
    separators = ["\n\n", "\n", ". ", " "]

    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        if end >= text_length:
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            break
            
        best_split = -1
        for sep in separators:
            sep_idx = text.rfind(sep, start, end)
            if sep_idx != -1 and sep_idx > start + int(chunk_size * 0.5):
                best_split = sep_idx + len(sep)
                break
                
        if best_split != -1:
            end = best_split
            
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        next_start = end - chunk_overlap
        if next_start <= start:
            next_start = start + 1
            
        if next_start > 0 and next_start < text_length:
            if text[next_start - 1] not in [" ", "\n"]:
                snap_idx = -1
                for sep in ["\n", " "]:
                    idx = text.find(sep, next_start)
                    if idx != -1 and idx < end:
                        snap_idx = idx + len(sep)
                        break
                if snap_idx != -1:
                    next_start = snap_idx

        start = next_start

    return chunks


def chunk_text_with_metadata(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    *,
    source_name: str = "",
    chunk_type: str = "text",
    section: str = "",
) -> list[StructuredChunk]:
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    if not chunks:
        return []

    records: list[StructuredChunk] = []
    cursor = 0
    for index, chunk in enumerate(chunks):
        start = text.find(chunk, cursor)
        if start < 0:
            start = cursor
        end = min(start + len(chunk), len(text))
        line_start = text.count("\n", 0, start) + 1
        line_end = text.count("\n", 0, end) + 1
        records.append(
            StructuredChunk(
                text=chunk,
                metadata={
                    "source_name": source_name,
                    "section": section or source_name,
                    "chunk_type": chunk_type,
                    "chunk_index": index,
                    "line_start": line_start,
                    "line_end": line_end,
                },
            )
        )
        cursor = max(end - chunk_overlap, end)
    return records


def _python_syntax_error_message(exc: SyntaxError, source_name: str = "") -> str:
    location = []
    if source_name:
        location.append(source_name)
    if exc.lineno:
        location.append(f"line {exc.lineno}")
    if exc.offset:
        location.append(f"column {exc.offset}")
    where = f" ({', '.join(location)})" if location else ""
    return f"SyntaxError{where}: {exc.msg}"


def chunk_python_source(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    *,
    source_name: str = "",
) -> list[StructuredChunk]:
    if not text or not text.strip():
        return []

    parsed = parse_source_structure(text, "python", source_name=source_name)
    if parsed.parser_available:
        return chunk_structured_source(
            text,
            chunk_size,
            chunk_overlap,
            source_name=source_name,
            language="python",
        )

    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        diagnostic = _python_syntax_error_message(exc, source_name)
        return chunk_text_with_metadata(
            f"[AST SyntaxError]\n{diagnostic}\n\n{text}",
            chunk_size,
            chunk_overlap,
            source_name=source_name,
            chunk_type="python_syntax_error",
            section="syntax_error",
        )

    lines = text.splitlines()
    records: list[StructuredChunk] = []

    def _traverse(node, current_path=""):
        extracted = []
        for child in getattr(node, "body", []):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = f"{current_path}.{child.name}" if current_path else child.name
                extracted.append((child, name, "python_function"))
                extracted.extend(_traverse(child, name))
            elif isinstance(child, ast.ClassDef):
                name = f"{current_path}.{child.name}" if current_path else child.name
                extracted.append((child, name, "python_class"))
                extracted.extend(_traverse(child, name))
        return extracted

    nodes_info = _traverse(tree)
    
    for index, (node, section_name, node_type) in enumerate(nodes_info):
        if not hasattr(node, "lineno") or not hasattr(node, "end_lineno"):
            continue
        line_start = int(getattr(node, "lineno", 1))
        line_end = int(getattr(node, "end_lineno", line_start))
        snippet = "\n".join(lines[line_start - 1 : line_end]).strip()
        if not snippet:
            continue
            
        if len(snippet) > chunk_size and node_type == "python_class":
            # Nếu class quá lớn, không đưa toàn bộ class vào 1 chunk (tránh phình to RAG)
            # Thay vào đó chunk_text_with_metadata sẽ chia nhỏ nó, 
            # HOẶC bỏ qua vì các method bên trong đã được bóc tách riêng.
            # Ở đây ta chọn băm nhỏ nó ra.
            sub_chunks = chunk_text_with_metadata(
                snippet,
                chunk_size,
                chunk_overlap,
                source_name=source_name,
                chunk_type=f"{node_type}_part",
                section=section_name,
            )
            for sc in sub_chunks:
                # Tính lại line_start/end cho các sub-chunk
                meta = dict(sc.metadata)
                meta["chunk_index"] = len(records)
                meta["line_start"] = line_start + int(meta.get("line_start", 1)) - 1
                meta["line_end"] = line_start + int(meta.get("line_end", 1)) - 1
                records.append(StructuredChunk(text=sc.text, metadata=meta))
        else:
            # Function hoặc Class nhỏ gọn thì đưa vào 1 chunk
            # Nếu Function quá lớn, ta cũng băm nhỏ nó.
            if len(snippet) > chunk_size:
                sub_chunks = chunk_text_with_metadata(
                    snippet,
                    chunk_size,
                    chunk_overlap,
                    source_name=source_name,
                    chunk_type=f"{node_type}_part",
                    section=section_name,
                )
                for sc in sub_chunks:
                    meta = dict(sc.metadata)
                    meta["chunk_index"] = len(records)
                    meta["line_start"] = line_start + int(meta.get("line_start", 1)) - 1
                    meta["line_end"] = line_start + int(meta.get("line_end", 1)) - 1
                    records.append(StructuredChunk(text=sc.text, metadata=meta))
            else:
                records.append(
                    StructuredChunk(
                        text=snippet,
                        metadata={
                            "source_name": source_name,
                            "section": section_name,
                            "chunk_type": node_type,
                            "chunk_index": len(records),
                            "line_start": line_start,
                            "line_end": line_end,
                        },
                    )
                )

    if records:
        return records

    return chunk_text_with_metadata(
        text,
        chunk_size,
        chunk_overlap,
        source_name=source_name,
        chunk_type="python_module",
        section=source_name,
    )


def chunk_structured_source(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    *,
    source_name: str = "",
    language: str,
) -> list[StructuredChunk]:
    if not text or not text.strip():
        return []

    parsed = parse_source_structure(text, language, source_name=source_name)
    records: list[StructuredChunk] = []
    if parsed.syntax_error:
        records.append(
            StructuredChunk(
                text=f"[AST SyntaxError]\n{parsed.syntax_error}",
                metadata={
                    "source_name": source_name,
                    "section": "syntax_error",
                    "chunk_type": f"{parsed.language}_syntax_error",
                    "chunk_index": 0,
                    "line_start": 1,
                    "line_end": 1,
                    "parser_backend": parsed.parser_backend,
                    "parser_available": parsed.parser_available,
                },
            )
        )

    for symbol in parsed.symbols:
        if not symbol.source:
            continue
        if len(symbol.source) > chunk_size:
            sub_chunks = chunk_text_with_metadata(
                symbol.source,
                chunk_size,
                chunk_overlap,
                source_name=source_name,
                chunk_type=f"{symbol.kind}_part",
                section=symbol.name,
            )
            for sub_chunk in sub_chunks:
                metadata = dict(sub_chunk.metadata)
                metadata["chunk_index"] = len(records)
                metadata["line_start"] = symbol.line_start + int(metadata.get("line_start", 1)) - 1
                metadata["line_end"] = symbol.line_start + int(metadata.get("line_end", 1)) - 1
                metadata["parser_backend"] = parsed.parser_backend
                metadata["parser_available"] = parsed.parser_available
                records.append(StructuredChunk(text=sub_chunk.text, metadata=metadata))
            continue
        records.append(
            StructuredChunk(
                text=symbol.source,
                metadata={
                    "source_name": source_name,
                    "section": symbol.name,
                    "chunk_type": symbol.kind,
                    "chunk_index": len(records),
                    "line_start": symbol.line_start,
                    "line_end": symbol.line_end,
                    "parser_backend": parsed.parser_backend,
                    "parser_available": parsed.parser_available,
                },
            )
        )

    if records:
        return records
    return chunk_text_with_metadata(
        text,
        chunk_size,
        chunk_overlap,
        source_name=source_name,
        chunk_type=f"{parsed.language}_module",
        section=source_name,
    )


def chunk_markdown_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
    *,
    source_name: str = "",
) -> list[StructuredChunk]:
    if not text or not text.strip():
        return []

    lines = text.splitlines()
    
    global_title = source_name or "document"
    for line in lines:
        if line.strip().startswith("# "):
            global_title = line.strip("# ").strip()
            break
            
    records: list[StructuredChunk] = []
    
    current_chunk_lines: list[str] = []
    current_chunk_len = 0
    current_start_line = 1
    
    header_stack: list[tuple[int, str]] = []
    in_code_block = False
    
    def get_section_path() -> str:
        if not header_stack:
            return global_title
        return " > ".join(t for _, t in header_stack)
        
    def flush(end_line: int):
        nonlocal current_chunk_lines, current_chunk_len, current_start_line
        if not current_chunk_lines:
            return
            
        chunk_text_raw = "\n".join(current_chunk_lines).strip()
        if not chunk_text_raw:
            current_chunk_lines = []
            current_chunk_len = 0
            current_start_line = end_line + 1
            return
            
        section_path = get_section_path()
        context_header = f"[Context: {section_path}]"
        
        sub_chunks = chunk_text_with_metadata(
            chunk_text_raw,
            chunk_size,
            chunk_overlap,
            source_name=source_name,
            chunk_type="markdown_section",
            section=section_path,
        )
        for offset, record in enumerate(sub_chunks):
            metadata = dict(record.metadata)
            metadata["chunk_index"] = len(records)
            metadata["line_start"] = current_start_line
            metadata["line_end"] = end_line
            
            final_text = f"{context_header}\n{record.text}"
            records.append(StructuredChunk(text=final_text, metadata=metadata))
            
        current_chunk_lines = []
        current_chunk_len = 0
        current_start_line = end_line + 1

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            
        is_header = False
        header_level = 0
        header_title = ""
        if not in_code_block and stripped.startswith("#"):
            parts = stripped.split(" ", 1)
            if parts[0].count("#") == len(parts[0]):
                is_header = True
                header_level = len(parts[0])
                header_title = parts[1].strip() if len(parts) > 1 else ""

        if is_header:
            flush(line_no - 1)
            while header_stack and header_stack[-1][0] >= header_level:
                header_stack.pop()
            header_stack.append((header_level, header_title))
            current_chunk_lines.append(line)
            current_chunk_len += len(line) + 1
            current_start_line = line_no
            continue
            
        current_chunk_lines.append(line)
        current_chunk_len += len(line) + 1
        
        if not in_code_block and current_chunk_len >= chunk_size * 0.8:
            if stripped == "":
                flush(line_no)
                
    flush(len(lines))
    return records


def chunk_section(
    name: str,
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[StructuredChunk]:
    lower_name = (name or "").lower()
    if lower_name.endswith(".py"):
        return chunk_python_source(text, chunk_size, chunk_overlap, source_name=name)
    if lower_name.endswith(".java"):
        return chunk_structured_source(text, chunk_size, chunk_overlap, source_name=name, language="java")
    if lower_name.endswith((".js", ".jsx")):
        return chunk_structured_source(text, chunk_size, chunk_overlap, source_name=name, language="javascript")
    if lower_name.endswith((".ts", ".tsx")):
        return chunk_structured_source(text, chunk_size, chunk_overlap, source_name=name, language="typescript")
    if lower_name.endswith((".md", ".markdown")) or "\n#" in f"\n{text}":
        return chunk_markdown_text(text, chunk_size, chunk_overlap, source_name=name)
    return chunk_text_with_metadata(
        text,
        chunk_size,
        chunk_overlap,
        source_name=name,
        chunk_type="text",
        section=name,
    )

def chunk_pdf_pages_with_metadata(
    pages: list[dict],
    chunk_size: int,
    chunk_overlap: int,
    *,
    source_name: str = "",
    source_rules: dict | None = None,
) -> list[StructuredChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    records: list[StructuredChunk] = []
    
    for page_dict in pages:
        page_num = page_dict.get("page", 0)
        page_text = page_dict.get("text", "")
        if not page_text or not page_text.strip():
            continue
            
        page_chunks = chunk_text(page_text, chunk_size, chunk_overlap)
        
        lines = page_text.strip().split("\n")
        section = lines[0].strip() if lines else f"Page {page_num}"
        
        for i, chunk in enumerate(page_chunks):
            metadata = {
                "source_name": source_name or page_dict.get("source_name", ""),
                "section": section,
                "chunk_type": "pdf_doc",
                "chunk_index": len(records),
                "page_start": page_num,
                "page_end": page_num,
            }
            if source_rules:
                for k in ["framework", "priority", "source_type"]:
                    if k in source_rules:
                        metadata[k] = source_rules[k]
                        
            records.append(
                StructuredChunk(
                    text=chunk,
                    metadata=metadata,
                )
            )
            
    return records

