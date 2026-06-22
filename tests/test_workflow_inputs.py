from __future__ import annotations

from testgen.workflow import resolve_retrieval_source


# ── Already covered: prefers explicit query, uses requirement before fallback, source+docs fallback ──

def test_resolve_retrieval_source_prefers_explicit_query():
    result = resolve_retrieval_source(
        retrieval_query="find auth edge cases",
        manual_requirement="test auth",
        has_docs=True,
        has_source=True,
        has_test_code=False,
    )
    assert result == "find auth edge cases"


def test_resolve_retrieval_source_uses_requirement_before_fallbacks():
    result = resolve_retrieval_source(
        retrieval_query="",
        manual_requirement="test wallet",
        has_docs=True,
        has_source=True,
        has_test_code=False,
    )
    assert result == "test wallet"


def test_resolve_retrieval_source_builds_source_docs_fallback():
    result = resolve_retrieval_source(
        retrieval_query="",
        manual_requirement="",
        has_docs=True,
        has_source=True,
        has_test_code=False,
    )
    assert "tài liệu và source code" in result


# ── New: cover remaining branches ──

def test_resolve_source_only():
    result = resolve_retrieval_source(
        retrieval_query="",
        manual_requirement="",
        has_docs=False,
        has_source=True,
        has_test_code=False,
    )
    assert "source code" in result
    assert "tài liệu" not in result


def test_resolve_docs_only():
    result = resolve_retrieval_source(
        retrieval_query="",
        manual_requirement="",
        has_docs=True,
        has_source=False,
        has_test_code=False,
    )
    assert "tài liệu" in result


def test_resolve_test_code_only():
    result = resolve_retrieval_source(
        retrieval_query="",
        manual_requirement="",
        has_docs=False,
        has_source=False,
        has_test_code=True,
    )
    assert "test code" in result


def test_resolve_nothing_returns_empty():
    result = resolve_retrieval_source(
        retrieval_query="",
        manual_requirement="",
        has_docs=False,
        has_source=False,
        has_test_code=False,
    )
    assert result == ""


def test_resolve_whitespace_query_falls_through():
    result = resolve_retrieval_source(
        retrieval_query="   ",
        manual_requirement="   ",
        has_docs=True,
        has_source=False,
        has_test_code=False,
    )
    assert "tài liệu" in result
