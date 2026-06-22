from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from shutil import copy2
from typing import Any
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from testgen.core.config import BASE_DIR, OUTPUT_RUNS_PATH as DEFAULT_OUTPUT_RUNS_PATH
from testgen.core.logger import get_logger
from testgen.core.utils import extract_json_payload as _extract_json_payload

logger = get_logger(__name__)


# Backward-compatible alias for tests/monkeypatching.
OUTPUT_PATH = DEFAULT_OUTPUT_RUNS_PATH

TEST_CODE_DIR = "test_code"
TEST_PLAN_DIR = "test_plan"
REVIEW_REPORT_DIR = "review_report"
COVERAGE_REPORT_DIR = "coverage_report"
PDF_FONT_NAME = "AppUnicode"
FONT_DIR = BASE_DIR / "testgen" / "assets" / "fonts"
BUNDLED_PDF_FONT = FONT_DIR / "DejaVuSans.ttf"


_EXTENSIONS = {
    "pytest": ".py",
    "Selenium": ".py",
    "Playwright": ".py",
    "JUnit": ".java",
    "Jest": ".js",
    "Postman script": ".js",
}


def create_run_id() -> str:
    return f"run_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"


def _run_day_folder(run_id: str) -> str:
    match = re.search(r"(\d{8})", run_id)
    if not match:
        return datetime.now().strftime("%Y-%m-%d")

    compact = match.group(1)
    return f"{compact[0:4]}-{compact[4:6]}-{compact[6:8]}"


def _normalize_run_id(run_id: str | None) -> str:
    value = (run_id or "").strip() or create_run_id()
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._-")
    return cleaned or create_run_id()


def resolve_run_dir(run_id: str | None, ensure_exists: bool = True) -> Path:
    normalized_run_id = _normalize_run_id(run_id)
    run_dir = OUTPUT_PATH / _run_day_folder(normalized_run_id) / normalized_run_id
    if ensure_exists:
        run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _artifact_dir(run_id: str | None, artifact_type: str) -> Path:
    run_dir = resolve_run_dir(run_id, ensure_exists=True) / artifact_type
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def _slugify(text: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return cleaned.lower() or "artifact"



def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)

def parse_test_plan_rows(test_plan_json: str) -> list[dict[str, str]]:
    payload = _extract_json_payload(test_plan_json)
    if isinstance(payload, dict) and isinstance(payload.get("test_scenarios"), list):
        rows: list[dict[str, str]] = []
        for index, scenario in enumerate(payload["test_scenarios"], start=1):
            if isinstance(scenario, dict):
                rows.append(
                    {
                        "STT": str(index),
                        "Mã": _stringify(scenario.get("id")),
                        "Loại": _stringify(scenario.get("type")),
                        "Tiêu đề": _stringify(scenario.get("title")),
                        "Điều kiện tiên quyết": _stringify(scenario.get("preconditions")),
                        "Dữ liệu kiểm thử": _stringify(scenario.get("test_data")),
                        "Kết quả mong đợi": _stringify(scenario.get("expected_result")),
                        "Độ ưu tiên": _stringify(scenario.get("priority")),
                    }
                )
        if rows:
            return rows
    return [{"Kế hoạch kiểm thử thô": test_plan_json}]


def save_generated_code(code: str, framework: str, run_id: str | None = None) -> str:
    output_dir = _artifact_dir(run_id, TEST_CODE_DIR)
    extension = _EXTENSIONS.get(framework, ".txt")
    file_path = output_dir / f"ma_kiem_thu_{_slugify(framework)}_{_timestamp()}{extension}"
    file_path.write_text(code or "", encoding="utf-8")
    return str(file_path)


def save_combined_coverage_report(execution_summary: dict[str, Any], run_id: str | None = None) -> tuple[str, str, str]:
    output_dir = _artifact_dir(run_id, COVERAGE_REPORT_DIR)
    timestamp = _timestamp()
    report_path = output_dir / f"combined_coverage_{timestamp}.md"
    json_path = output_dir / f"combined_coverage_{timestamp}.json"
    raw_coverage_path = output_dir / f"coverage_raw_{timestamp}.json"

    combined = execution_summary.get("combined_report")
    if not isinstance(combined, dict):
        combined = {
            "passed": bool(execution_summary.get("passed", False)),
            "coverage_percent": float(execution_summary.get("coverage_percent", 0.0) or 0.0),
            "missing_lines": execution_summary.get("missing_lines", []),
            "coverage_path": execution_summary.get("coverage_path", ""),
            "test_paths": [execution_summary.get("test_path", "")],
            "output": execution_summary.get("output", ""),
        }

    json_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
    copied_raw_path = ""
    source_coverage_path = Path(str(combined.get("coverage_path", "") or ""))
    if source_coverage_path.exists() and source_coverage_path.is_file():
        copy2(source_coverage_path, raw_coverage_path)
        copied_raw_path = str(raw_coverage_path)

    missing_lines = combined.get("missing_lines", [])
    missing_count = len(missing_lines) if isinstance(missing_lines, list) else 0
    output_text = str(combined.get("output", "") or "").strip()
    if len(output_text) > 5000:
        output_text = output_text[:5000].rstrip() + "\n..."

    markdown = (
        "# Combined Coverage Report\n\n"
        f"- Pytest pass: {bool(combined.get('passed', False))}\n"
        f"- Coverage: {float(combined.get('coverage_percent', 0.0) or 0.0):.1f}%\n"
        f"- Missing lines: {missing_count}\n"
        f"- Coverage JSON: `{combined.get('coverage_path', '')}`\n\n"
        f"- Pytest log: `{combined.get('pytest_log_path', '')}`\n"
        f"- Collect-only log: `{combined.get('collection_log_path', '')}`\n\n"
        "## Test Files\n\n"
        + "\n".join(f"- `{path}`" for path in combined.get("test_paths", []) if path)
        + "\n\n## Pytest Output\n\n"
        "```text\n"
        f"{output_text}\n"
        "```\n"
    )
    report_path.write_text(markdown, encoding="utf-8")
    return str(report_path), str(json_path), copied_raw_path


def save_review_report(review: str, run_id: str | None = None) -> tuple[str, str]:
    output_dir = _artifact_dir(run_id, REVIEW_REPORT_DIR)
    timestamp = _timestamp()
    pdf_path = output_dir / f"bao_cao_phan_tich_{timestamp}.pdf"
    md_path = output_dir / f"bao_cao_phan_tich_{timestamp}.md"
    md_path.write_text(review or "", encoding="utf-8")
    _write_review_pdf(review or "", pdf_path)
    return str(pdf_path), str(md_path)


def _register_pdf_font() -> str:
    if PDF_FONT_NAME in pdfmetrics.getRegisteredFontNames():
        return PDF_FONT_NAME
    if BUNDLED_PDF_FONT.exists():
        try:
            pdfmetrics.registerFont(TTFont(PDF_FONT_NAME, str(BUNDLED_PDF_FONT)))
            return PDF_FONT_NAME
        except Exception:
            logger.exception("Khong the dang ky bundled PDF font: %s", BUNDLED_PDF_FONT)
    return "Helvetica"


def _markdown_to_plain_text(markdown_text: str) -> str:
    text = (markdown_text or "").replace("\r\n", "\n")
    lines: list[str] = []
    in_code_block = False
    for raw_line in text.split("\n"):
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        cleaned = raw_line
        if not in_code_block:
            cleaned = re.sub(r"^\s{0,3}#{1,6}\s*", "", cleaned)
            cleaned = re.sub(r"^\s*[-*+]\s+", "• ", cleaned)
            cleaned = cleaned.replace("**", "").replace("__", "").replace("`", "")
        lines.append(cleaned.rstrip())
    return "\n".join(lines).strip()


def _write_review_pdf(review_markdown: str, file_path: Path) -> None:
    font_name = _register_pdf_font()
    plain_text = _markdown_to_plain_text(review_markdown)

    pdf = canvas.Canvas(str(file_path), pagesize=A4)
    page_width, page_height = A4
    margin = 40
    text_width = page_width - (margin * 2)
    line_height = 15
    y = page_height - margin

    pdf.setFont(font_name, 14)
    pdf.drawString(margin, y, "Báo cáo rà soát test code")
    y -= line_height * 1.5

    pdf.setFont(font_name, 11)
    for line in plain_text.split("\n"):
        wrapped_lines = simpleSplit(line or " ", font_name, 11, text_width)
        if not wrapped_lines:
            wrapped_lines = [""]
        for wrapped in wrapped_lines:
            if y <= margin:
                pdf.showPage()
                y = page_height - margin
                pdf.setFont(font_name, 11)
            pdf.drawString(margin, y, wrapped)
            y -= line_height

    pdf.save()


def save_test_plan_excel(test_plan_json: str, run_id: str | None = None) -> str:
    output_dir = _artifact_dir(run_id, TEST_PLAN_DIR)
    file_path = output_dir / f"ke_hoach_kiem_thu_{_timestamp()}.xlsx"
    rows = parse_test_plan_rows(test_plan_json)
    dataframe = pd.DataFrame(rows)

    try:
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            dataframe.to_excel(writer, index=False, sheet_name="KeHoachKiemThu")
    except ImportError:
        _write_minimal_xlsx(file_path, rows)
    return str(file_path)


def _column_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def _xlsx_cell(reference: str, value: str) -> str:
    text = escape(value or "")
    return f'<c r="{reference}" t="inlineStr"><is><t>{text}</t></is></c>'


def _write_minimal_xlsx(file_path: Path, rows: list[dict[str, str]]) -> None:
    headers = list(rows[0].keys()) if rows else ["Kế hoạch kiểm thử"]
    sheet_rows = [headers, *[[row.get(header, "") for header in headers] for row in rows]]
    xml_rows: list[str] = []
    for row_index, row in enumerate(sheet_rows, start=1):
        cells = [
            _xlsx_cell(f"{_column_name(column_index)}{row_index}", str(value))
            for column_index, value in enumerate(row, start=1)
        ]
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    worksheet = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        "</worksheet>"
    )
    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="KeHoachKiemThu" sheetId="1" r:id="rId1"/></sheets>'
        "</workbook>"
    )
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        "</Relationships>"
    )
    package_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        "</Types>"
    )

    with ZipFile(file_path, "w", ZIP_DEFLATED) as workbook_zip:
        workbook_zip.writestr("[Content_Types].xml", content_types)
        workbook_zip.writestr("_rels/.rels", package_rels)
        workbook_zip.writestr("xl/workbook.xml", workbook)
        workbook_zip.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        workbook_zip.writestr("xl/worksheets/sheet1.xml", worksheet)

