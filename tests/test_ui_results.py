from __future__ import annotations

from testgen.core.constants import GENERATE_WORKFLOW
from testgen.ui import results
from testgen.ui.results import (
    build_artifact_link_rows,
    build_quality_assessment,
    build_review_group_summary,
    format_action_items_for_copy,
    parse_review_report_sections,
    severity_badge_html,
)


def test_quality_assessment_marks_passed_high_coverage_as_ok():
    assessment = build_quality_assessment(
        {
            "diagnostics": {
                "pytest_passed": True,
                "pytest_coverage_percent": 92.0,
                "pytest_combined_coverage_percent": 92.0,
                "pytest_attempts": 1,
            },
            "execution_summary": {"missing_lines": []},
        }
    )

    assert assessment["verdict"] == "Đạt"
    assert assessment["score"] >= 80


def test_quality_assessment_marks_collection_error_as_high_risk():
    assessment = build_quality_assessment(
        {
            "diagnostics": {
                "pytest_passed": False,
                "pytest_coverage_percent": 0.0,
                "pytest_attempts": 1,
                "pytest_execution_issue_type": "collection_error",
            },
            "execution_summary": {"missing_lines": [1, 2]},
        }
    )

    assert assessment["verdict"] == "Rủi ro cao"
    assert assessment["score"] < 50
    assert assessment["action_items"]


def test_quality_assessment_external_framework_marks_coverage_na():
    assessment = build_quality_assessment(
        {
            "framework": "Jest",
            "diagnostics": {
                "test_execution_framework": "Jest",
                "external_execution_passed": True,
                "external_attempts": 1,
                "external_coverage_percent": 0.0,
                "external_coverage_available": False,
                "external_coverage_status": "artifact_missing",
                "external_retry_supported": False,
            },
            "execution_summary": {
                "passed": True,
                "coverage_percent": 0.0,
                "coverage_available": False,
                "coverage_status": "artifact_missing",
            },
        }
    )

    assert assessment["verdict"] == "Đạt"
    assert assessment["coverage_label"] == "N/A"
    assert any("Retry tự động" in item for item in assessment["action_items"])
    assert any("0.0 không có nghĩa" in item for item in assessment["action_items"])


def _section_items(report: str) -> dict[str, list[str]]:
    return {
        str(section["key"]): list(section["items"])
        for section in parse_review_report_sections(report)
    }


def test_parse_review_report_sections_from_expected_headings():
    items = _section_items(
        """
## Lỗi nghiêm trọng
- Import sai target `Calculator`.

## Test còn thiếu
- Thiếu boundary case cho số âm.

## Assertion yếu
- Test chỉ print kết quả, không assert.

## Rủi ro maintainability
- Phụ thuộc network nên dễ flaky.

## Gợi ý sửa ngay
- Sửa import và bổ sung boundary test.
"""
    )

    assert items["critical"] == ["Import sai target `Calculator`."]
    assert items["missing_tests"] == ["Thiếu boundary case cho số âm."]
    assert items["weak_assertions"] == ["Test chỉ print kết quả, không assert."]
    assert items["maintainability"] == ["Phụ thuộc network nên dễ flaky."]
    assert items["fixes"] == ["Sửa import và bổ sung boundary test."]


def test_parse_review_report_sections_from_loose_bullets():
    items = _section_items(
        """
- Critical: test không chạy do import sai.
- Thiếu negative case khi input rỗng.
- Assertion yếu vì assert True.
- Minor: mock quá mức làm test khó bảo trì.
- Gợi ý: sửa import trước.
"""
    )

    assert items["critical"]
    assert items["missing_tests"]
    assert items["weak_assertions"]
    assert items["maintainability"]
    assert items["fixes"]


def test_parse_review_report_sections_ignores_no_issue_placeholders():
    items = _section_items(
        """
## Lỗi nghiêm trọng
- Không phát hiện.

## Gợi ý sửa ngay
- Không cần sửa ngay.
"""
    )

    assert items["critical"] == []
    assert items["fixes"] == []


def test_action_items_copy_block_uses_markdown_bullets():
    text = format_action_items_for_copy(["Fix import", "Add boundary test"])

    assert text == "- Fix import\n- Add boundary test"


def test_review_group_summary_includes_severity_for_each_group():
    sections = parse_review_report_sections(
        """
## Critical
- Import sai.
"""
    )
    rows = build_review_group_summary(sections)

    assert len(rows) == 5
    assert rows[0]["Severity"] == "High"
    assert rows[0]["Items"] == 1
    assert "High" in severity_badge_html("High")


def test_build_artifact_link_rows_prefers_log_paths_and_coverage_artifacts(tmp_path):
    pytest_log = tmp_path / "pytest.log"
    collect_log = tmp_path / "pytest_collect_only.log"
    coverage_report = tmp_path / "coverage.md"
    for path in [pytest_log, collect_log, coverage_report]:
        path.write_text("ok", encoding="utf-8")

    rows = build_artifact_link_rows(
        {
            "pytest_log_path": str(pytest_log),
            "collection_log_path": str(collect_log),
            "coverage_report_path": str(coverage_report),
            "execution_summary": {"output": "1 passed", "collection_output": "collected"},
        }
    )

    lookup = {row["Artifact"]: row for row in rows}
    assert lookup["Pytest log"]["Status"] == "File"
    assert lookup["Collect-only log"]["Path"] == str(collect_log)
    assert lookup["Coverage report"]["Path"] == str(coverage_report)


class _FakeStreamlit:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def columns(self, count):
        return [self for _ in range(count)]

    def tabs(self, labels):
        return [self for _ in labels]

    def expander(self, *args, **kwargs):
        return self

    def metric(self, *args, **kwargs):
        return None

    def dataframe(self, *args, **kwargs):
        return None

    def info(self, *args, **kwargs):
        return None

    def markdown(self, *args, **kwargs):
        return None

    def subheader(self, *args, **kwargs):
        return None

    def code(self, *args, **kwargs):
        return None

    def caption(self, *args, **kwargs):
        return None

    def write(self, *args, **kwargs):
        return None

    def json(self, *args, **kwargs):
        return None

    def download_button(self, *args, **kwargs):
        return None


def test_render_results_smoke_with_diagnostics(monkeypatch):
    monkeypatch.setattr(results, "st", _FakeStreamlit())

    results.render_results(
        {
            "mode": "CLI / Ollama",
            "workflow_label": "Sinh mã kiểm thử",
            "framework": "pytest",
            "test_technique": "Hybrid",
            "backend": "ollama",
            "embedding_backend": "ollama",
            "docs_context": "doc ctx",
            "source_context": "source ctx",
            "context": "merged ctx",
            "progress": [{"step": "1", "agent": "Input", "model": "rule", "status": "OK", "result": "done"}],
            "diagnostics": {
                "llm_calls_estimated": 3,
                "rag_reused_collections": 1,
                "docs_chunks_indexed": 2,
                "source_chunks_indexed": 0,
                "stage_timings_ms": {"input": 1.0, "review": 2.0},
                "stage_bottleneck": {"stage": "review", "elapsed_ms": 2.0},
                "retry_summary": {"pytest_attempts": 1, "retry_modes": ["initial"]},
                "models_used": {"requirement": "qwen", "planning": "llama"},
                "rag_retrieval": {
                    "docs": {
                        "sources": [
                            {
                                "rank": 1,
                                "source_name": "docs.md",
                                "section": "Intro",
                                "chunk_type": "markdown_section",
                            }
                        ]
                    },
                    "source": {"skipped_reason": "pytest_ast_context"},
                },
                "pytest_passed": True,
                "pytest_coverage_percent": 91.0,
                "pytest_combined_coverage_percent": 91.0,
                "pytest_attempts": 1,
            },
            "execution_summary": {
                "passed": True,
                "coverage_percent": 91.0,
                "missing_lines": [],
                "execution_issue": {"type": "", "title": ""},
                "output": "ok",
                "collection_output": "collected",
                "combined_report": {"coverage_percent": 91.0, "passed": True, "missing_lines": []},
            },
            "generated_code": "def test_ok():\n    assert True",
            "test_case_rows": [{"id": "TC-001", "title": "ok"}],
            "test_plan_json": '{"test_scenarios": []}',
            "requirement_json": '{"module": "calc"}',
            "review_target_label": "Mã kiểm thử đã sinh",
            "review_target_code": "def test_ok(): pass",
            "review_report": "## Review\nOK",
        },
        GENERATE_WORKFLOW,
        "pytest",
        "Hybrid",
    )
