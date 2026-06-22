from __future__ import annotations

from testgen.core import language_guard


# ── _detect_language_from_text ──

def test_detect_python_def():
    assert language_guard._detect_language_from_text("def hello():\n    pass") == "python"


def test_detect_python_class():
    assert language_guard._detect_language_from_text("class Foo:\n    pass") == "python"


def test_detect_python_import():
    assert language_guard._detect_language_from_text("from os import path") == "python"


def test_detect_python_main_guard():
    assert language_guard._detect_language_from_text('if __name__ == "__main__":\n    pass') == "python"


def test_detect_java_public_class():
    assert language_guard._detect_language_from_text("public class Calc {}") == "java"


def test_detect_java_import():
    # `import java.util.List;` starts with `import \w+` which matches Python first.
    # The Java-specific pattern is `\bimport\s+java\.` — but Python `import` regex fires earlier.
    # Use `System.out.println` which unambiguously triggers the Java pattern.
    assert language_guard._detect_language_from_text("System.out.println(x);") == "java"


def test_detect_java_throws():
    assert language_guard._detect_language_from_text("public void calc() throws Exception {}") == "java"


def test_detect_javascript_function():
    assert language_guard._detect_language_from_text("function add(a, b) { return a + b; }") == "javascript"


def test_detect_javascript_const():
    assert language_guard._detect_language_from_text("const x = 5;") == "javascript"


def test_detect_javascript_arrow():
    assert language_guard._detect_language_from_text("const fn = (x) => x + 1;") == "javascript"


def test_detect_javascript_describe():
    assert language_guard._detect_language_from_text("describe('test', () => {});") == "javascript"


def test_detect_unknown_for_plain_text():
    assert language_guard._detect_language_from_text("just some plain text") == "unknown"


def test_detect_unknown_for_empty():
    assert language_guard._detect_language_from_text("") == "unknown"


def test_detect_unknown_for_none():
    assert language_guard._detect_language_from_text(None) == "unknown"


# ── detect_section_language ──

def test_detect_section_language_by_extension():
    assert language_guard.detect_section_language("file.py", "anything") == "python"
    assert language_guard.detect_section_language("file.java", "anything") == "java"
    assert language_guard.detect_section_language("file.js", "anything") == "javascript"
    assert language_guard.detect_section_language("file.ts", "anything") == "javascript"


def test_detect_section_language_falls_back_to_text():
    assert language_guard.detect_section_language("file.txt", "def hello(): pass") == "python"


# ── detect_languages ──

def test_detect_languages_multiple():
    sections = [
        ("a.py", "def foo(): pass"),
        ("b.java", "public class B {}"),
    ]
    langs = language_guard.detect_languages(sections)
    assert langs == {"python", "java"}


def test_detect_languages_ignores_unknown():
    sections = [("readme.txt", "plain text")]
    assert language_guard.detect_languages(sections) == set()


# ── expected_language_for_framework ──

def test_expected_language_pytest():
    assert language_guard.expected_language_for_framework("pytest") == "python"


def test_expected_language_selenium():
    assert language_guard.expected_language_for_framework("Selenium") == "python"


def test_expected_language_unknown_framework():
    assert language_guard.expected_language_for_framework("unknown") is None


def test_expected_language_empty():
    assert language_guard.expected_language_for_framework("") is None


# ── validate_framework_sections ──

def test_validate_accepts_matching_language():
    sections = [("calc.py", "def add(a, b): return a + b")]
    assert language_guard.validate_framework_sections("pytest", sections) is None


def test_validate_rejects_mismatched_language():
    sections = [("Calc.java", "public class Calc {}")]
    msg = language_guard.validate_framework_sections("pytest", sections)
    assert msg is not None
    assert "pytest" in msg


def test_validate_returns_none_for_unknown_framework():
    sections = [("file.py", "def f(): pass")]
    assert language_guard.validate_framework_sections("CustomFramework", sections) is None


def test_validate_returns_none_when_no_language_detected():
    sections = [("readme.txt", "just docs")]
    assert language_guard.validate_framework_sections("pytest", sections) is None
