"""Unit tests cho P0 RAG PDF improvements.

Covers:
1. test_load_pdf_pages_preserves_page_metadata
2. test_pdf_source_rules_assign_framework_and_priority
3. test_chunk_pdf_pages_adds_framework_page_metadata
4. test_retrieve_context_passes_metadata_filter
5. test_rag_quality_warns_framework_mismatch

Plus regression tests cho section filter, metadata filter fallback,
framework isolation, ve missing metadata warnings.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from testgen.rag.chunker import chunk_pdf_pages_with_metadata
from testgen.rag.document_loader import load_pdf_pages
from testgen.rag.pdf_sources import (
    PDF_RAG_SOURCE_RULES,
    filter_pdf_pages,
    get_source_rules,
    should_keep_pdf_page_or_section,
)
from testgen.rag.quality import assess_rag_quality
from testgen.rag.retriever import _build_chroma_where_filter, retrieve_context_with_diagnostics


# ---------------------------------------------------------------------------
# 1. load_pdf_pages e P0.1
# ---------------------------------------------------------------------------

class TestLoadPdfPages:
    def test_load_pdf_pages_preserves_page_metadata(self):
        """M?i page ph?i ce page number, text, source_name."""
        with patch("testgen.rag.document_loader.PdfReader") as mock_reader:
            page1 = MagicMock()
            page1.extract_text.return_value = "pytest assertions chapter"
            page2 = MagicMock()
            page2.extract_text.return_value = "  "  # r?ng e ph?i b? b?
            page3 = MagicMock()
            page3.extract_text.return_value = "fixtures and conftest"
            mock_pdf = MagicMock()
            mock_pdf.pages = [page1, page2, page3]
            mock_reader.return_value = mock_pdf

            result = load_pdf_pages(b"dummy", source_name="pytest_official.pdf")

        assert len(result) == 2, "Page r?ng ph?i b? b?"
        assert result[0]["page"] == 1
        assert result[0]["source_name"] == "pytest_official.pdf"
        assert "pytest assertions" in result[0]["text"]
        assert result[1]["page"] == 3
        assert result[1]["source_name"] == "pytest_official.pdf"

    def test_load_pdf_pages_empty_bytes_returns_empty(self):
        result = load_pdf_pages(b"")
        assert result == []

    def test_load_pdf_pages_none_returns_empty(self):
        result = load_pdf_pages(None)
        assert result == []

    def test_load_pdf_pages_source_name_propagated(self):
        with patch("testgen.rag.document_loader.PdfReader") as mock_reader:
            page = MagicMock()
            page.extract_text.return_value = "JUnit assertions"
            mock_pdf = MagicMock()
            mock_pdf.pages = [page]
            mock_reader.return_value = mock_pdf

            result = load_pdf_pages(b"dummy", source_name="junit5_user_guide_official.pdf")

        assert result[0]["source_name"] == "junit5_user_guide_official.pdf"

    def test_load_pdf_pages_no_source_name_defaults_empty(self):
        with patch("testgen.rag.document_loader.PdfReader") as mock_reader:
            page = MagicMock()
            page.extract_text.return_value = "some content"
            mock_pdf = MagicMock()
            mock_pdf.pages = [page]
            mock_reader.return_value = mock_pdf

            result = load_pdf_pages(b"dummy")

        assert result[0]["source_name"] == ""


# ---------------------------------------------------------------------------
# 2. PDF_RAG_SOURCE_RULES e P0.2
# ---------------------------------------------------------------------------

class TestPdfSourceRules:
    def test_pdf_source_rules_assign_framework_and_priority(self):
        """M?i PDF seed ph?i ce framework ve priority."""
        for fname, rules in PDF_RAG_SOURCE_RULES.items():
            assert "framework" in rules, f"{fname} thi?u framework"
            assert rules["framework"], f"{fname} framework r?ng"
            assert "priority" in rules, f"{fname} thi?u priority"
            assert "source_type" in rules, f"{fname} thi?u source_type"

    def test_pytest_official_has_correct_framework(self):
        rules = PDF_RAG_SOURCE_RULES["pytest_official.pdf"]
        assert rules["framework"] == "pytest"
        assert rules["priority"] == "P0"

    def test_junit5_has_correct_framework(self):
        rules = PDF_RAG_SOURCE_RULES["junit5_user_guide_official.pdf"]
        assert rules["framework"] == "JUnit"

    def test_postman_focused_docs_matches_runtime_framework_name(self):
        rules = PDF_RAG_SOURCE_RULES["postman_focused_docs.md"]
        assert rules["framework"] == "Postman script"

    def test_selenium_pdf_rule_available(self):
        rules = PDF_RAG_SOURCE_RULES["selenium_python_bindings_unofficial.pdf"]
        assert rules["framework"] == "Selenium"

    def test_get_source_rules_case_insensitive(self):
        rules = get_source_rules("PYTEST_OFFICIAL.PDF")
        assert rules.get("framework") == "pytest"

    def test_get_source_rules_unknown_returns_empty(self):
        rules = get_source_rules("unknown_file.pdf")
        assert rules == {}

    def test_all_rules_have_include_and_exclude_keywords(self):
        for fname, rules in PDF_RAG_SOURCE_RULES.items():
            assert isinstance(rules.get("include_keywords"), list), f"{fname} thi?u include_keywords list"
            assert isinstance(rules.get("exclude_keywords"), list), f"{fname} thi?u exclude_keywords list"
            assert len(rules["include_keywords"]) > 0, f"{fname} include_keywords r?ng"


# ---------------------------------------------------------------------------
# 3. chunk_pdf_pages_with_metadata e P0.4
# ---------------------------------------------------------------------------

class TestChunkPdfPagesWithMetadata:
    def _make_pages(self, texts: list[str], source_name: str = "pytest_official.pdf"):
        return [
            {"page": i + 1, "text": t, "source_name": source_name}
            for i, t in enumerate(texts)
        ]

    def test_chunk_pdf_pages_adds_framework_page_metadata(self):
        """M?i chunk ph?i ce framework, page_start, page_end, chunk_type=pdf_doc."""
        pages = self._make_pages(["pytest assert and raises usage " * 20])
        rules = {"framework": "pytest", "priority": "P0", "source_type": "official_pdf"}
        chunks = chunk_pdf_pages_with_metadata(pages, chunk_size=200, chunk_overlap=20, source_rules=rules)

        assert chunks, "Ph?i ce et nh?t 1 chunk"
        for chunk in chunks:
            assert chunk.metadata["framework"] == "pytest"
            assert chunk.metadata["chunk_type"] == "pdf_doc"
            assert chunk.metadata["page_start"] == 1
            assert chunk.metadata["page_end"] == 1
            assert chunk.metadata["priority"] == "P0"
            assert chunk.metadata["source_type"] == "official_pdf"

    def test_chunk_pdf_pages_empty_pages_returns_empty(self):
        chunks = chunk_pdf_pages_with_metadata([], chunk_size=500, chunk_overlap=50, source_rules={})
        assert chunks == []

    def test_chunk_pdf_pages_multiple_pages_have_correct_page_numbers(self):
        pages = self._make_pages(["page one content " * 10, "page two content " * 10])
        rules = {"framework": "JUnit", "priority": "P0", "source_type": "official_pdf"}
        chunks = chunk_pdf_pages_with_metadata(pages, chunk_size=500, chunk_overlap=50, source_rules=rules)

        page_numbers = {c.metadata["page_start"] for c in chunks}
        assert 1 in page_numbers
        assert 2 in page_numbers

    def test_chunk_pdf_pages_section_from_first_line(self):
        pages = [{"page": 1, "text": "How to use assertions\nmore content here", "source_name": "pytest_official.pdf"}]
        rules = {"framework": "pytest", "priority": "P0", "source_type": "official_pdf"}
        chunks = chunk_pdf_pages_with_metadata(pages, chunk_size=500, chunk_overlap=50, source_rules=rules)
        assert chunks[0].metadata["section"] == "How to use assertions"

    def test_chunk_pdf_pages_skips_empty_pages(self):
        pages = [
            {"page": 1, "text": "valid content " * 20, "source_name": "x.pdf"},
            {"page": 2, "text": "   ", "source_name": "x.pdf"},
        ]
        rules = {"framework": "pytest", "priority": "P0", "source_type": "official_pdf"}
        chunks = chunk_pdf_pages_with_metadata(pages, chunk_size=500, chunk_overlap=50, source_rules=rules)
        page_nums = {c.metadata["page_start"] for c in chunks}
        assert 2 not in page_nums

    def test_chunk_pdf_pages_invalid_chunk_size_raises(self):
        with pytest.raises(ValueError, match="chunk_size"):
            chunk_pdf_pages_with_metadata(
                [{"page": 1, "text": "x", "source_name": "x"}],
                chunk_size=0,
                chunk_overlap=0,
                source_rules={},
            )


# ---------------------------------------------------------------------------
# 3b. should_keep_pdf_page_or_section e P0.3
# ---------------------------------------------------------------------------

class TestShouldKeepPdfPageOrSection:
    def test_keeps_page_with_include_keyword(self):
        rules = {"include_keywords": ["assert", "raises"], "exclude_keywords": []}
        assert should_keep_pdf_page_or_section("How to write assert statements in pytest", rules) is True

    def test_drops_page_with_exclude_keyword_in_header(self):
        rules = {"include_keywords": ["assert"], "exclude_keywords": ["changelog"]}
        assert should_keep_pdf_page_or_section("changelog\nsome extra content", rules) is False

    def test_keeps_empty_include_list_no_exclude(self):
        """Kheng ce include list ve kheng ce exclude ? gi?."""
        rules: dict = {}
        assert should_keep_pdf_page_or_section("some general content", rules) is True

    def test_drops_empty_text(self):
        assert should_keep_pdf_page_or_section("", {}) is False
        assert should_keep_pdf_page_or_section("   ", {}) is False

    def test_filter_pdf_pages_logs_kept_dropped(self):
        pages = [
            {"page": 1, "text": "assert usage in pytest", "source_name": "pytest_official.pdf"},
            {"page": 2, "text": "changelog\nold changes listed here", "source_name": "pytest_official.pdf"},
            {"page": 3, "text": "fixtures and conftest setup", "source_name": "pytest_official.pdf"},
        ]
        rules = {"include_keywords": ["assert", "fixture"], "exclude_keywords": ["changelog"]}
        kept, kept_count, dropped_count = filter_pdf_pages(pages, rules)
        assert dropped_count == 1
        assert kept_count == 2
        assert all("changelog" not in p["text"] for p in kept)


# ---------------------------------------------------------------------------
# 4. retrieve_context_with_diagnostics e P0.5
# ---------------------------------------------------------------------------

class TestRetrieveContextMetadataFilter:
    def _make_collection(self, docs: list[str], metadatas: list[dict]):
        """T?o mock ChromaDB collection."""
        collection = MagicMock()
        collection.query.return_value = {
            "documents": [docs],
            "metadatas": [metadatas],
            "distances": [[0.1] * len(docs)],
        }
        return collection

    def test_retrieve_context_passes_metadata_filter(self):
        """metadata_filter ph?i du?c truy?n veo collection.query du?i d?ng where clause."""
        collection = self._make_collection(
            ["pytest assert content"],
            [{"source_name": "pytest_official.pdf", "framework": "pytest",
              "section": "assertions", "chunk_type": "pdf_doc",
              "page_start": 1, "page_end": 1}],
        )

        context, diagnostics = retrieve_context_with_diagnostics(
            collection,
            query="pytest assertions",
            top_k=3,
            metadata_filter={"framework": "pytest"},
        )

        call_kwargs = collection.query.call_args[1]
        assert "where" in call_kwargs, "Ph?i truy?n where clause khi ce metadata_filter"
        assert "pytest" in context

    def test_retrieve_context_no_filter_no_where_clause(self):
        """Kheng ce metadata_filter ? kheng truy?n where veo collection.query."""
        collection = self._make_collection(
            ["some content"],
            [{"source_name": "x", "section": "s", "chunk_type": "text",
              "line_start": 1, "line_end": 2}],
        )

        retrieve_context_with_diagnostics(collection, query="test", top_k=3)

        call_kwargs = collection.query.call_args[1]
        assert "where" not in call_kwargs

    def test_retrieve_context_diagnostics_has_applied_filter(self):
        collection = self._make_collection(
            ["junit content"],
            [{"source_name": "junit5.pdf", "framework": "JUnit",
              "section": "annotations", "chunk_type": "pdf_doc",
              "page_start": 5, "page_end": 5}],
        )

        _, diagnostics = retrieve_context_with_diagnostics(
            collection,
            query="JUnit assertThrows",
            top_k=3,
            metadata_filter={"framework": "JUnit"},
        )

        assert diagnostics["applied_filter"] is True
        assert diagnostics["metadata_filter"] == {"framework": "JUnit"}

    def test_retrieve_context_sources_include_framework_and_page(self):
        """sources trong diagnostics ph?i ce framework, page_start, page_end."""
        collection = self._make_collection(
            ["pytest fixture content"],
            [{"source_name": "pytest_official.pdf", "framework": "pytest",
              "section": "fixtures", "chunk_type": "pdf_doc",
              "page_start": 12, "page_end": 13}],
        )

        _, diagnostics = retrieve_context_with_diagnostics(
            collection, query="fixtures", top_k=3
        )

        source = diagnostics["sources"][0]
        assert source["framework"] == "pytest"
        assert source["page_start"] == 12
        assert source["page_end"] == 13

    def test_retrieve_context_fallback_when_filter_raises(self):
        """N?u where filter raise exception ? fallback query kheng filter."""
        collection = MagicMock()
        call_count = {"n": 0}

        def side_effect(**kwargs):
            call_count["n"] += 1
            if "where" in kwargs:
                raise Exception("ChromaDB where filter error")
            return {
                "documents": [["fallback content"]],
                "metadatas": [[{"source_name": "x", "section": "s",
                                "chunk_type": "text", "line_start": 1, "line_end": 1}]],
                "distances": [[0.2]],
            }

        collection.query.side_effect = side_effect

        context, diagnostics = retrieve_context_with_diagnostics(
            collection,
            query="test",
            top_k=3,
            metadata_filter={"framework": "pytest"},
        )
        assert "fallback content" in context
        assert call_count["n"] == 2  # l?n 1 filter (fail), l?n 2 fallback

    def test_build_chroma_where_filter_single_key(self):
        metadata_filter = {"framework": "pytest"}
        result = _build_chroma_where_filter(metadata_filter)
        assert result == {"framework": {"$in": ["pytest", "Python", "pytest-cov", "coverage"]}}

    def test_build_chroma_where_filter_multiple_keys(self):
        result = _build_chroma_where_filter({"framework": "pytest", "priority": "P0"})
        assert result is not None
        assert "$and" in result
        assert len(result["$and"]) == 2

    def test_build_chroma_where_filter_empty_returns_none(self):
        assert _build_chroma_where_filter({}) is None
        assert _build_chroma_where_filter(None) is None


# ---------------------------------------------------------------------------
# 5. assess_rag_quality framework mismatch e P0.6
# ---------------------------------------------------------------------------

class TestRagQualityFrameworkMismatch:
    def test_rag_quality_warns_framework_mismatch(self):
        """Chunk kheng kh?p framework dang ch?y ph?i b? canh beo."""
        quality = assess_rag_quality(
            {
                "docs": {
                    "returned_chunks": 2,
                    "sources": [
                        {
                            "score": 0.75,
                            "metadata_missing_fields": [],
                            "chunk_type": "pdf_doc",
                            "framework": "JUnit",   # sai e dang ch?y pytest
                            "page_start": 1,
                            "page_end": 1,
                        },
                        {
                            "score": 0.70,
                            "metadata_missing_fields": [],
                            "chunk_type": "pdf_doc",
                            "framework": "JUnit",
                            "page_start": 2,
                            "page_end": 2,
                        },
                    ],
                }
            },
            expected_framework="pytest",
        )

        assert quality["pdf_doc_quality"]["framework_mismatch"] == 2
        assert any("framework=pytest" in w for w in quality["warnings"])

    def test_rag_quality_warns_missing_page_metadata(self):
        """Chunk thi?u page_start/page_end ph?i b? canh beo."""
        quality = assess_rag_quality(
            {
                "docs": {
                    "returned_chunks": 1,
                    "sources": [
                        {
                            "score": 0.80,
                            "metadata_missing_fields": [],
                            "chunk_type": "pdf_doc",
                            "framework": "pytest",
                            "page_start": "",   # thi?u
                            "page_end": "",     # thi?u
                        }
                    ],
                }
            },
            expected_framework="pytest",
        )

        assert quality["pdf_doc_quality"]["page_metadata_missing"] == 1
        assert any("page_start/page_end" in w for w in quality["warnings"])

    def test_rag_quality_warns_missing_framework_field(self):
        quality = assess_rag_quality(
            {
                "docs": {
                    "returned_chunks": 1,
                    "sources": [
                        {
                            "score": 0.65,
                            "metadata_missing_fields": [],
                            "chunk_type": "pdf_doc",
                            "framework": "",    # framework r?ng
                            "page_start": 3,
                            "page_end": 3,
                        }
                    ],
                }
            }
        )

        assert quality["pdf_doc_quality"]["framework_missing"] == 1
        assert any("thi?u metadata framework" in w for w in quality["warnings"])

    def test_rag_quality_no_warnings_when_correct_framework(self):
        """Kheng ce warning khi chunk kh?p framework ve d? metadata."""
        quality = assess_rag_quality(
            {
                "docs": {
                    "returned_chunks": 2,
                    "sources": [
                        {
                            "score": 0.82,
                            "metadata_missing_fields": [],
                            "chunk_type": "pdf_doc",
                            "framework": "pytest",
                            "page_start": 5,
                            "page_end": 5,
                        },
                        {
                            "score": 0.78,
                            "metadata_missing_fields": [],
                            "chunk_type": "pdf_doc",
                            "framework": "pytest",
                            "page_start": 6,
                            "page_end": 6,
                        },
                    ],
                }
            },
            expected_framework="pytest",
        )

        assert quality["pdf_doc_quality"]["framework_mismatch"] == 0
        assert quality["pdf_doc_quality"]["framework_missing"] == 0
        assert quality["pdf_doc_quality"]["page_metadata_missing"] == 0
        assert quality["pdf_doc_quality"]["warnings"] == []

    def test_rag_quality_non_pdf_chunks_not_checked(self):
        """Chunks lo?i text/python_function kheng b? ki?m tra pdf_doc quality."""
        quality = assess_rag_quality(
            {
                "docs": {
                    "returned_chunks": 1,
                    "sources": [
                        {
                            "score": 0.85,
                            "metadata_missing_fields": [],
                            "chunk_type": "python_function",   # kheng ph?i pdf_doc
                            "framework": "",
                            "page_start": "",
                            "page_end": "",
                        }
                    ],
                }
            },
            expected_framework="pytest",
        )

        # Kheng ce warnings t? pdf_doc check ve chunk_type != pdf_doc
        assert quality["pdf_doc_quality"]["framework_missing"] == 0
        assert quality["pdf_doc_quality"]["framework_mismatch"] == 0

    def test_existing_quality_tests_still_pass(self):
        """e?m bao backward compat e test cu kheng b? ?nh hu?ng."""
        # Test cu: missing when no chunks
        quality = assess_rag_quality(
            {
                "docs": {"top_k_requested": 4, "returned_chunks": 0, "sources": []},
                "source": {"top_k_requested": 4, "returned_chunks": 0, "sources": []},
            }
        )
        assert quality["verdict"] == "missing"
        assert quality["score"] == 0

        # Test cu: pdf_doc_quality key ph?i t?n t?i ngay c? khi kheng ce pdf chunks
        assert "pdf_doc_quality" in quality


# ---------------------------------------------------------------------------
# Regression: Framework isolation
# ---------------------------------------------------------------------------

class TestFrameworkIsolation:
    def test_pytest_docs_not_retrieved_when_junit_filter(self):
        """V?i metadata_filter JUnit, pytest chunk kheng du?c xu?t hi?n."""
        pytest_meta = {
            "source_name": "pytest_official.pdf", "framework": "pytest",
            "section": "assertions", "chunk_type": "pdf_doc",
            "page_start": 1, "page_end": 1,
        }
        junit_meta = {
            "source_name": "junit5_user_guide_official.pdf", "framework": "JUnit",
            "section": "assertThrows", "chunk_type": "pdf_doc",
            "page_start": 5, "page_end": 5,
        }

        collection = MagicMock()
        # Filter JUnit ch? tri v? junit chunk
        collection.query.return_value = {
            "documents": [["JUnit assertThrows content"]],
            "metadatas": [[junit_meta]],
            "distances": [[0.1]],
        }

        context, diagnostics = retrieve_context_with_diagnostics(
            collection,
            query="assertThrows annotation",
            top_k=3,
            metadata_filter={"framework": "JUnit"},
        )

        sources = diagnostics["sources"]
        assert all(s["framework"] == "JUnit" for s in sources if s["chunk_type"] == "pdf_doc")
        assert "JUnit" in context

    def test_chunk_missing_metadata_warns_in_quality(self):
        """Chunk thi?u metadata b? beo warning theo P0.6."""
        quality = assess_rag_quality(
            {
                "docs": {
                    "returned_chunks": 1,
                    "sources": [
                        {
                            "score": 0.72,
                            "metadata_missing_fields": ["source_type"],
                            "chunk_type": "pdf_doc",
                            "framework": "pytest",
                            "page_start": 1,
                            "page_end": 1,
                        }
                    ],
                }
            }
        )
        # source_type thi?u ? missing_metadata_count tang
        assert quality["missing_metadata_count"] == 1
        assert quality["verdict"] == "weak"
