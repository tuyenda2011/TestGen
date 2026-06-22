import streamlit as st
from testgen.core.config import (
    CHROMA_PATH,
    DOC_COLLECTION_NAME,
    SOURCE_COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    GEMINI_EMBED_MODEL,
    EMBED_MODEL
)
from testgen.rag.vector_store import (
    get_collection,
    create_or_reset_collection,
    add_chunks,
    delete_collection
)
from testgen.rag.index_cache import build_labeled_chunks, prepare_indexed_collection
from testgen.core.llm import get_gemini_embedding, get_ollama_embedding
from testgen.core.utils import normalize_text

def _doc_embedder(embedding_backend: str, api_key: str | None):
    if embedding_backend == "gemini":
        return lambda text: get_gemini_embedding(
            text,
            api_key=api_key,
            model=GEMINI_EMBED_MODEL,
            task_type="RETRIEVAL_DOCUMENT",
        )
    return lambda text: get_ollama_embedding(text)

def _rag_signature_key(collection_name: str) -> str:
    return f"rag_index_signature::{collection_name}"

def _chunk_labeled_sections(sections: list[tuple[str, str]], section_prefix: str) -> list[str]:
    return build_labeled_chunks(sections, section_prefix, CHUNK_SIZE, CHUNK_OVERLAP)

def _collection_count(collection_name: str) -> int:
    if not CHROMA_PATH.exists():
        return 0
    collection = get_collection(collection_name)
    if collection is None:
        return 0
    try:
        return int(collection.count())
    except Exception as exc:
        from testgen.core.logger import get_logger
        logger = get_logger(__name__)
        logger.warning(f"Lỗi khi lấy collection_count trong ui: {exc}")
        return 0

def sync_docs_rag_state() -> int:
    chunk_count = _collection_count(DOC_COLLECTION_NAME)
    if st.session_state.get("docs_rag_stale", False):
        st.session_state["docs_rag_ready"] = False
        st.session_state["docs_rag_chunk_count"] = chunk_count
    elif chunk_count > 0:
        st.session_state["docs_rag_ready"] = True
        st.session_state["docs_rag_chunk_count"] = chunk_count
    else:
        st.session_state["docs_rag_ready"] = False
        st.session_state["docs_rag_chunk_count"] = 0
    return chunk_count

def invalidate_docs_rag_index() -> None:
    delete_collection(DOC_COLLECTION_NAME)
    st.session_state.pop(_rag_signature_key(DOC_COLLECTION_NAME), None)
    st.session_state["docs_rag_ready"] = False
    st.session_state["docs_rag_stale"] = True
    st.session_state["docs_rag_stale_reason"] = "documents_changed"
    st.session_state["docs_rag_chunk_count"] = 0

def index_rag_sections(
    collection_name: str,
    sections: list[tuple[str, str]],
    section_prefix: str,
    embedding_backend: str,
    api_key: str | None,
) -> tuple[int, bool]:
    chunks = _chunk_labeled_sections(sections, section_prefix)
    if not chunks:
        return 0, False
    previous_signature = str(st.session_state.get(_rag_signature_key(collection_name), "") or "")
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
    st.session_state[_rag_signature_key(collection_name)] = prepared.signature
    return len(prepared.chunks), prepared.reused
