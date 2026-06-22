from __future__ import annotations

from testgen.rag.chunker import chunk_python_source
from testgen.rag.chunker import chunk_markdown_text, chunk_section, chunk_text_with_metadata
from testgen.rag.index_cache import build_labeled_chunk_records
from testgen.rag.retriever import retrieve_context_with_diagnostics


def test_chunk_python_source_uses_functions_with_line_metadata():
    records = chunk_python_source(
        "def add(a, b):\n    return a + b\n\nclass Calc:\n    def ok(self):\n        return True\n",
        chunk_size=200,
        chunk_overlap=20,
        source_name="calc.py",
    )

    assert [record.metadata["chunk_type"] for record in records] == ["python_function", "python_class", "python_function"]
    assert records[0].metadata["section"] == "add"
    assert records[0].metadata["line_start"] == 1


def test_labeled_chunk_records_preserve_metadata():
    records = build_labeled_chunk_records(
        [("calc.py", "def add(a, b):\n    return a + b\n")],
        "Source code",
        200,
        20,
    )

    assert records[0].text.startswith("# Source code: calc.py")
    assert records[0].metadata["source_name"] == "calc.py"
    assert records[0].metadata["chunk_type"] == "python_function"


class _FakeCollection:
    def query(self, **kwargs):
        return {
            "documents": [["# Source code: calc.py\n\ndef add(a, b): return a + b"]],
            "metadatas": [[{"source_name": "calc.py", "section": "add", "line_start": 1, "line_end": 1}]],
            "distances": [[0.12]],
        }


def test_retrieve_context_with_diagnostics_returns_sources():
    context, diagnostics = retrieve_context_with_diagnostics(
        _FakeCollection(),
        "add",
        4,
        embedder=lambda text: [0.1, 0.2],
    )

    assert "def add" in context
    assert diagnostics["returned_chunks"] == 1
    assert diagnostics["sources"][0]["source_name"] == "calc.py"
    assert diagnostics["sources"][0]["score"] == 0.88


def test_chunk_markdown_text_uses_headings_as_sections():
    records = chunk_markdown_text("# Intro\nHello\n\n## API\nDetails", 200, 20, source_name="docs.md")

    assert len(records) == 2
    assert records[0].metadata["section"] == "Intro"
    assert records[1].metadata["section"] == "API"


def test_chunk_section_falls_back_to_text_metadata_for_plain_text():
    records = chunk_section("notes.txt", "plain text", 200, 20)

    assert records[0].metadata["chunk_type"] == "text"
    assert records[0].metadata["source_name"] == "notes.txt"


def test_chunk_section_uses_tree_sitter_for_java_source():
    records = chunk_section(
        "Calculator.java",
        "public class Calculator { int add(int a, int b) { return a + b; } }",
        200,
        20,
    )

    chunk_types = [record.metadata["chunk_type"] for record in records]
    assert "java_class" in chunk_types
    assert "java_method" in chunk_types
    assert any(record.metadata["section"] == "add" for record in records)
    assert all("parser_backend" in record.metadata for record in records)


def test_chunk_section_uses_tree_sitter_for_javascript_source():
    records = chunk_section(
        "cart.js",
        "class Cart { total(a, b) { return a + b; } }\nconst tax = (value) => value * 0.1;",
        200,
        20,
    )

    chunk_types = [record.metadata["chunk_type"] for record in records]
    assert "javascript_class" in chunk_types
    assert "javascript_function" in chunk_types
    assert any(record.metadata["section"] == "tax" for record in records)


def test_chunk_text_with_metadata_validates_empty_text():
    assert chunk_text_with_metadata("", 100, 10, source_name="empty.txt") == []


def test_chunk_python_source_falls_back_when_syntax_invalid():
    records = chunk_python_source("def broken(:\n    pass\n", 200, 20, source_name="broken.py")

    assert records[0].metadata["chunk_type"] == "python_syntax_error"
    assert "SyntaxError" in records[0].text
