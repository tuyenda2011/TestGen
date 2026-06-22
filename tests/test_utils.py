from __future__ import annotations

from pathlib import Path

from testgen.core import utils


# --- normalize_text ---

def test_normalize_text_strips_whitespace():
    assert utils.normalize_text("  hello  ") == "hello"


def test_normalize_text_returns_empty_for_none():
    assert utils.normalize_text(None) == ""


def test_normalize_text_converts_non_string():
    assert utils.normalize_text(42) == "42"


# --- fix_json_trailing_commas ---

def test_fix_json_trailing_commas_removes_trailing_comma_before_brace():
    assert utils.fix_json_trailing_commas('{"a": 1,}') == '{"a": 1}'


def test_fix_json_trailing_commas_removes_trailing_comma_before_bracket():
    assert utils.fix_json_trailing_commas('[1, 2,]') == '[1, 2]'


def test_fix_json_trailing_commas_handles_clean_json():
    clean = '{"key": "value"}'
    assert utils.fix_json_trailing_commas(clean) == clean


# --- extract_json_payload ---

def test_extract_json_payload_parses_raw_json():
    result = utils.extract_json_payload('{"module": "auth"}')
    assert result == {"module": "auth"}


def test_extract_json_payload_strips_markdown_fence():
    result = utils.extract_json_payload('```json\n{"x": 1}\n```')
    assert result == {"x": 1}


def test_extract_json_payload_returns_none_for_empty():
    assert utils.extract_json_payload("") is None
    assert utils.extract_json_payload(None) is None


def test_extract_json_payload_extracts_from_surrounding_text():
    result = utils.extract_json_payload('Some text {"a": 2} more text')
    assert result == {"a": 2}


def test_extract_json_payload_fixes_trailing_comma():
    result = utils.extract_json_payload('{"a": 1,}')
    assert result == {"a": 1}


def test_extract_json_payload_returns_none_for_garbage():
    assert utils.extract_json_payload("not json at all") is None


# --- pretty_json_or_raw ---

def test_pretty_json_or_raw_formats_json():
    result = utils.pretty_json_or_raw('{"k": "v"}')
    assert '"k": "v"' in result
    # Indented output
    assert "\n" in result


def test_pretty_json_or_raw_returns_raw_for_non_json():
    assert utils.pretty_json_or_raw("  plain text  ") == "plain text"


# --- get_file_mime_from_extension ---

def test_get_file_mime_xlsx():
    assert "spreadsheet" in utils.get_file_mime_from_extension(Path("report.xlsx"))


def test_get_file_mime_pdf():
    assert utils.get_file_mime_from_extension(Path("doc.pdf")) == "application/pdf"


def test_get_file_mime_md():
    assert utils.get_file_mime_from_extension(Path("README.md")) == "text/markdown"


def test_get_file_mime_unknown_defaults_to_text():
    assert utils.get_file_mime_from_extension(Path("data.csv")) == "text/plain"


# --- get_code_language ---

def test_get_code_language_pytest():
    assert utils.get_code_language("pytest") == "python"


def test_get_code_language_junit():
    assert utils.get_code_language("JUnit") == "java"


def test_get_code_language_jest():
    assert utils.get_code_language("Jest") == "javascript"


def test_get_code_language_postman():
    assert utils.get_code_language("Postman script") == "javascript"


def test_get_code_language_unknown():
    assert utils.get_code_language("unknown_framework") == "text"
