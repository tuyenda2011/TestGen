from testgen.core.logger import get_logger
logger = get_logger(__name__)
from testgen.core.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    DOC_COLLECTION_NAME,
    SOURCE_COLLECTION_NAME,
)
from testgen.rag.index_cache import build_labeled_chunks, prepare_indexed_collection
from testgen.rag.vector_store import get_collection, create_or_reset_collection, add_chunks
from testgen.rag.retriever import retrieve_context_with_diagnostics
from testgen.core.utils import normalize_text
from testgen.core.llm import get_gemini_embedding, get_ollama_embedding
from testgen.core.config import GEMINI_EMBED_MODEL

def _doc_embedder(embedding_backend: str, api_key: str | None):
    if embedding_backend == "gemini":
        return lambda texts: get_gemini_embedding(
            texts,
            api_key=api_key,
            model=GEMINI_EMBED_MODEL,
            task_type="RETRIEVAL_DOCUMENT",
        )
    return lambda texts: get_ollama_embedding(texts)

def _query_embedder(embedding_backend: str, api_key: str | None):
    if embedding_backend == "gemini":
        return lambda text: get_gemini_embedding(
            text,
            api_key=api_key,
            model=GEMINI_EMBED_MODEL,
            task_type="RETRIEVAL_QUERY",
        )
    return lambda text: get_ollama_embedding(text)

def collection_count(collection_name: str) -> int:
    try:
        col = get_collection(collection_name)
        if col:
            return col.count()
    except Exception as exc:
        logger.warning(f"Lỗi khi lấy collection_count cho {collection_name}: {exc}")
    return 0

def chunk_labeled_sections(sections: list[tuple[str, str]], section_prefix: str) -> list[str]:
    return build_labeled_chunks(sections, section_prefix, CHUNK_SIZE, CHUNK_OVERLAP)

def build_rag_context(
    collection_name: str,
    sections: list[tuple[str, str]],
    query: str,
    section_prefix: str,
    embedding_backend: str,
    api_key: str | None,
    previous_signature: str = "",
) -> tuple[str, int, bool, str, dict[str, object]]:
    chunks = chunk_labeled_sections(sections, section_prefix)
    if not chunks:
        return "", 0, False, "", {
            "top_k_requested": TOP_K,
            "returned_chunks": 0,
            "sources": [],
            "skipped_reason": "no_chunks",
        }

    prepared = prepare_indexed_collection(
        collection_name=collection_name,
        sections=sections,
        section_prefix=section_prefix,
        backend=embedding_backend,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        previous_signature=previous_signature,
        get_collection_fn=get_collection,
        create_or_reset_collection_fn=create_or_reset_collection,
        add_chunks_fn=lambda collection, prepared_chunks, metadatas=None: add_chunks(
            collection,
            prepared_chunks,
            metadatas=metadatas,
            embedder=_doc_embedder(embedding_backend, api_key),
        ),
    )

    cleaned_query = normalize_text(query)
    if not cleaned_query:
        return "", len(prepared.chunks), prepared.reused, prepared.signature, {
            "top_k_requested": TOP_K,
            "returned_chunks": 0,
            "sources": [],
        }

    context, diagnostics = retrieve_context_with_diagnostics(
        prepared.collection,
        cleaned_query,
        TOP_K,
        embedder=_query_embedder(embedding_backend, api_key),
    )
    return context, len(prepared.chunks), prepared.reused, prepared.signature, diagnostics

def retrieve_preindexed_rag_context(
    collection_name: str,
    query: str,
    embedding_backend: str,
    api_key: str | None,
) -> tuple[str, bool, dict[str, object]]:
    collection = get_collection(collection_name)
    if collection is None:
        return "", False, {
            "top_k_requested": TOP_K,
            "returned_chunks": 0,
            "sources": [],
            "skipped_reason": "preindexed_collection_missing",
            "collection_name": collection_name,
        }

    cleaned_query = normalize_text(query)
    if not cleaned_query:
        return "", True, {"top_k_requested": TOP_K, "returned_chunks": 0, "sources": []}

    context, diagnostics = retrieve_context_with_diagnostics(
        collection,
        cleaned_query,
        TOP_K,
        embedder=_query_embedder(embedding_backend, api_key),
    )
    return context, True, diagnostics

def combine_sections(uploaded_entries: list[tuple[str, str]], pasted_text: str, pasted_label: str) -> list[tuple[str, str]]:
    sections = list(uploaded_entries)
    manual_text = normalize_text(pasted_text)
    if manual_text:
        sections.append((pasted_label, manual_text))
    return sections

def python_source_for_generation(source_sections: list[tuple[str, str]]) -> str:
    parts: list[str] = []
    for name, text in source_sections:
        cleaned = normalize_text(text)
        if not cleaned:
            continue
        parts.append(cleaned)
    return "\n\n".join(parts)

def merge_contexts(docs_context: str, source_context: str) -> str:
    parts: list[str] = []
    if normalize_text(docs_context):
        parts.append("Tài liệu tham khảo:\n" + normalize_text(docs_context))
    if normalize_text(source_context):
        parts.append("Source code tham chiếu:\n" + normalize_text(source_context))
    return "\n\n---\n\n".join(parts)

def clip_text(text: str, max_chars: int) -> str:
    cleaned = normalize_text(text)
    if len(cleaned) <= max_chars:
        return cleaned
    return f"{cleaned[: max_chars - 3].rstrip()}..."
