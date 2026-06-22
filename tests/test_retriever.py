from __future__ import annotations

from testgen.rag.retriever import retrieve_context, retrieve_context_with_diagnostics


class FakeCollection:
    """Minimal ChromaDB collection mock."""

    def __init__(self, documents: list[list[str]] | None = None):
        self._documents = documents

    def query(self, query_embeddings, n_results, include):
        return {"documents": self._documents}


def _constant_embedder(text: str) -> list[float]:
    return [0.1, 0.2, 0.3]


def test_retrieve_context_returns_empty_when_collection_is_none():
    assert retrieve_context(None, "query", 3, embedder=_constant_embedder) == ""


def test_retrieve_context_returns_empty_for_empty_query():
    col = FakeCollection(documents=[["doc1"]])
    assert retrieve_context(col, "", 3, embedder=_constant_embedder) == ""


def test_retrieve_context_returns_empty_for_none_query():
    col = FakeCollection(documents=[["doc1"]])
    assert retrieve_context(col, None, 3, embedder=_constant_embedder) == ""


def test_retrieve_context_returns_joined_documents():
    col = FakeCollection(documents=[["chunk A", "chunk B"]])
    result = retrieve_context(col, "test query", 2, embedder=_constant_embedder)
    assert "chunk A" in result
    assert "chunk B" in result


def test_retrieve_context_strips_whitespace_from_chunks():
    col = FakeCollection(documents=[["  hello  ", "  world  "]])
    result = retrieve_context(col, "q", 2, embedder=_constant_embedder)
    assert result == "hello\n\nworld"


def test_retrieve_context_filters_empty_chunks():
    col = FakeCollection(documents=[["valid", "", "   ", "also valid"]])
    result = retrieve_context(col, "q", 4, embedder=_constant_embedder)
    assert "valid" in result
    assert "also valid" in result
    # Empty/whitespace chunks should not appear
    lines = [line for line in result.split("\n\n") if line.strip()]
    assert len(lines) == 2


def test_retrieve_context_handles_empty_documents_list():
    col = FakeCollection(documents=[])
    assert retrieve_context(col, "q", 3, embedder=_constant_embedder) == ""


def test_retrieve_context_handles_none_documents():
    col = FakeCollection(documents=None)
    assert retrieve_context(col, "q", 3, embedder=_constant_embedder) == ""


def test_retrieve_context_diagnostics_handles_missing_metadata_fields():
    class MetadataCollection:
        def query(self, query_embeddings, n_results, include):
            return {
                "documents": [["chunk A"]],
                "metadatas": [[{"source_name": "doc.md"}]],
                "distances": [[0.25]],
            }

    context, diagnostics = retrieve_context_with_diagnostics(
        MetadataCollection(),
        "query",
        1,
        embedder=_constant_embedder,
    )

    assert context == "chunk A"
    source = diagnostics["sources"][0]
    assert source["source_name"] == "doc.md"
    assert source["section"] == "unknown"
    assert "section" in source["metadata_missing_fields"]
