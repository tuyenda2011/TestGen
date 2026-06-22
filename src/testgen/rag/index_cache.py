from __future__ import annotations

from dataclasses import dataclass
import hashlib
import inspect
import json
from typing import Any, Callable

from testgen.rag.chunker import StructuredChunk, chunk_section


@dataclass
class PreparedIndex:
    collection: Any
    chunks: list[str]
    metadatas: list[dict[str, object]]
    signature: str
    reused: bool


def build_labeled_chunk_records(
    sections: list[tuple[str, Any]],
    section_prefix: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[StructuredChunk]:
    records: list[StructuredChunk] = []
    for name, content in sections:
        if isinstance(content, str):
            section_records = chunk_section(name, content, chunk_size, chunk_overlap)
        else:
            from testgen.rag.chunker import chunk_pdf_pages_with_metadata
            from testgen.rag.pdf_sources import get_source_rules
            rules = get_source_rules(name)
            rules["source_name"] = name
            section_records = chunk_pdf_pages_with_metadata(
                content, chunk_size, chunk_overlap, source_name=name, source_rules=rules
            )
            
        if not section_records:
            continue
            
        for index, record in enumerate(section_records, start=1):
            header = f"# {section_prefix}: {name}"
            if len(section_records) > 1:
                header = f"{header} (phần {index})"
            metadata = dict(record.metadata)
            metadata["section_prefix"] = section_prefix
            metadata["source_name"] = str(metadata.get("source_name") or name)
            metadata["chunk_index"] = len(records)
            records.append(StructuredChunk(text=f"{header}\n\n{record.text}", metadata=metadata))
    return records


def build_labeled_chunks(
    sections: list[tuple[str, Any]],
    section_prefix: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    return [
        record.text
        for record in build_labeled_chunk_records(sections, section_prefix, chunk_size, chunk_overlap)
    ]


def build_sections_signature(
    *,
    collection_name: str,
    sections: list[tuple[str, Any]],
    section_prefix: str,
    backend: str,
    chunk_size: int,
    chunk_overlap: int,
) -> str:
    payload = {
        "collection_name": collection_name,
        "section_prefix": section_prefix,
        "backend": backend,
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "sections": [
            {"name": str(name), "text": str(text)}
            for name, text in sections
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _call_add_chunks(
    add_chunks_fn: Callable[..., None],
    collection: Any,
    chunks: list[str],
    metadatas: list[dict[str, object]],
) -> None:
    try:
        parameters = inspect.signature(add_chunks_fn).parameters
    except (TypeError, ValueError):
        parameters = {}
    if len(parameters) >= 3:
        add_chunks_fn(collection, chunks, metadatas)
    else:
        add_chunks_fn(collection, chunks)


def prepare_indexed_collection(
    *,
    collection_name: str,
    sections: list[tuple[str, Any]],
    section_prefix: str,
    backend: str,
    chunk_size: int,
    chunk_overlap: int,
    previous_signature: str | None,
    get_collection_fn: Callable[[str], Any],
    create_or_reset_collection_fn: Callable[[str], Any],
    add_chunks_fn: Callable[..., None],
) -> PreparedIndex:
    records = build_labeled_chunk_records(sections, section_prefix, chunk_size, chunk_overlap)
    chunks = [record.text for record in records]
    metadatas = [record.metadata for record in records]
    signature = build_sections_signature(
        collection_name=collection_name,
        sections=sections,
        section_prefix=section_prefix,
        backend=backend,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    if chunks and previous_signature == signature:
        collection = get_collection_fn(collection_name)
        if collection is not None:
            return PreparedIndex(
                collection=collection,
                chunks=chunks,
                metadatas=metadatas,
                signature=signature,
                reused=True,
            )

    collection = create_or_reset_collection_fn(collection_name)
    _call_add_chunks(add_chunks_fn, collection, chunks, metadatas)
    return PreparedIndex(
        collection=collection,
        chunks=chunks,
        metadatas=metadatas,
        signature=signature,
        reused=False,
    )
