from __future__ import annotations

from typing import Any


_NON_ERROR_SKIPS = {"pytest_ast_context", "no_source", "no_docs"}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _group_quality(name: str, diagnostics: dict[str, Any], *, min_confidence: float) -> dict[str, Any]:
    returned_chunks = int(diagnostics.get("returned_chunks", 0) or 0)
    skipped_reason = str(diagnostics.get("skipped_reason", "") or "")
    sources = diagnostics.get("sources", [])
    sources = sources if isinstance(sources, list) else []

    scores: list[float] = []
    missing_metadata_count = 0
    for source in sources:
        if not isinstance(source, dict):
            continue
        score = source.get("score")
        if score is not None:
            scores.append(_safe_float(score))
        missing_fields = source.get("metadata_missing_fields", [])
        if isinstance(missing_fields, list) and missing_fields:
            missing_metadata_count += 1

    max_score = max(scores) if scores else 0.0
    avg_score = sum(scores) / len(scores) if scores else 0.0
    warnings: list[str] = []

    if returned_chunks == 0 and skipped_reason and skipped_reason not in _NON_ERROR_SKIPS:
        warnings.append(f"{name}: retrieval skipped ({skipped_reason}).")
    if returned_chunks > 0 and not scores:
        warnings.append(f"{name}: không có relevance score trong diagnostics.")
    if returned_chunks > 0 and scores and max_score < min_confidence:
        warnings.append(f"{name}: low relevance score (max={max_score:.2f}).")
    if missing_metadata_count > 0:
        warnings.append(f"{name}: {missing_metadata_count} chunk thiếu metadata quan trọng.")

    return {
        "name": name,
        "returned_chunks": returned_chunks,
        "scores": [round(score, 4) for score in scores],
        "max_score": round(max_score, 4),
        "avg_score": round(avg_score, 4),
        "low_confidence": bool(returned_chunks > 0 and scores and max_score < min_confidence),
        "missing_score": bool(returned_chunks > 0 and not scores),
        "missing_metadata_count": missing_metadata_count,
        "skipped_reason": skipped_reason,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# P0.6: Kiểm tra framework/source_type/page metadata trong retrieved chunks
# ---------------------------------------------------------------------------

def _check_pdf_doc_metadata(
    sources: list[dict[str, Any]],
    *,
    expected_framework: str = "",
) -> dict[str, Any]:
    """Kiểm tra metadata chất lượng cho chunks loại pdf_doc.

    P0.6: Phát hiện chunks thiếu framework, source_type, page_start/page_end,
    hoặc không khớp framework đang chạy.

    Returns:
        Dict với các key: framework_missing, source_type_missing,
        page_metadata_missing, framework_mismatch, warnings.
    """
    framework_missing = 0
    source_type_missing = 0
    page_metadata_missing = 0
    framework_mismatch = 0
    warnings: list[str] = []

    pdf_sources = [s for s in sources if isinstance(s, dict) and str(s.get("chunk_type", "")) == "pdf_doc"]
    if not pdf_sources:
        return {
            "framework_missing": 0,
            "source_type_missing": 0,
            "page_metadata_missing": 0,
            "framework_mismatch": 0,
            "warnings": [],
        }

    for src in pdf_sources:
        fw = str(src.get("framework", "") or "")
        if not fw:
            framework_missing += 1
        elif expected_framework and fw.lower() != expected_framework.lower():
            framework_mismatch += 1

        # source_type nằm trong metadata_missing_fields hoặc không có trong source dict
        missing = src.get("metadata_missing_fields", [])
        if isinstance(missing, list):
            if "source_type" in missing:
                source_type_missing += 1

        pg_start = src.get("page_start", "")
        pg_end = src.get("page_end", "")
        if pg_start == "" and pg_end == "":
            page_metadata_missing += 1

    total = len(pdf_sources)
    if framework_missing:
        warnings.append(f"docs: {framework_missing}/{total} pdf_doc chunks thiếu metadata framework.")
    if source_type_missing > 0:
        warnings.append(f"docs: {source_type_missing}/{total} pdf_doc chunks thiếu source_type.")
    if page_metadata_missing > 0:
        warnings.append(f"docs: {page_metadata_missing}/{total} pdf_doc chunks thiếu page_start/page_end.")
    if expected_framework and framework_mismatch > 0:
        warnings.append(
            f"docs: {framework_mismatch}/{total} pdf_doc chunks không khớp framework={expected_framework}."
        )

    return {
        "framework_missing": framework_missing,
        "source_type_missing": source_type_missing,
        "page_metadata_missing": page_metadata_missing,
        "framework_mismatch": framework_mismatch,
        "warnings": warnings,
    }


def assess_rag_quality(
    rag_retrieval: dict[str, Any] | None,
    *,
    min_confidence: float = 0.35,
    expected_framework: str = "",
) -> dict[str, Any]:
    """Đánh giá chất lượng RAG retrieval.

    P0.6: Thêm kiểm tra framework/source_type/page metadata cho pdf_doc chunks.

    Args:
        rag_retrieval: Dict {"docs": diagnostics, "source": diagnostics}.
        min_confidence: Ngưỡng score tối thiểu.
        expected_framework: Framework đang chạy (vd: "pytest", "JUnit").
            Nếu truyền vào, sẽ cảnh báo nếu retrieved chunks không khớp.

    Returns:
        Dict quality report với thêm key "pdf_doc_quality".
    """
    retrieval = rag_retrieval if isinstance(rag_retrieval, dict) else {}
    groups: dict[str, dict[str, Any]] = {}
    for name in ("docs", "source"):
        group_diag = retrieval.get(name, {})
        groups[name] = _group_quality(
            name,
            group_diag if isinstance(group_diag, dict) else {},
            min_confidence=min_confidence,
        )

    returned_chunks = sum(int(group.get("returned_chunks", 0) or 0) for group in groups.values())
    score_values: list[float] = []
    for group in groups.values():
        scores = group.get("scores", [])
        if isinstance(scores, list):
            score_values.extend(_safe_float(score) for score in scores)
    max_score = max(score_values) if score_values else 0.0
    avg_score = sum(score_values) / len(score_values) if score_values else 0.0
    missing_metadata_count = sum(int(group.get("missing_metadata_count", 0) or 0) for group in groups.values())
    warnings = [warning for group in groups.values() for warning in group.get("warnings", [])]
    low_confidence = any(bool(group.get("low_confidence", False)) for group in groups.values())
    missing_score = any(bool(group.get("missing_score", False)) for group in groups.values())

    # P0.6: Kiểm tra pdf_doc metadata chất lượng
    all_sources: list[dict[str, Any]] = []
    for name in ("docs", "source"):
        group_diag = retrieval.get(name, {})
        if isinstance(group_diag, dict):
            srcs = group_diag.get("sources", [])
            if isinstance(srcs, list):
                all_sources.extend(srcs)

    pdf_doc_quality = _check_pdf_doc_metadata(all_sources, expected_framework=expected_framework)
    warnings.extend(pdf_doc_quality.get("warnings", []))

    # Tính verdict
    pdf_issues = (
        pdf_doc_quality.get("framework_missing", 0)
        + pdf_doc_quality.get("page_metadata_missing", 0)
        + pdf_doc_quality.get("framework_mismatch", 0)
    )

    if returned_chunks == 0:
        verdict = "missing"
        score = 0
    elif low_confidence or missing_metadata_count or missing_score or pdf_issues:
        verdict = "weak"
        score = max(35, min(69, int(avg_score * 100)))
    else:
        verdict = "good"
        score = max(70, min(100, int(avg_score * 100) if avg_score else 70))

    recommended_action: list[str] = []
    if returned_chunks == 0:
        recommended_action.append("Kiểm tra query, tài liệu/source đầu vào hoặc collection RAG.")
    low_quality = int(low_confidence) + int(missing_score)
    if low_quality > 0:
        recommended_action.append("Làm rõ retrieval query hoặc bổ sung từ khóa target/framework.")
    docs_missing = int(missing_metadata_count) + int(pdf_issues)
    if docs_missing > 0:
        recommended_action.append("Kiểm tra chunker/index metadata để debug nguồn context.")
        if expected_framework:
            recommended_action.append(
                "Kiểm tra chunk_pdf_pages_with_metadata() để gắn đủ framework/page metadata chưa."
            )
    if not recommended_action:
        recommended_action.append("RAG context đã đúng, không có hành động bắt buộc.")

    return {
        "verdict": verdict,
        "score": score,
        "returned_chunks": returned_chunks,
        "avg_score": round(avg_score, 4),
        "max_score": round(max_score, 4),
        "low_confidence": low_confidence,
        "missing_metadata_count": missing_metadata_count,
        "source_coverage": {
            "docs": int(groups["docs"].get("returned_chunks", 0) or 0),
            "source": int(groups["source"].get("returned_chunks", 0) or 0),
        },
        "warnings": warnings,
        "recommended_action": recommended_action,
        "groups": groups,
        "pdf_doc_quality": pdf_doc_quality,
    }
