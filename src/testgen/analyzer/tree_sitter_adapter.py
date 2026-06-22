from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SourceSymbol:
    name: str
    kind: str
    line_start: int
    line_end: int
    source: str
    params: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    has_return_value: bool = False


@dataclass(frozen=True)
class SourceParseResult:
    language: str
    parser_backend: str
    parser_available: bool
    syntax_error: str
    symbols: list[SourceSymbol]


_TREE_SITTER_NODE_TYPES = {
    "java": {
        "class_declaration": "java_class",
        "interface_declaration": "java_interface",
        "enum_declaration": "java_enum",
        "record_declaration": "java_record",
        "method_declaration": "java_method",
        "constructor_declaration": "java_constructor",
    },
    "javascript": {
        "class_declaration": "javascript_class",
        "function_declaration": "javascript_function",
        "generator_function_declaration": "javascript_function",
        "method_definition": "javascript_method",
        "variable_declarator": "javascript_function",
    },
    "typescript": {
        "class_declaration": "typescript_class",
        "function_declaration": "typescript_function",
        "generator_function_declaration": "typescript_function",
        "method_definition": "typescript_method",
        "variable_declarator": "typescript_function",
    },
    "python": {
        "class_definition": "python_class",
        "function_definition": "python_function",
    },
}


def normalize_source_language(language: str, source_name: str = "") -> str:
    value = (language or "").strip().lower()
    suffix = ""
    if "." in (source_name or ""):
        suffix = "." + source_name.rsplit(".", 1)[-1].lower()
    if suffix == ".java":
        return "java"
    if suffix in {".ts", ".tsx"}:
        return "typescript"
    if suffix in {".js", ".jsx"}:
        return "javascript"
    if value in {"js", "jsx"}:
        return "javascript"
    if value in {"ts", "tsx"}:
        return "typescript"
    if value in {"java", "javascript", "typescript", "python"}:
        return value
    return value or "unknown"


def _load_parser(language: str) -> tuple[Any | None, str]:
    parser_language = normalize_source_language(language)
    if parser_language == "unknown":
        return None, ""
    try:
        from tree_sitter_language_pack import get_parser

        return get_parser(parser_language), "tree-sitter-language-pack"
    except Exception:
        pass
    try:
        from tree_sitter_languages import get_parser

        return get_parser(parser_language), "tree-sitter-languages"
    except Exception:
        return None, ""


def _call_or_value(value: Any) -> Any:
    return value() if callable(value) else value


def _node_attr(node: Any, name: str, default: Any = None) -> Any:
    try:
        value = getattr(node, name)
    except AttributeError:
        return default
    return _call_or_value(value)


def _node_kind(node: Any) -> str:
    return str(_node_attr(node, "type", None) or _node_attr(node, "kind", ""))


def _point_line(point: Any, default: int) -> int:
    if point is None:
        return default
    row = getattr(point, "row", None)
    if row is not None:
        return int(_call_or_value(row)) + 1
    try:
        return int(point[0]) + 1
    except Exception:
        return default


def _node_line_start(node: Any) -> int:
    return _point_line(_node_attr(node, "start_point", None) or _node_attr(node, "start_position", None), 1)


def _node_line_end(node: Any, fallback: int) -> int:
    return _point_line(_node_attr(node, "end_point", None) or _node_attr(node, "end_position", None), fallback)


def _node_named_children(node: Any) -> list[Any]:
    children = _node_attr(node, "named_children", None)
    if isinstance(children, list):
        return children
    count = int(_node_attr(node, "named_child_count", 0) or 0)
    return [node.named_child(index) for index in range(count)]


def _node_text(source: str, node: Any) -> str:
    start = int(_node_attr(node, "start_byte", 0) or 0)
    end = int(_node_attr(node, "end_byte", len(source)) or len(source))
    return source.encode("utf-8")[start:end].decode("utf-8", errors="replace")


def _node_name(source: str, node: Any) -> str:
    name_node = node.child_by_field_name("name") if hasattr(node, "child_by_field_name") else None
    if name_node is not None:
        return _node_text(source, name_node).strip()
    return ""


def _is_function_variable(language: str, source: str, node: Any) -> bool:
    if _node_kind(node) != "variable_declarator":
        return False
    snippet = _node_text(source, node)
    return "=>" in snippet or "function" in snippet


def _parse_with_tree_sitter(source: str, language: str) -> SourceParseResult | None:
    parser_language = normalize_source_language(language)
    parser, backend = _load_parser(parser_language)
    if parser is None:
        return None

    try:
        try:
            tree = parser.parse(source)
        except TypeError:
            tree = parser.parse(source.encode("utf-8"))
        root = _call_or_value(getattr(tree, "root_node"))
    except Exception:
        return None

    node_types = _TREE_SITTER_NODE_TYPES.get(parser_language, {})
    symbols: list[SourceSymbol] = []

    def walk(node: Any) -> None:
        kind = _node_kind(node)
        mapped_kind = node_types.get(kind, "")
        if mapped_kind and (kind != "variable_declarator" or _is_function_variable(parser_language, source, node)):
            name = _node_name(source, node)
            if name:
                line_start = _node_line_start(node)
                line_end = _node_line_end(node, line_start)
                
                params: list[str] = []
                conditions: list[str] = []
                exceptions: list[str] = []
                has_return = False
                
                def inner_walk(inner_node: Any) -> None:
                    nonlocal has_return
                    inner_kind = _node_kind(inner_node)
                    if inner_kind == "if_statement":
                        cond_node = inner_node.child_by_field_name("condition") if hasattr(inner_node, "child_by_field_name") else None
                        if cond_node:
                            conditions.append(_node_text(source, cond_node))
                    elif inner_kind == "throw_statement":
                        exceptions.append(_node_text(source, inner_node).replace("throw", "").strip(" ;"))
                    elif inner_kind == "return_statement":
                        has_return = True
                    for child in _node_named_children(inner_node):
                        inner_walk(child)

                params_node = node.child_by_field_name("parameters") if hasattr(node, "child_by_field_name") else None
                if params_node:
                    for child in _node_named_children(params_node):
                        params.append(_node_text(source, child))
                
                body_node = node.child_by_field_name("body") if hasattr(node, "child_by_field_name") else None
                if body_node:
                    inner_walk(body_node)
                elif kind == "variable_declarator":
                    inner_walk(node)

                symbols.append(
                    SourceSymbol(
                        name=name,
                        kind=mapped_kind,
                        line_start=line_start,
                        line_end=line_end,
                        source=_node_text(source, node).strip(),
                        params=tuple(params),
                        conditions=tuple(conditions),
                        exceptions=tuple(exceptions),
                        has_return_value=has_return,
                    )
                )
        for child in _node_named_children(node):
            walk(child)

    walk(root)
    syntax_error = ""
    if bool(_node_attr(root, "has_error", False)):
        syntax_error = f"Tree-sitter reported syntax errors while parsing {parser_language} source."
    return SourceParseResult(
        language=parser_language,
        parser_backend=backend,
        parser_available=True,
        syntax_error=syntax_error,
        symbols=symbols,
    )


def _line_end_by_braces(lines: list[str], start_line: int) -> int:
    balance = 0
    seen_open = False
    for index in range(start_line - 1, len(lines)):
        line = lines[index]
        balance += line.count("{")
        if "{" in line:
            seen_open = True
        balance -= line.count("}")
        if seen_open and balance <= 0:
            return index + 1
    return start_line


def _heuristic_symbols(source: str, language: str) -> list[SourceSymbol]:
    parser_language = normalize_source_language(language)
    lines = source.splitlines()
    symbols: list[SourceSymbol] = []
    patterns: list[tuple[str, re.Pattern[str]]] = []
    if parser_language == "java":
        patterns = [
            ("java_class", re.compile(r"(?m)^\s*(?:public\s+|private\s+|protected\s+|abstract\s+|final\s+)*((?:class|interface|enum|record))\s+([A-Za-z_][A-Za-z0-9_]*)")),
            ("java_method", re.compile(r"(?m)^\s*(?:@\w+(?:\([^)]*\))?\s*)*(?:public\s+|private\s+|protected\s+|static\s+|final\s+|synchronized\s+|abstract\s+)*(?:[\w<>\[\], ?]+\s+)+([A-Za-z_][A-Za-z0-9_]*)\s*\([^;{}]*\)\s*(?:throws\s+[^{]+)?\{")),
        ]
    elif parser_language in {"javascript", "typescript"}:
        prefix = "typescript" if parser_language == "typescript" else "javascript"
        patterns = [
            (f"{prefix}_class", re.compile(r"(?m)^\s*(?:export\s+default\s+|export\s+)?class\s+([A-Za-z_$][A-Za-z0-9_$]*)")),
            (f"{prefix}_function", re.compile(r"(?m)^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")),
            (f"{prefix}_function", re.compile(r"(?m)^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][A-Za-z0-9_$]*)\s*=>")),
        ]
    for kind, pattern in patterns:
        for match in pattern.finditer(source):
            name = match.group(match.lastindex or 1)
            if kind == "java_class" and match.lastindex and match.lastindex >= 2:
                name = match.group(2)
            line_start = source.count("\n", 0, match.start()) + 1
            line_end = _line_end_by_braces(lines, line_start)
            snippet = "\n".join(lines[line_start - 1 : line_end]).strip()
            symbols.append(
                SourceSymbol(
                    name=name,
                    kind=kind,
                    line_start=line_start,
                    line_end=line_end,
                    source=snippet,
                )
            )
    symbols.sort(key=lambda item: (item.line_start, item.line_end, item.kind))
    return symbols


def parse_source_structure(source: str, language: str, *, source_name: str = "") -> SourceParseResult:
    parser_language = normalize_source_language(language, source_name)
    parsed = _parse_with_tree_sitter(source or "", parser_language)
    if parsed is not None:
        return parsed
    return SourceParseResult(
        language=parser_language,
        parser_backend="heuristic",
        parser_available=False,
        syntax_error="",
        symbols=_heuristic_symbols(source or "", parser_language),
    )
