from __future__ import annotations

import os
from pathlib import Path

import pytest

from testgen.agents import formatter_agent


def test_create_run_id():
    run_id = formatter_agent.create_run_id()
    assert run_id.startswith("run_")


def test_run_day_folder_with_valid_run_id():
    assert formatter_agent._run_day_folder("run_20231025_123456") == "2023-10-25"


def test_run_day_folder_with_invalid_run_id():
    # Should return today's date, just check it's a string of len 10
    assert len(formatter_agent._run_day_folder("invalid")) == 10


def test_normalize_run_id_clean():
    assert formatter_agent._normalize_run_id("run_123") == "run_123"


def test_normalize_run_id_dirty():
    assert formatter_agent._normalize_run_id("run_123!@#") == "run_123"


def test_resolve_run_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    run_dir = formatter_agent.resolve_run_dir("run_20231025_123456")
    assert run_dir.exists()
    assert "2023-10-25" in str(run_dir)
    assert "run_20231025_123456" in str(run_dir)


def test_artifact_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    art_dir = formatter_agent._artifact_dir("run_20231025_123456", "test_code")
    assert art_dir.exists()
    assert art_dir.name == "test_code"


def test_slugify():
    assert formatter_agent._slugify("C# Framework!") == "c_framework"
    assert formatter_agent._slugify("") == "artifact"


def test_stringify():
    assert formatter_agent._stringify(None) == ""
    assert formatter_agent._stringify("text") == "text"
    assert formatter_agent._stringify(123) == "123"
    assert formatter_agent._stringify({"a": 1}) == '{"a": 1}'


def test_parse_test_plan_rows_valid_json():
    json_str = '{"test_scenarios": [{"id": "TC-01", "type": "positive", "title": "test title"}]}'
    rows = formatter_agent.parse_test_plan_rows(json_str)
    assert len(rows) == 1
    assert rows[0]["Mã"] == "TC-01"
    assert rows[0]["Loại"] == "positive"
    assert rows[0]["Tiêu đề"] == "test title"


def test_parse_test_plan_rows_invalid_json():
    rows = formatter_agent.parse_test_plan_rows("not json")
    assert len(rows) == 1
    assert "Kế hoạch kiểm thử thô" in rows[0]
    assert rows[0]["Kế hoạch kiểm thử thô"] == "not json"


def test_save_generated_code(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    file_path = formatter_agent.save_generated_code("print('hello')", "pytest", "run_test")
    assert Path(file_path).exists()
    assert Path(file_path).suffix == ".py"
    assert Path(file_path).read_text(encoding="utf-8") == "print('hello')"


def test_save_combined_coverage_report_copies_raw_coverage(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    raw_coverage = tmp_path / "coverage.json"
    raw_coverage.write_text('{"files": {}}', encoding="utf-8")

    report_path, json_path, raw_path = formatter_agent.save_combined_coverage_report(
        {
            "combined_report": {
                "passed": True,
                "coverage_percent": 88.0,
                "missing_lines": [4],
                "coverage_path": str(raw_coverage),
                "test_paths": ["test_generated.py"],
                "output": "1 passed",
            }
        },
        "run_test",
    )

    assert Path(report_path).exists()
    assert Path(json_path).exists()
    assert Path(raw_path).exists()
    assert Path(raw_path).read_text(encoding="utf-8") == '{"files": {}}'


def test_save_review_report_writes_pdf_and_markdown(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    pdf_path, md_path = formatter_agent.save_review_report("# Review\nOK", "run_test")

    assert Path(pdf_path).exists()
    assert Path(pdf_path).suffix == ".pdf"
    assert Path(md_path).exists()
    assert Path(md_path).suffix == ".md"
    assert Path(md_path).read_text(encoding="utf-8") == "# Review\nOK"


def test_markdown_to_plain_text():
    md = """# Header
- List item
**Bold** text
```python
def x(): pass
```"""
    plain = formatter_agent._markdown_to_plain_text(md)
    assert "Header" in plain
    assert "• List item" in plain
    assert "Bold text" in plain
    assert "def x(): pass" in plain


def test_save_test_plan_excel_with_pandas(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    json_str = '{"test_scenarios": [{"id": "TC-01", "title": "test"}]}'
    file_path = formatter_agent.save_test_plan_excel(json_str, "run_test")
    assert Path(file_path).exists()
    assert Path(file_path).suffix == ".xlsx"


def test_save_test_plan_excel_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", tmp_path)
    
    import pandas as pd
    def raise_import_error(*args, **kwargs):
        raise ImportError("Mocked ImportError for openpyxl")
    monkeypatch.setattr(pd, "ExcelWriter", raise_import_error)
    
    json_str = '{"test_scenarios": [{"id": "TC-01", "title": "test"}]}'
    file_path = formatter_agent.save_test_plan_excel(json_str, "run_test")
    assert Path(file_path).exists()
    assert Path(file_path).suffix == ".xlsx"


def test_register_pdf_font_fallback(monkeypatch):
    monkeypatch.setattr(formatter_agent.pdfmetrics, "getRegisteredFontNames", lambda: [])
    monkeypatch.setattr(Path, "exists", lambda self: False)
    assert formatter_agent._register_pdf_font() == "Helvetica"


def test_register_pdf_font_uses_bundled_font(tmp_path, monkeypatch):
    font_path = tmp_path / "DejaVuSans.ttf"
    font_path.write_bytes(b"fake-font")
    registered = []

    monkeypatch.setattr(formatter_agent, "BUNDLED_PDF_FONT", font_path)
    monkeypatch.setattr(formatter_agent.pdfmetrics, "getRegisteredFontNames", lambda: [])
    monkeypatch.setattr(formatter_agent, "TTFont", lambda name, path: ("font", name, path))
    monkeypatch.setattr(formatter_agent.pdfmetrics, "registerFont", lambda font: registered.append(font))

    assert formatter_agent._register_pdf_font() == formatter_agent.PDF_FONT_NAME
    assert registered == [("font", formatter_agent.PDF_FONT_NAME, str(font_path))]
