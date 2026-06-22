import re
import unicodedata
from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st
from testgen.core.config import PYTEST_COVERAGE_THRESHOLD
from testgen.core.constants import (
    GENERATE_WORKFLOW,
    REVIEW_WORKFLOW,
    workflow_label,
)
from testgen.core.utils import normalize_text
from testgen.ui.styles import verdict_badge_html as _verdict_badge_html, pillar_bar_html as _pillar_bar_html


_REVIEW_GROUPS = [
    {
        "key": "critical",
        "label": "Lỗi nghiêm trọng",
        "severity": "High",
        "heading_terms": ["loi nghiem trong", "critical", "major"],
        "line_terms": [
            "critical",
            "major",
            "syntax",
            "import",
            "name error",
            "khong chay",
            "b ia",
            "bia",
            "sai target",
            "expected value",
            "sai ky vong",
        ],
    },
    {
        "key": "missing_tests",
        "label": "Test còn thiếu",
        "severity": "Medium",
        "heading_terms": ["test con thieu", "ca kiem thu con thieu", "missing test", "coverage thieu"],
        "line_terms": ["thieu negative", "thieu boundary", "boundary", "exception", "security", "missing test", "chua cover"],
    },
    {
        "key": "weak_assertions",
        "label": "Assertion yếu",
        "severity": "Medium",
        "heading_terms": ["assertion yeu", "assert yeu", "weak assertion", "thieu assert"],
        "line_terms": ["assertion yeu", "assert yeu", "assert true", "thieu assert", "chi print", "print log", "khong assert"],
    },
    {
        "key": "maintainability",
        "label": "Rủi ro maintainability",
        "severity": "Low",
        "heading_terms": ["maintainability", "bao tri", "rui ro maintainability", "rui ro bao tri", "minor"],
        "line_terms": ["maintainability", "bao tri", "flaky", "network", "file system", "thoi gian", "trang thai ngoai", "mock sai", "dependency", "minor"],
    },
    {
        "key": "fixes",
        "label": "Gợi ý sửa ngay",
        "severity": "Action",
        "heading_terms": ["goi y sua", "sua ngay", "de xuat", "de xuat chinh sua", "recommendation", "fix"],
        "line_terms": ["goi y", "sua ngay", "de xuat", "recommend", "fix"],
    },
]


def _normalize_for_match(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text or "")
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    without_marks = without_marks.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-zA-Z0-9]+", " ", without_marks).lower().strip()


def _clean_review_line(line: str) -> str:
    cleaned = re.sub(r"^\s{0,3}#{1,6}\s*", "", line or "").strip()
    cleaned = re.sub(r"^\s*[-*+]\s+", "", cleaned)
    cleaned = re.sub(r"^\s*\d+[.)]\s+", "", cleaned)
    cleaned = cleaned.strip().strip("*`:_ ")
    return cleaned.strip()


def _is_review_heading(line: str) -> bool:
    stripped = (line or "").strip()
    if not stripped:
        return False
    if re.match(r"^#{1,6}\s+", stripped):
        return True
    if re.match(r"^\*\*[^*]{1,80}:?\*\*$", stripped):
        return True
    return not stripped.startswith(("-", "*", "+")) and stripped.endswith(":") and len(stripped) <= 90


def _review_group_key(text: str, *, heading: bool) -> str | None:
    normalized = _normalize_for_match(text)
    if not normalized:
        return None
    if heading and any(term in normalized for term in ("tom tat", "ket luan")):
        return None
    if heading and "van de phat hien" in normalized and "critical" in normalized and "major" in normalized:
        return None
    if not heading and normalized.startswith(("goi y", "de xuat", "sua ngay", "recommend", "fix")):
        return "fixes"

    field = "heading_terms" if heading else "line_terms"
    for group in _REVIEW_GROUPS:
        if any(term in normalized for term in group[field]):
            return str(group["key"])
    return None


def _is_empty_review_item(text: str) -> bool:
    normalized = _normalize_for_match(text)
    return normalized.startswith("khong phat hien") or normalized.startswith("khong can sua") or normalized in {
        "none",
        "n a",
        "khong co",
    }


def parse_review_report_sections(report: str) -> list[dict[str, object]]:
    grouped: dict[str, list[str]] = {str(group["key"]): [] for group in _REVIEW_GROUPS}
    current_group: str | None = None

    in_code_block = False

    for raw_line in (report or "").splitlines():
        if raw_line.strip().startswith("```"):
            in_code_block = not in_code_block
            if current_group:
                if grouped[current_group]:
                    grouped[current_group][-1] += "\n" + raw_line
                else:
                    grouped[current_group].append(raw_line)
            continue
            
        if in_code_block:
            if current_group:
                if grouped[current_group]:
                    grouped[current_group][-1] += "\n" + raw_line
                else:
                    grouped[current_group].append(raw_line)
            continue

        cleaned = _clean_review_line(raw_line)
        if not cleaned:
            continue

        if _is_review_heading(raw_line):
            current_group = _review_group_key(cleaned, heading=True)
            continue

        target_group = current_group or _review_group_key(cleaned, heading=False)
        if not target_group:
            continue
        if _is_empty_review_item(cleaned):
            continue

        items = grouped[target_group]
        if not any(it == cleaned or it.startswith(cleaned + "\n") for it in items):
            items.append(cleaned)

    return [
        {
            "key": group["key"],
            "label": group["label"],
            "severity": group["severity"],
            "items": grouped[str(group["key"])],
        }
        for group in _REVIEW_GROUPS
    ]

def _code_language(framework: str) -> str:
    mapping = {
        "pytest": "python",
        "Selenium": "python",
        "Playwright": "python",
        "JUnit": "java",
        "Jest": "javascript",
        "Postman script": "javascript",
    }
    return mapping.get(framework, "text")


def _safe_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_quality_assessment(result: dict) -> dict[str, object]:
    diagnostics = result.get("diagnostics", {}) if isinstance(result, dict) else {}
    diagnostics = diagnostics if isinstance(diagnostics, dict) else {}
    execution_summary = result.get("execution_summary", {}) if isinstance(result, dict) else {}
    execution_summary = execution_summary if isinstance(execution_summary, dict) else {}
    execution_framework = str(diagnostics.get("test_execution_framework") or result.get("framework") or "")
    is_external = bool(execution_framework and execution_framework != "pytest" and "external_execution_passed" in diagnostics)

    if is_external:
        coverage_available = bool(
            diagnostics.get("external_coverage_available", execution_summary.get("coverage_available", False))
        )
        coverage_status = str(
            diagnostics.get("external_coverage_status", execution_summary.get("coverage_status", "")) or ""
        )
        coverage = (
            _safe_float(
                diagnostics.get("external_coverage_percent", execution_summary.get("coverage_percent")),
                0.0,
            )
            if coverage_available
            else 0.0
        )
        passed = bool(diagnostics.get("external_execution_passed", execution_summary.get("passed", False)))
        attempts = int(diagnostics.get("external_attempts", 1 if execution_summary else 0) or 0)
        issue_type = str(diagnostics.get("external_execution_issue_type", "") or "")
        retry_supported = bool(diagnostics.get("external_retry_supported", execution_summary.get("retry_supported", False)))

        action_items: list[str] = []
        if not passed:
            action_items.append(f"Xem log/diagnostics của {execution_framework} executor trước khi dùng test.")
        if not coverage_available:
            action_items.append(
                f"Coverage không khả dụng cho {execution_framework}; 0.0 không có nghĩa là source thật sự cover 0%."
            )
        if not retry_supported:
            action_items.append("Retry tự động theo missing lines hiện chỉ hỗ trợ pytest/Python.")
        if not action_items:
            action_items.append("Không có hành động bắt buộc từ execution diagnostics.")

        verdict = "Đạt" if passed else "Cần xem log"
        score = 75 if passed else 45
        if coverage_available:
            score += min(20, int(max(0.0, coverage) * 0.2))
        elif passed:
            score += 5

        return {
            "verdict": verdict,
            "score": max(0, min(100, score)),
            "coverage": coverage,
            "coverage_available": coverage_available,
            "coverage_label": f"{coverage:.1f}%" if coverage_available else "N/A",
            "passed": passed,
            "attempts": attempts,
            "issue_type": issue_type,
            "missing_count": 0,
            "action_items": action_items,
        }

    coverage = _safe_float(
        execution_summary.get("coverage_percent"),
        _safe_float(diagnostics.get("pytest_combined_coverage_percent") or diagnostics.get("pytest_coverage_percent"), 0.0),
    )
    passed = bool(diagnostics.get("pytest_passed", execution_summary.get("passed", False)))
    attempts = int(diagnostics.get("pytest_attempts") or diagnostics.get("attempts", 0))
    issue_type = str(diagnostics.get("pytest_execution_issue_type", "") or "")
    missing_lines = execution_summary.get("missing_lines", [])
    missing_count = len(missing_lines) if isinstance(missing_lines, list) else 0

    action_items: list[str] = []
    if issue_type in {"syntax_error", "import_error", "collection_error"}:
        action_items.append("Sửa lỗi syntax/import/collection trước khi đánh giá coverage.")
    if not passed and attempts:
        action_items.append("Ưu tiên xem log pytest và failure summary vì test vẫn chưa pass.")
    if coverage < PYTEST_COVERAGE_THRESHOLD and attempts:
        action_items.append(
            f"Bổ sung test cho missing lines để đạt coverage {PYTEST_COVERAGE_THRESHOLD:.0f}%."
        )
    if missing_count:
        lines_str = ", ".join(map(str, missing_lines))
        if len(lines_str) <= 60:
            action_items.append(f"Còn {missing_count} dòng source chưa được cover (Dòng: {lines_str}).")
            missing_lines = []
        else:
            action_items.append(f"Còn {missing_count} dòng source chưa được cover.")
    if int(diagnostics.get("pytest_targeted_retries", 0) or 0):
        action_items.append("Kiểm tra các test retry theo function để tránh trùng hoặc assertion yếu.")
    if not action_items:
        action_items.append("Không có hành động bắt buộc từ execution diagnostics.")

    if issue_type in {"syntax_error", "import_error", "collection_error"} or (attempts and not passed):
        verdict = "Rủi ro cao"
    elif attempts and coverage < PYTEST_COVERAGE_THRESHOLD:
        verdict = "Cần sửa"
    elif attempts:
        verdict = "Đạt"
    else:
        verdict = "Cần xem review"

    score = 0
    if attempts:
        score += 35 if passed else 0
        score += min(45, int(max(0.0, coverage) * 0.45))
        if not issue_type:
            score += 10
        score += max(0, 10 - min(missing_count, 10))
    else:
        score = 50 if result.get("review_report") else 0

    if verdict == "Rủi ro cao":
        score = min(score, 49)
    elif verdict == "Cần sửa":
        score = min(score, 79)

    return {
        "verdict": verdict,
        "score": max(0, min(100, score)),
        "coverage": coverage,
        "coverage_available": True,
        "coverage_label": f"{coverage:.1f}%",
        "passed": passed,
        "attempts": attempts,
        "issue_type": issue_type,
        "missing_count": missing_count,
        "missing_lines": missing_lines,
        "action_items": action_items,
    }


def format_action_items_for_copy(action_items: list[object]) -> str:
    cleaned = [str(item).strip() for item in action_items if str(item or "").strip()]
    return "\n".join(f"- {item}" for item in cleaned)


def build_review_group_summary(sections: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for section in sections:
        items = section.get("items", [])
        count = len(items) if isinstance(items, list) else 0
        severity = str(section.get("severity", "") or "Info")
        rows.append(
            {
                "Group": str(section.get("label", "")),
                "Severity": severity,
                "Items": count,
                "Status": "Action needed" if count else "Clear",
            }
        )
    return rows


def build_review_agent_rows(result: dict) -> list[dict[str, object]]:
    post_review = result.get("post_review_quality", {})
    post_review = post_review if isinstance(post_review, dict) else {}
    findings = post_review.get("review_findings", {})
    findings = findings if isinstance(findings, dict) else {}

    rows: list[dict[str, object]] = []

    def add_rows(group: str, severity: str, items: object, status: str) -> None:
        if not isinstance(items, list):
            return
        for item in items:
            text = str(item or "").strip()
            if text:
                rows.append(
                    {
                        "Nguồn": "Review Agent",
                        "Nhóm": group,
                        "Mức": severity,
                        "Trạng thái": status,
                        "Nội dung": text,
                    }
                )

    add_rows("Blocking", "High", post_review.get("blocking_findings", []), "Cần xử lý")
    add_rows("Khuyến nghị", "Action", post_review.get("recommended_action", []), "Đề xuất")

    group_meta = {
        "critical": ("Lỗi nghiêm trọng", "High"),
        "missing_tests": ("Test còn thiếu", "Medium"),
        "weak_assertions": ("Assertion yếu", "Medium"),
        "requirement": ("Sai yêu cầu", "High"),
        "maintainability": ("Maintainability", "Low"),
        "fixes": ("Gợi ý sửa", "Action"),
        "ignored_missing_tests": ("Đã bỏ qua hợp lệ", "Info"),
    }
    for key, (label, severity) in group_meta.items():
        status = "Đã bỏ qua" if key == "ignored_missing_tests" else "Phát hiện"
        add_rows(label, severity, findings.get(key, []), status)

    return rows


def severity_badge_html(severity: str) -> str:
    palette = {
        "High": ("#7f1d1d", "#fee2e2", "#fecaca"),
        "Medium": ("#7c2d12", "#ffedd5", "#fed7aa"),
        "Low": ("#1f2937", "#f3f4f6", "#d1d5db"),
        "Action": ("#064e3b", "#d1fae5", "#a7f3d0"),
    }
    text_color, bg_color, border_color = palette.get(severity, ("#1f2937", "#f3f4f6", "#d1d5db"))
    safe_severity = escape(severity or "Info")
    return (
        "<span style=\"display:inline-block;border-radius:999px;"
        f"border:1px solid {border_color};background:{bg_color};color:{text_color};"
        "padding:0.12rem 0.5rem;font-size:0.78rem;font-weight:700;\">"
        f"{safe_severity}</span>"
    )


def _nested_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _first_text(*values: object) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def _artifact_status(path: str, *, has_inline_text: bool = False) -> str:
    if path.startswith("#"):
        return "Inline"
    if path and Path(path).exists():
        return "File"
    if has_inline_text:
        return "Inline"
    return "Missing"


def build_artifact_link_rows(result: dict) -> list[dict[str, str]]:
    execution_summary = _nested_dict(result.get("execution_summary") if isinstance(result, dict) else {})
    combined_report = _nested_dict(execution_summary.get("combined_report"))
    pytest_log_path = _first_text(
        result.get("pytest_log_path"),
        execution_summary.get("pytest_log_path"),
        combined_report.get("pytest_log_path"),
    )
    collection_log_path = _first_text(
        result.get("collection_log_path"),
        execution_summary.get("collection_log_path"),
        combined_report.get("collection_log_path"),
    )
    pytest_output = str(execution_summary.get("output", "") or "").strip()
    collection_output = str(execution_summary.get("collection_output", "") or "").strip()

    rows = [
        {
            "Artifact": "Pytest log",
            "Status": _artifact_status(pytest_log_path, has_inline_text=bool(pytest_output)),
            "Path": pytest_log_path or ("#pytest-log" if pytest_output else ""),
        },
        {
            "Artifact": "Collect-only log",
            "Status": _artifact_status(collection_log_path, has_inline_text=bool(collection_output)),
            "Path": collection_log_path or ("#collect-only-log" if collection_output else ""),
        },
        {
            "Artifact": "Coverage report",
            "Status": _artifact_status(str(result.get("coverage_report_path", "") or "")),
            "Path": str(result.get("coverage_report_path", "") or ""),
        },
        {
            "Artifact": "Coverage JSON",
            "Status": _artifact_status(str(result.get("coverage_json_path", "") or "")),
            "Path": str(result.get("coverage_json_path", "") or ""),
        },
        {
            "Artifact": "Raw coverage JSON",
            "Status": _artifact_status(
                _first_text(result.get("coverage_raw_path"), execution_summary.get("coverage_path"))
            ),
            "Path": _first_text(result.get("coverage_raw_path"), execution_summary.get("coverage_path")),
        },
    ]
    return [row for row in rows if row["Path"] or row["Status"] != "Missing"]


def render_results(result: dict, workflow_mode: str, framework: str, test_technique: str) -> None:
    if not result or workflow_mode not in {GENERATE_WORKFLOW, REVIEW_WORKFLOW}:
        return

    summary_cols = st.columns(4)
    summary_cols[0].metric("Chế độ chạy", result.get("mode", ""))
    summary_cols[1].metric("Luồng chạy", result.get("workflow_label", workflow_label(workflow_mode)))
    summary_cols[2].metric("Framework kiểm thử", result.get("framework", framework))
    summary_cols[3].metric("Kỹ thuật", result.get("test_technique", test_technique))

    tab_overview, tab_artifacts, tab_review, tab_context, tab_exports = st.tabs(
        [
            "Tổng quan",
            "Kết quả chính",
            "Rà soát",
            "Ngữ cảnh & Yêu cầu",
            "Tải xuống",
        ]
    )

    with tab_overview:
        assessment = build_quality_assessment(result)
        verdict = str(assessment.get("verdict", ""))
        score = int(assessment.get("score", 0) or 0)
        action_items = assessment.get("action_items", [])
        coverage_label = str(
            assessment.get("coverage_label")
            or f"{float(assessment.get('coverage', 0.0) or 0.0):.1f}%"
        )

        # ── Hàng 1: Verdict badge + các metric chính ──
        try:
            from testgen.core.post_review_quality import assess_post_review_quality
            prq = assess_post_review_quality(
                framework=str(result.get("framework", framework)),
                execution_summary=result.get("execution_summary", {}) if isinstance(result.get("execution_summary"), dict) else {},
                review_report=str(result.get("review_report") or ""),
                generated_code=str(result.get("generated_code") or ""),
                diagnostics=result.get("diagnostics", {}) if isinstance(result.get("diagnostics"), dict) else {}
            )
            if isinstance(result, dict):
                result["post_review_quality"] = prq
        except Exception:
            prq = result.get("post_review_quality") if isinstance(result, dict) else None
        
        # Ghi đè verdict từ PRQ nếu có, vì PRQ là thang điểm chuẩn mới
        if isinstance(prq, dict) and "verdict" in prq:
            verdict = str(prq["verdict"])
            
        st.markdown(_verdict_badge_html(verdict), unsafe_allow_html=True)
        
        display_score = int(prq.get("score", score)) if isinstance(prq, dict) and "score" in prq else score
        
        score_cols = st.columns(4)
        score_cols[0].metric("🎯 Quality Score", f"{display_score}/100")
        score_cols[1].metric("📊 Coverage", coverage_label)
        
        loop_attempt = int(
            (prq.get("loop_attempt") if isinstance(prq, dict) else None)
            or result.get("diagnostics", {}).get("review_loop_attempt", 1)
            or 1
        )
        score_cols[2].metric("🔄 Vòng lặp tự sửa", f"{loop_attempt}/3")
        attempts = int(assessment.get("attempts", 0) or 0)
        score_cols[3].metric("⚙️ Execution attempts", str(attempts) if attempts else "N/A")

        # ── Score Breakdown + Pillar bars ──
        if isinstance(prq, dict) and prq:
            exec_score  = int(prq.get("execution_score", 0) or 0)
            cov_score   = int(prq.get("coverage_score", 0) or 0)
            rev_score   = int(prq.get("review_score", 0) or 0)
            asrt_score  = int(prq.get("assertion_quality_score", 0) or 0)
            req_score   = int(prq.get("requirement_alignment_score", 0) or 0)
            maint_score = int(prq.get("maintainability_score", 0) or 0)
            art_score   = int(prq.get("artifact_score", 0) or 0)
            flow_score  = int(prq.get("flow_or_api_assertion_score", 0) or 0)
            is_e2e = str(prq.get("framework", "")) in {"Selenium", "Playwright", "Postman script"}

            maint_mx = 10 if is_e2e else 5
            pillars: list[tuple[str, int, int]] = [
                ("Execution (pass/fail)", exec_score, 30),
            ]
            if is_e2e:
                pillars.append(("Flow / API Assertion", flow_score, 25))
            else:
                pillars.append(("Coverage (pytest-cov/JaCoCo)", cov_score, 25))
            
            pillars += [
                ("Review Agent (findings)", rev_score, 20),
                ("Assertion Quality", asrt_score, 10),
                ("Requirement Alignment", req_score, 10),
                ("Maintainability", maint_score, maint_mx),
            ]
            if is_e2e:
                pillars.append(("Artifact (Bonus)", art_score, 0))

            with st.expander("📊 Score Breakdown – điểm từng Pillar", expanded=True):
                left_col, right_col = st.columns([1, 1])
                with left_col:
                    bars_html = "".join(
                        _pillar_bar_html(label, pts, mx if mx > 0 else 5) for label, pts, mx in pillars
                    )
                    total_pts = sum(p[1] for p in pillars)
                    total_mx  = 100
                    actual_score = int(prq.get("score", total_pts)) if "score" in prq else min(100, total_pts)
                    
                    bars_html += _pillar_bar_html("Tổng (Đã chặn trần 100)", actual_score, total_mx)
                    st.markdown(bars_html, unsafe_allow_html=True)
                with right_col:
                    breakdown_rows = [
                        {"🏳️ Pillar": label, "Điểm": pts, "Tối đa": mx if mx > 0 else "Bonus",
                         "%": f"{int(pts/mx*100)}%" if mx > 0 else ("100%" if pts > 0 else "0%")}
                        for label, pts, mx in pillars
                    ]
                    breakdown_rows.append({
                        "🏳️ Pillar": "─ Tổng (Đã chặn trần 100)",
                        "Điểm": actual_score,
                        "Tối đa": total_mx,
                        "%": f"{int(actual_score/total_mx*100) if total_mx else 0}%",
                    })
                    st.dataframe(
                        pd.DataFrame(breakdown_rows),
                        use_container_width=True,
                        hide_index=True,
                    )

                blocking = prq.get("blocking_findings", [])
                if blocking:
                    st.error("⛔ Vấn đề chặn xuất kết quả:\n\n" + "\n".join(f"- {b}" for b in blocking[:5]))
                recommended = prq.get("recommended_action", [])
                if recommended and not blocking:
                    st.info("💡 Gợi ý cải thiện:\n\n" + "\n".join(f"- {r}" for r in recommended[:4]))

        # ── Bảng tiến trình Pipeline ──
        progress = result.get("progress", [])
        if isinstance(progress, list) and progress:
            st.markdown("##### 📌 Tiến trình Pipeline")
            progress_frame = pd.DataFrame(
                [
                    {
                        "Bước": item.get("step", ""),
                        "Agent": item.get("agent", ""),
                        "Model": item.get("model", ""),
                        "Trạng thái": item.get("status", ""),
                        "Kết quả": item.get("result", ""),
                    }
                    for item in progress
                ]
            )
            st.dataframe(progress_frame, use_container_width=True, hide_index=True)
        else:
            st.info("Chưa có dữ liệu tiến trình.")
        info_cols = st.columns(4)
        info_cols[0].metric("Backend", str(result.get("backend", "")).upper())
        info_cols[1].metric("Embedding", str(result.get("embedding_backend", "")).upper())
        info_cols[2].metric("Ngữ cảnh tài liệu", f"{len(normalize_text(str(result.get('docs_context') or ''))):,} ký tự")
        info_cols[3].metric("Ngữ cảnh source", f"{len(normalize_text(str(result.get('source_context') or ''))):,} ký tự")
        diagnostics = result.get("diagnostics", {})
        if isinstance(diagnostics, dict) and diagnostics:
            diag_cols = st.columns(4)
            diag_cols[0].metric("LLM calls", str(diagnostics.get("llm_calls_estimated", 0)))
            diag_cols[1].metric("RAG reused", str(diagnostics.get("rag_reused_collections", 0)))
            diag_cols[2].metric("Docs chunks mới", str(diagnostics.get("docs_chunks_indexed", 0)))
            diag_cols[3].metric("Source chunks mới", str(diagnostics.get("source_chunks_indexed", 0)))
            stage_timings = diagnostics.get("stage_timings_ms")
            bottleneck = diagnostics.get("stage_bottleneck")
            retry_summary = diagnostics.get("retry_summary")
            models_used = diagnostics.get("models_used")
            rag_retrieval = diagnostics.get("rag_retrieval")

            if any([stage_timings, bottleneck, retry_summary, models_used, rag_retrieval]):
                with st.expander("Advanced Diagnostics (Dành cho Debug)", expanded=False):
                    if isinstance(stage_timings, dict) and stage_timings:
                        st.markdown("##### Thời gian từng stage")
                        timing_rows = [
                            {"Stage": stage_name, "Thời gian (s)": round(float(elapsed_ms or 0) / 1000.0, 2)}
                            for stage_name, elapsed_ms in stage_timings.items()
                        ]
                        st.dataframe(pd.DataFrame(timing_rows), use_container_width=True, hide_index=True)
                        if isinstance(bottleneck, dict) and bottleneck:
                            st.caption(
                                "Bottleneck: "
                                f"{bottleneck.get('stage', '')} - {float(bottleneck.get('elapsed_ms', 0.0) or 0.0) / 1000.0:.2f} s"
                            )

                    if isinstance(retry_summary, dict) and retry_summary:
                        st.markdown("##### Retry diagnostics")
                        st.json(retry_summary)

                    if isinstance(models_used, dict) and models_used:
                        st.markdown("##### Model diagnostics")
                        st.dataframe(
                            pd.DataFrame(
                                [{"Agent": key, "Model": value} for key, value in models_used.items()]
                            ),
                            use_container_width=True,
                            hide_index=True,
                        )

                    if isinstance(rag_retrieval, dict) and rag_retrieval:
                        retrieval_rows = []
                        for group_name, group in rag_retrieval.items():
                            if not isinstance(group, dict):
                                continue
                            for source in group.get("sources", []) or []:
                                if isinstance(source, dict):
                                    retrieval_rows.append({"Nhóm": group_name, **source})
                            if group.get("skipped_reason"):
                                retrieval_rows.append({"Nhóm": group_name, "section": group.get("skipped_reason")})
                        if retrieval_rows:
                            st.markdown("##### RAG retrieval diagnostics")
                            st.dataframe(pd.DataFrame(retrieval_rows), use_container_width=True, hide_index=True)
        execution_summary = result.get("execution_summary", {})
        if isinstance(execution_summary, dict) and execution_summary:
            coverage_value = float(execution_summary.get("coverage_percent", 0.0))
            passed_value = bool(execution_summary.get("passed", False))
            missing_lines = execution_summary.get("missing_lines", [])
            display_fw = str(result.get("framework", framework) or "pytest")
            st.markdown(f"#### Kết quả chạy {display_fw}")
            run_cols = st.columns(3)
            run_cols[0].metric("Coverage", f"{coverage_value:.1f}%")
            run_cols[1].metric(f"{display_fw.capitalize()} pass", "Có" if passed_value else "Không")
            run_cols[2].metric(
                "Missing lines",
                str(len(missing_lines)) if isinstance(missing_lines, list) else "0",
            )
            execution_issue = execution_summary.get("execution_issue")
            if isinstance(execution_issue, dict) and execution_issue:
                st.caption(
                    "Execution issue: "
                    f"{execution_issue.get('type', '')} - {execution_issue.get('title', '')}"
                )
            output_text = normalize_text(str(execution_summary.get("output", "")))
            if output_text:
                st.markdown('<span id="pytest-log"></span>', unsafe_allow_html=True)
                with st.expander(f"Log {display_fw}", expanded=False):
                    st.code(output_text, language="text")
            collection_output = normalize_text(str(execution_summary.get("collection_output", "")))
            if collection_output:
                st.markdown('<span id="collect-only-log"></span>', unsafe_allow_html=True)
                with st.expander(f"Log {display_fw} collect-only", expanded=False):
                    st.code(collection_output, language="text")
            combined_report = execution_summary.get("combined_report")
            if isinstance(combined_report, dict):
                st.markdown("#### Combined coverage")
                combined_cols = st.columns(3)
                combined_cols[0].metric(
                    "Combined coverage",
                    f"{float(combined_report.get('coverage_percent', 0.0) or 0.0):.1f}%",
                )
                combined_cols[1].metric(
                    "Combined pass",
                    "Có" if bool(combined_report.get("passed", False)) else "Không",
                )
                combined_missing = combined_report.get("missing_lines", [])
                combined_cols[2].metric(
                    "Combined missing",
                    str(len(combined_missing)) if isinstance(combined_missing, list) else "0",
                )

    with tab_artifacts:
        if result.get("workflow") == REVIEW_WORKFLOW:
            st.info("Chế độ rà soát chỉ đánh giá test code đầu vào, không sinh mã kiểm thử mới.")
        else:
            framework_value = str(result.get("framework", framework))
            with st.expander("Mã kiểm thử", expanded=False):
                st.code(result.get("generated_code") or "", language=_code_language(framework_value))
            rows = result.get("test_case_rows")
            if not isinstance(rows, list):
                from testgen.agents.formatter_agent import parse_test_plan_rows
                rows = parse_test_plan_rows(str(result.get("test_plan_json", "")))
            st.subheader("Bảng test case")
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            with st.expander("JSON kế hoạch kiểm thử", expanded=False):
                from testgen.core.utils import pretty_json_or_raw
                st.code(pretty_json_or_raw(str(result.get("test_plan_json", ""))), language="json")

    with tab_review:
        # ── Header: Review score + target ──
        _prq = result.get("post_review_quality")
        _rev_score = int(_prq.get("review_score", 0) or 0) if isinstance(_prq, dict) else 0
        rev_header_cols = st.columns([2, 1])
        with rev_header_cols[0]:
            st.caption(f"Đã rà soát: {result.get('review_target_label', 'Mã kiểm thử đã sinh')}")
        with rev_header_cols[1]:
            st.metric("🔍 Review Agent Score", f"{_rev_score}/20")

        with st.expander("📄 Mã được rà soát", expanded=False):
            st.code(result.get("review_target_code") or "", language=_code_language(str(result.get("framework", framework))))

        review_report = str(result.get("review_report") or "")
        review_sections = parse_review_report_sections(review_report)
        has_grouped_review = any(section.get("items") for section in review_sections)

        if has_grouped_review:
            # ── Severity bars trực quan ──
            severity_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢", "Action": "🟦"}
            max_count = max(
                (len(s.get("items", [])) for s in review_sections if s.get("items")), default=1
            ) or 1
            bars_html_parts = []
            for section in review_sections:
                items = section.get("items", [])
                count = len(items) if isinstance(items, list) else 0
                icon = severity_icon.get(str(section.get("severity", "")), "🔵")
                label = f"{icon} {section.get('label', '')}"
                pct = int(count / max_count * 100) if max_count else 0
                color = {
                    "High": "pillar-red",
                    "Medium": "pillar-yellow",
                    "Low": "pillar-green",
                    "Action": "pillar-green",
                }.get(str(section.get("severity", "")), "pillar-yellow")
                bars_html_parts.append(
                    '<div class="pillar-bar-wrap">'
                    f'<div class="pillar-bar-label"><span>{escape(label)}</span>'
                    f'<span><b>{count}</b> vấn đề</span></div>'
                    '<div class="pillar-bar-track">'
                    f'<div class="pillar-bar-fill {color}" style="width:{pct}%"></div>'
                    '</div></div>'
                )
            st.markdown("".join(bars_html_parts), unsafe_allow_html=True)
            st.divider()

            # ── Chi tiết từng section ──
            for section in review_sections:
                items = section.get("items", [])
                if not isinstance(items, list) or not items:
                    continue
                label = str(section.get("label", ""))
                severity = str(section.get("severity", ""))
                icon = severity_icon.get(severity, "🔵")
                expanded = section.get("key") in {"critical", "fixes"}
                with st.expander(f"{icon} {label} ({len(items)})", expanded=expanded):
                    st.markdown(severity_badge_html(severity), unsafe_allow_html=True)
                    for item in items:
                        st.markdown(f"- {item}")
            with st.expander("📝 Markdown review gốc", expanded=False):
                st.markdown(review_report)
        else:
            st.markdown(review_report or "Chưa có báo cáo rà soát.")

    with tab_context:
        with st.expander("JSON yêu cầu", expanded=False):
            from testgen.core.utils import pretty_json_or_raw
            st.code(pretty_json_or_raw(str(result.get("requirement_json", ""))), language="json")

        docs_context = str(result.get("docs_context") or "").strip()
        source_context = str(result.get("source_context") or "").strip()
        if docs_context:
            with st.expander("Ngữ cảnh tài liệu", expanded=False):
                st.code(docs_context, language="markdown")
        if source_context:
            with st.expander("Ngữ cảnh source code", expanded=False):
                st.code(source_context, language="markdown")
        with st.expander("Ngữ cảnh truy xuất tổng hợp", expanded=False):
            st.code(result.get("context") or "Không có ngữ cảnh truy xuất.", language="markdown")

    with tab_exports:
        st.write("Các tệp đã xuất")
        code_path = str(result.get("code_path", ""))
        test_plan_path = str(result.get("test_plan_path", ""))
        review_path = str(result.get("review_path", ""))
        review_md_path = str(result.get("review_md_path", ""))
        coverage_report_path = str(result.get("coverage_report_path", ""))
        coverage_json_path = str(result.get("coverage_json_path", ""))
        coverage_raw_path = str(result.get("coverage_raw_path", ""))
        execution_summary = result.get("execution_summary", {})
        execution_summary = execution_summary if isinstance(execution_summary, dict) else {}
        pytest_log_path = _first_text(result.get("pytest_log_path"), execution_summary.get("pytest_log_path"))
        collection_log_path = _first_text(result.get("collection_log_path"), execution_summary.get("collection_log_path"))

        # We cannot easily re-use _download_button if it's in streamlit_app.py,
        # so let's import it or re-implement it briefly.
        from pathlib import Path
        def _file_mime(p: Path) -> str:
            if p.suffix == ".xlsx": return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            if p.suffix == ".pdf": return "application/pdf"
            if p.suffix == ".md": return "text/markdown"
            return "text/plain"
        
        def local_download_btn(label: str, path: str, key: str):
            if not path:
                st.caption(f"Thiếu đường dẫn cho {label}.")
                return
            file_path = Path(path)
            if not file_path.exists() or file_path.is_dir():
                st.caption(f"Thiếu tệp: {file_path}")
                return
            if file_path.suffix in {".xlsx", ".pdf"}:
                data = file_path.read_bytes()
            else:
                data = file_path.read_text(encoding="utf-8")
            st.download_button(label, data=data, file_name=file_path.name, mime=_file_mime(file_path), key=key, use_container_width=True)

        if code_path:
            local_download_btn("Tải mã kiểm thử", code_path, "code-download")
        if test_plan_path:
            local_download_btn("Tải bảng Excel kiểm thử", test_plan_path, "excel-download")
        if review_path:
            local_download_btn("Tải báo cáo rà soát", review_path, "review-download")

        if review_md_path:
            local_download_btn("Tải báo cáo Markdown", review_md_path, "review-md-download")
        if coverage_report_path:
            local_download_btn("Tải combined coverage report", coverage_report_path, "coverage-report-download")
        if coverage_json_path:
            local_download_btn("Tải combined coverage JSON", coverage_json_path, "coverage-json-download")
        if coverage_raw_path:
            local_download_btn("Tải raw coverage JSON", coverage_raw_path, "coverage-raw-download")

        display_fw = str(result.get("framework", framework) or "pytest")
        if pytest_log_path:
            local_download_btn(f"Tải {display_fw} log", pytest_log_path, "pytest-log-download")
        if collection_log_path:
            local_download_btn(f"Tải {display_fw} collect-only log", collection_log_path, "collect-log-download")

        exported_paths = "\n".join(
            path
            for path in [
                code_path,
                test_plan_path,
                review_path,
                review_md_path,
                coverage_report_path,
                coverage_json_path,
                coverage_raw_path,
                pytest_log_path,
                collection_log_path,
            ]
            if path
        )
        st.code(exported_paths or "Không có tệp để tải xuống.", language="text")
