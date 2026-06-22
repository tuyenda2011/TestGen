from __future__ import annotations

from typing import Callable

from testgen.core.llm import get_embedding
from testgen.rag.query_builder import build_enriched_query


EmbeddingFn = Callable[[str], list[float]]


def _score_from_distance(distance) -> float | None:
    try:
        return round(max(0.0, 1.0 - float(distance)), 4)
    except (TypeError, ValueError):
        return None


def _metadata_text(metadata: dict[str, object], key: str, default: str = "unknown") -> str:
    value = metadata.get(key)
    text = str(value if value is not None else "").strip()
    return text or default

def _build_chroma_where_filter(metadata_filter: dict[str, str] | None) -> dict | None:
    if not metadata_filter:
        return None
    conditions = []
    for k, v in metadata_filter.items():
        if v:
            if k == "framework" and v in ("pytest", "pytest-cov", "coverage"):
                conditions.append({k: {"$in": ["pytest", "Python", "pytest-cov", "coverage"]}})
            elif k == "framework" and v in ("JUnit", "junit"):
                conditions.append({k: {"$in": ["JUnit", "Java", "junit"]}})
            else:
                conditions.append({k: {"$eq": v}})
    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def retrieve_context_with_diagnostics(
    collection,
    query: str,
    top_k: int,
    embedder: EmbeddingFn | None = None,
    metadata_filter: dict[str, str] | None = None,
    min_score: float = 0.30,
) -> tuple[str, dict[str, object]]:
    if collection is None:
        return "", {"top_k_requested": top_k, "returned_chunks": 0, "sources": []}

    cleaned_query = (query or "").strip()
    if not cleaned_query:
        return "", {"top_k_requested": top_k, "returned_chunks": 0, "sources": []}
        
    enriched_query = build_enriched_query(cleaned_query)

    embed = embedder or get_embedding
    embedding = embed(enriched_query)
    where_filter = _build_chroma_where_filter(metadata_filter)
    
    query_kwargs = {
        "query_embeddings": [embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"]
    }
    if where_filter:
        query_kwargs["where"] = where_filter

    try:
        results = collection.query(**query_kwargs)
    except Exception:
        # Fallback if filter causes error (e.g., metadata not found or empty)
        if where_filter:
            del query_kwargs["where"]
            results = collection.query(**query_kwargs)
        else:
            raise

    documents = results.get("documents") or []
    if not documents:
        return "", {"top_k_requested": top_k, "returned_chunks": 0, "sources": []}

    top_chunks = documents[0] if documents else []
    cleaned_chunks = [chunk.strip() for chunk in top_chunks if isinstance(chunk, str) and chunk.strip()]
    metadatas = (results.get("metadatas") or [[]])[0] if results.get("metadatas") else []
    distances = (results.get("distances") or [[]])[0] if results.get("distances") else []

    sources: list[dict[str, object]] = []
    filtered_low_score_chunks = 0
    final_cleaned_chunks = []
    
    expected_metadata_fields = ("source_name", "section", "chunk_type", "line_start", "line_end")
    for index, chunk in enumerate(top_chunks):
        if not isinstance(chunk, str) or not chunk.strip():
            continue
        metadata = metadatas[index] if index < len(metadatas) and isinstance(metadatas[index], dict) else {}
        distance = distances[index] if index < len(distances) else None
        score = _score_from_distance(distance)
        
        if score is not None and score < min_score:
            filtered_low_score_chunks += 1
            # We still record it in sources for diagnostics, but we won't include it in final_cleaned_chunks
            include_in_context = False
        else:
            include_in_context = True
            final_cleaned_chunks.append(chunk.strip())

        missing_fields = [
            field
            for field in expected_metadata_fields
            if field not in metadata or metadata.get(field) in (None, "")
        ]
        source_info = {
            "rank": len(sources) + 1,
            "source_name": _metadata_text(metadata, "source_name"),
            "section": _metadata_text(metadata, "section"),
            "chunk_type": _metadata_text(metadata, "chunk_type"),
            "line_start": metadata.get("line_start", ""),
            "line_end": metadata.get("line_end", ""),
            "distance": distance,
            "score": score,
            "metadata_missing_fields": missing_fields,
            "filtered_by_min_score": not include_in_context,
        }
        for extra in ("framework", "page_start", "page_end"):
            if extra in metadata:
                source_info[extra] = metadata[extra]
                
        sources.append(source_info)
        
    diagnostics: dict[str, object] = {
        "top_k_requested": top_k,
        "returned_chunks": len(final_cleaned_chunks),
        "filtered_low_score_chunks": filtered_low_score_chunks,
        "sources": sources,
    }
    if metadata_filter:
        diagnostics["applied_filter"] = True
        diagnostics["metadata_filter"] = metadata_filter
        
    return "\n\n".join(final_cleaned_chunks), diagnostics


def retrieve_context(collection, query: str, top_k: int, embedder: EmbeddingFn | None = None) -> str:
    context, _diagnostics = retrieve_context_with_diagnostics(collection, query, top_k, embedder=embedder)
    return context

