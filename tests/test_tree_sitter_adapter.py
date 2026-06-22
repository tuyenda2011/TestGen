from __future__ import annotations

from testgen.analyzer import tree_sitter_adapter as adapter


def test_normalize_source_language_prefers_source_extension():
    assert adapter.normalize_source_language("javascript", "Example.java") == "java"
    assert adapter.normalize_source_language("", "cart.tsx") == "typescript"
    assert adapter.normalize_source_language("js") == "javascript"


def test_parse_source_structure_with_tree_sitter_java():
    result = adapter.parse_source_structure(
        "public class Calculator { int add(int a, int b) { return a + b; } }",
        "java",
        source_name="Calculator.java",
    )

    assert result.parser_available is True
    assert result.parser_backend == "tree-sitter-language-pack"
    assert [(symbol.kind, symbol.name) for symbol in result.symbols] == [
        ("java_class", "Calculator"),
        ("java_method", "add"),
    ]


def test_parse_source_structure_with_tree_sitter_javascript_arrow_function():
    result = adapter.parse_source_structure(
        "class Cart { total(a, b) { return a + b; } }\nconst tax = (value) => value * 0.1;",
        "javascript",
        source_name="cart.js",
    )

    assert result.parser_available is True
    assert ("javascript_class", "Cart") in [(symbol.kind, symbol.name) for symbol in result.symbols]
    assert ("javascript_method", "total") in [(symbol.kind, symbol.name) for symbol in result.symbols]
    assert ("javascript_function", "tax") in [(symbol.kind, symbol.name) for symbol in result.symbols]


def test_parse_source_structure_reports_tree_sitter_syntax_errors():
    result = adapter.parse_source_structure("function ( {", "javascript", source_name="bad.js")

    assert result.parser_available is True
    assert "syntax errors" in result.syntax_error


def test_parse_source_structure_uses_java_heuristic_when_parser_missing(monkeypatch):
    monkeypatch.setattr(adapter, "_load_parser", lambda language: (None, ""))

    result = adapter.parse_source_structure(
        "public class Service {\n  public int total(int a, int b) { return a + b; }\n}",
        "java",
        source_name="Service.java",
    )

    assert result.parser_available is False
    assert result.parser_backend == "heuristic"
    assert ("java_class", "Service") in [(symbol.kind, symbol.name) for symbol in result.symbols]
    assert ("java_method", "total") in [(symbol.kind, symbol.name) for symbol in result.symbols]


def test_parse_source_structure_uses_javascript_heuristic_when_parser_missing(monkeypatch):
    monkeypatch.setattr(adapter, "_load_parser", lambda language: (None, ""))

    result = adapter.parse_source_structure(
        "class Cart { total(a, b) { return a + b; } }\nconst tax = value => value * 0.1;",
        "javascript",
        source_name="cart.js",
    )

    assert result.parser_available is False
    assert ("javascript_class", "Cart") in [(symbol.kind, symbol.name) for symbol in result.symbols]
    assert ("javascript_function", "tax") in [(symbol.kind, symbol.name) for symbol in result.symbols]
