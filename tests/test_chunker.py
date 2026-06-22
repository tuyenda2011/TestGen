from __future__ import annotations

from testgen.rag.chunker import (
    chunk_text,
    chunk_text_with_metadata,
    _python_syntax_error_message,
    chunk_python_source,
    chunk_structured_source,
    chunk_markdown_text,
    chunk_section,
    StructuredChunk,
)
import pytest


def test_chunk_text_empty_returns_empty():
    assert chunk_text("", 100, 10) == []


def test_chunk_text_whitespace_only_returns_empty():
    assert chunk_text("   \n  ", 100, 10) == []


def test_chunk_text_short_text_returns_single_chunk():
    result = chunk_text("hello world", 100, 10)
    assert result == ["hello world"]


def test_chunk_text_splits_long_text():
    text = "a" * 200
    result = chunk_text(text, 100, 20)
    assert len(result) >= 2
    # Each chunk should be at most 100 chars
    for chunk in result:
        assert len(chunk) <= 100


def test_chunk_text_overlap_creates_overlapping_content():
    text = "ABCDEFGHIJ" * 5  # 50 chars
    result = chunk_text(text, 20, 5)
    # With overlap, subsequent chunks should share some content with previous
    assert len(result) >= 2


def test_chunk_text_raises_on_zero_chunk_size():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("hello", 0, 0)


def test_chunk_text_raises_on_negative_chunk_size():
    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text("hello", -1, 0)


def test_chunk_text_raises_on_negative_overlap():
    with pytest.raises(ValueError, match="chunk_overlap"):
        chunk_text("hello", 10, -1)


def test_chunk_text_raises_when_overlap_equals_chunk_size():
    with pytest.raises(ValueError, match="chunk_overlap"):
        chunk_text("hello", 10, 10)


def test_chunk_text_raises_when_overlap_exceeds_chunk_size():
    with pytest.raises(ValueError, match="chunk_overlap"):
        chunk_text("hello", 10, 15)


def test_chunk_text_zero_overlap():
    text = "a" * 30
    result = chunk_text(text, 10, 0)
    assert len(result) == 3
    for chunk in result:
        assert len(chunk) == 10

def test_chunk_text_with_metadata():
    res = chunk_text_with_metadata("abcdef", 3, 1, source_name="test.txt", section="sec")
    assert len(res) == 3
    assert res[0].text == "abc"
    assert res[0].metadata["source_name"] == "test.txt"
    assert res[0].metadata["section"] == "sec"
    assert res[0].metadata["chunk_index"] == 0
    
    assert chunk_text_with_metadata("", 10, 0) == []

def test_python_syntax_error_message():
    class DummySyntaxError(SyntaxError):
        def __init__(self):
            self.lineno = 10
            self.offset = 5
            self.msg = "bad syntax"
    exc = DummySyntaxError()
    msg = _python_syntax_error_message(exc, "file.py")
    assert "SyntaxError (file.py, line 10, column 5): bad syntax" in msg

def test_chunk_python_source_empty():
    assert chunk_python_source("", 10, 0) == []

def test_chunk_python_source_ast_fallback(monkeypatch):
    from testgen.analyzer import tree_sitter_adapter
    monkeypatch.setattr(tree_sitter_adapter, "parse_source_structure", lambda *a, **k: tree_sitter_adapter.ParsedSource(
        symbols=[], language="python", syntax_error="", parser_backend="none", parser_available=False
    ))
    
    # ast syntax error
    res = chunk_python_source("def bad(", 100, 0, source_name="bad.py")
    assert len(res) == 1
    assert "SyntaxError" in res[0].text
    
    # valid ast fallback
    res2 = chunk_python_source("def foo():\n  pass\n", 100, 0, source_name="ok.py")
    assert len(res2) > 0
    assert "def foo" in res2[0].text

    # large class
    res3 = chunk_python_source("class Big:\n" + "  pass\n" * 20, 10, 2, source_name="big.py")
    assert len(res3) > 1
    assert res3[0].metadata["chunk_type"] == "python_class_part"

    # large function
    res4 = chunk_python_source("def big():\n" + "  pass\n" * 20, 10, 2, source_name="bigf.py")
    assert len(res4) > 1
    assert res4[0].metadata["chunk_type"] == "python_function_part"

    # no records fallback
    res5 = chunk_python_source("x = 1\ny = 2\n", 100, 0)
    assert len(res5) == 1
    assert res5[0].metadata["chunk_type"] == "python_module"

def test_chunk_structured_source():
    assert chunk_structured_source("", 10, 0, language="java") == []

def test_chunk_markdown_text():
    assert chunk_markdown_text("", 10, 0) == []
    
    md = "# Title 1\nsome text\n# Title 2\nmore text"
    res = chunk_markdown_text(md, 100, 0)
    assert len(res) == 2
    assert "Title 1" in res[0].text
    assert "Title 2" in res[1].text

def test_chunk_section():
    assert chunk_section("test.py", "def x(): pass", 100, 0)[0].metadata["source_name"] == "test.py"
    assert chunk_section("test.java", "class X {}", 100, 0)[0].metadata["source_name"] == "test.java"
    assert chunk_section("test.js", "function x() {}", 100, 0)[0].metadata["source_name"] == "test.js"
    assert chunk_section("test.ts", "function x() {}", 100, 0)[0].metadata["source_name"] == "test.ts"
    assert chunk_section("test.md", "# header", 100, 0)[0].metadata["source_name"] == "test.md"
    assert chunk_section("plain", "hello", 100, 0)[0].metadata["source_name"] == "plain"
