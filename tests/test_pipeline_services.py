from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from testgen.core import pipeline_services
from testgen.core.config import TOP_K


def test_doc_embedder():
    with patch("testgen.core.pipeline_services.get_gemini_embedding") as mock_gemini:
        fn = pipeline_services._doc_embedder("gemini", "dummy_key")
        fn("hello")
        mock_gemini.assert_called_once()
        
    with patch("testgen.core.pipeline_services.get_ollama_embedding") as mock_ollama:
        fn2 = pipeline_services._doc_embedder("ollama", None)
        fn2("hello")
        mock_ollama.assert_called_once_with("hello")


def test_query_embedder():
    with patch("testgen.core.pipeline_services.get_gemini_embedding") as mock_gemini:
        fn = pipeline_services._query_embedder("gemini", "dummy_key")
        fn("hello")
        mock_gemini.assert_called_once()
        
    with patch("testgen.core.pipeline_services.get_ollama_embedding") as mock_ollama:
        fn2 = pipeline_services._query_embedder("ollama", None)
        fn2("hello")
        mock_ollama.assert_called_once_with("hello")


@patch("testgen.core.pipeline_services.get_collection")
def test_collection_count(mock_get_collection):
    mock_get_collection.return_value = None
    assert pipeline_services.collection_count("my_col") == 0

    mock_col = MagicMock()
    mock_col.count.return_value = 5
    mock_get_collection.return_value = mock_col
    assert pipeline_services.collection_count("my_col") == 5

    mock_get_collection.side_effect = Exception("error")
    assert pipeline_services.collection_count("my_col") == 0


@patch("testgen.core.pipeline_services.build_labeled_chunks")
def test_chunk_labeled_sections(mock_build):
    mock_build.return_value = ["chunk1", "chunk2"]
    res = pipeline_services.chunk_labeled_sections([("doc1", "text")], "Tài liệu")
    assert res == ["chunk1", "chunk2"]


@patch("testgen.core.pipeline_services.chunk_labeled_sections")
def test_build_rag_context_empty(mock_chunk):
    mock_chunk.return_value = []
    context, chunks_len, reused, sig, diag = pipeline_services.build_rag_context(
        "my_col", [], "query", "Prefix", "gemini", None
    )
    assert context == ""
    assert chunks_len == 0
    assert not reused
    assert diag["skipped_reason"] == "no_chunks"


@patch("testgen.core.pipeline_services.prepare_indexed_collection")
@patch("testgen.core.pipeline_services.retrieve_context_with_diagnostics")
@patch("testgen.core.pipeline_services.chunk_labeled_sections")
def test_build_rag_context_valid(mock_chunk, mock_retrieve, mock_prepare):
    mock_chunk.return_value = ["chunk"]
    mock_prepared = MagicMock()
    mock_prepared.chunks = ["chunk"]
    mock_prepared.reused = False
    mock_prepared.signature = "sig"
    mock_prepared.collection = MagicMock()
    mock_prepare.return_value = mock_prepared

    mock_retrieve.return_value = ("context", {"sources": []})

    context, chunks_len, reused, sig, diag = pipeline_services.build_rag_context(
        "my_col", [("doc", "text")], "query text", "Prefix", "gemini", "key"
    )

    assert context == "context"
    assert chunks_len == 1
    assert sig == "sig"

    # Test empty query
    context2, chunks_len2, reused2, sig2, diag2 = pipeline_services.build_rag_context(
        "my_col", [("doc", "text")], "   ", "Prefix", "gemini", "key"
    )
    assert context2 == ""


@patch("testgen.core.pipeline_services.get_collection")
@patch("testgen.core.pipeline_services.retrieve_context_with_diagnostics")
def test_retrieve_preindexed_rag_context(mock_retrieve, mock_get_col):
    mock_get_col.return_value = None
    context, ok, diag = pipeline_services.retrieve_preindexed_rag_context("col", "q", "gemini", None)
    assert context == ""
    assert not ok

    mock_col = MagicMock()
    mock_get_col.return_value = mock_col
    mock_retrieve.return_value = ("context", {"a": 1})

    context2, ok2, diag2 = pipeline_services.retrieve_preindexed_rag_context("col", "q", "gemini", None)
    assert context2 == "context"
    assert ok2
    
    # empty query
    context3, ok3, diag3 = pipeline_services.retrieve_preindexed_rag_context("col", "", "gemini", None)
    assert context3 == ""
    assert ok3


def test_combine_sections():
    assert pipeline_services.combine_sections([], "", "label") == []
    assert pipeline_services.combine_sections([("doc1", "text")], "  pasted  ", "label") == [("doc1", "text"), ("label", "pasted")]


def test_python_source_for_generation():
    assert pipeline_services.python_source_for_generation([]) == ""
    assert pipeline_services.python_source_for_generation([("a", "  "), ("b", "text")]) == "text"


def test_merge_contexts():
    assert pipeline_services.merge_contexts("", "") == ""
    assert pipeline_services.merge_contexts("docs", "") == "Tài liệu tham khảo:\ndocs"
    assert pipeline_services.merge_contexts("", "source") == "Source code tham chiếu:\nsource"
    assert pipeline_services.merge_contexts("docs", "source") == "Tài liệu tham khảo:\ndocs\n\n---\n\nSource code tham chiếu:\nsource"


def test_clip_text():
    assert pipeline_services.clip_text("hello", 10) == "hello"
    assert pipeline_services.clip_text("hello world", 10) == "hello w..."
