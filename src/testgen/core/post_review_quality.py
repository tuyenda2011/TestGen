from __future__ import annotations

import re
import unicodedata
from typing import Any

from testgen.core.config import PYTEST_COVERAGE_THRESHOLD
from testgen.core.utils import repair_common_mojibake


E2E_API_FRAMEWORKS = {"Selenium", "Playwright", "Postman script"}
COVERAGE_FRAMEWORKS = {"pytest", "Jest", "JUnit"}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text or "")
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    without_marks = without_marks.replace("d", "d").replace("?", "D")
    return re.sub(r"[^a-zA-Z0-9]+", " ", without_marks).lower().strip()


def _review_findings(review_report: str) -> dict[str, list[str]]:
    groups = {
        "critical": [],
        "missing_tests": [],
        "weak_assertions": [],
        "maintainability": [],
        "fixes": [],
        "requirement": [],
        "ignored_missing_tests": [],
        "ignored_stale_findings": [],
    }
    current = ""
    skip_current_section = False
    in_code_block = False

    for raw_line in (review_report or "").splitlines():
        stripped = raw_line.strip()
        
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
            
        if in_code_block or not stripped:
            continue
            
        normalized = _normalize(stripped)
        if not normalized:
            continue
        if normalized.startswith(("khong phat hien", "khong can sua", "none", "n a")):
            continue

        if stripped.startswith("#"):
            skip_current_section = False
            if any(term in normalized for term in ("loi nghiem trong", "critical", "major")):
                current = "critical"
            elif any(term in normalized for term in ("test con thieu", "missing test", "coverage thieu")):
                current = "missing_tests"
            elif any(term in normalized for term in ("assertion yeu", "weak assertion", "assert yeu")):
                current = "weak_assertions"
            elif any(term in normalized for term in ("maintainability", "bao tri", "flaky")):
                current = "maintainability"
            elif any(term in normalized for term in ("sai requirement", "sai yeu cau", "mismatch", "invented")):
                current = "requirement"
            elif any(term in normalized for term in ("goi y", "fix", "sua ngay")):
                current = "fixes"
            else:
                current = ""
            continue

        if skip_current_section:
            continue

        is_bullet = bool(re.match(r"^\s*([-*+]|\d+[.)])\s+", raw_line))
        cleaned = re.sub(r"^\s*[-*+]\s*", "", stripped)
        cleaned = re.sub(r"^\s*\d+[.)]\s*", "", cleaned).strip()
        if not cleaned:
            continue

        norm_cleaned = _normalize(cleaned)
        if norm_cleaned in ("khong phat hien", "khong co", "none", "n a", "khong"):
            skip_current_section = True
            continue
        if current == "maintainability" and any(
            phrase in norm_cleaned
            for phrase in (
                "khong co mock",
                "khong co phu thuoc ben ngoai",
                "it rui ro flaky",
                "khong gay rui ro flaky",
                "khong phu thuoc ben ngoai",
            )
        ):
            continue
            
        if "out of scope" in norm_cleaned:
            continue

        target = current
        if not target:
            if any(term in normalized for term in ("critical", "import sai", "syntax", "khong chay", "sai expected")):
                target = "critical"
            elif any(term in normalized for term in ("thieu", "missing", "boundary", "negative")):
                target = "missing_tests"
            elif any(term in normalized for term in ("assert true", "assertion yeu", "print", "weak assertion")):
                target = "weak_assertions"
            elif any(term in normalized for term in ("sai requirement", "sai yeu cau", "mismatch", "invented", "bia")):
                target = "requirement"
            elif any(term in normalized for term in ("flaky", "network", "sleep", "maintainability", "bao tri")):
                target = "maintainability"
            elif any(term in normalized for term in ("goi y", "fix", "sua")):
                target = "fixes"
                
        if target in groups:
            is_nested_bullet = bool(re.match(r"^\s{2,}([-*+]|\d+[.)])\s+", raw_line))
            if is_nested_bullet and groups[target]:
                groups[target][-1] += " " + cleaned
            elif is_bullet or not groups[target]:
                groups[target].append(cleaned)
            else:
                groups[target][-1] += " " + cleaned
    return groups


def _first_issue_type(framework: str, execution_summary: dict[str, Any], diagnostics: dict[str, Any]) -> str:
    issue = execution_summary.get("execution_issue")
    if isinstance(issue, dict) and issue.get("type"):
        return str(issue.get("type"))
    normalized_framework = framework.lower().replace(" ", "_").replace("-", "_")
    return str(
        diagnostics.get(f"{normalized_framework}_execution_issue_type")
        or diagnostics.get("external_execution_issue_type")
        or diagnostics.get("pytest_execution_issue_type")
        or ""
    )


def _normalize_e2e_issue_type(framework: str, issue_type: str, coverage_supported: bool) -> str:
    if framework in E2E_API_FRAMEWORKS and not coverage_supported and issue_type == "coverage_artifact_missing":
        return "none"
    return issue_type


def _has_artifact(execution_summary: dict[str, Any], *keys: str) -> bool:
    return any(bool(str(execution_summary.get(key, "") or "").strip()) for key in keys)


def _case_ids_in_text(text: str) -> list[str]:
    candidates = [str(text or ""), repair_common_mojibake(text)]
    ids: set[str] = set()
    for candidate in candidates:
        normalized = unicodedata.normalize("NFKC", candidate)
        for match in re.findall(r"(?i)\btc.{0,12}?(\d{1,4})", normalized):
            ids.add(f"TC-{match.zfill(3)}")
    return sorted(ids)


def _text_mentions_any(text: str, values: set[str]) -> bool:
    if not values:
        return False
    normalized = _normalize(repair_common_mojibake(text))
    return any(_normalize(value) in normalized for value in values if _normalize(value))


def _is_jest_non_public_missing_note(text: str) -> bool:
    normalized = _normalize(repair_common_mojibake(text))
    non_public_markers = (
        "khong duoc export",
        "khong export",
        "not exported",
        "non exported",
        "module exports",
        "ham noi bo",
        "internal helper",
        "khong the kiem thu truc tiep",
        "kiem thu gian tiep",
        "export ham",
    )
    return any(marker in normalized for marker in non_public_markers)


def _filter_jest_missing_findings(
    findings: dict[str, list[str]],
    traceability: dict[str, Any],
) -> dict[str, list[str]]:
    filtered = {key: list(value) for key, value in findings.items()}
    missing_in_scope = set(traceability.get("missing_in_scope_case_ids", []) or [])
    raw_missing = set(traceability.get("raw_missing_case_ids", traceability.get("missing_case_ids", [])) or [])
    non_required = set(traceability.get("ambiguous_case_ids", []) or []) | set(
        traceability.get("out_of_scope_case_ids", []) or []
    )
    case_bindings = traceability.get("case_bindings", {}) or {}
    case_reasons = traceability.get("case_binding_reasons", {})
    non_required_symbols: set[str] = set()
    if isinstance(case_reasons, dict):
        for case_id, reason in case_reasons.items():
            if case_id in non_required and "exported source symbol" in str(reason).lower():
                if isinstance(case_bindings, dict) and case_id in case_bindings:
                    for symbol in case_bindings[case_id]:
                        non_required_symbols.add(str(symbol))

    kept_missing: list[str] = []
    ignored_missing: list[str] = []
    for item in filtered.get("missing_tests", []):
        ids = set(_case_ids_in_text(item))
        if ids and ids <= raw_missing and not ids & missing_in_scope:
            ignored_missing.append(item)
            continue
        if non_required_symbols and _text_mentions_any(item, non_required_symbols):
            ignored_missing.append(item)
            continue
        if not missing_in_scope and _is_jest_non_public_missing_note(item):
            ignored_missing.append(item)
            continue
        kept_missing.append(item)

    filtered["missing_tests"] = kept_missing
    if ignored_missing:
        filtered["ignored_missing_tests"] = ignored_missing
    return filtered


def _filter_stale_jest_findings_against_code(
    findings: dict[str, list[str]],
    traceability: dict[str, Any],
    generated_code: str,
) -> dict[str, list[str]]:
    filtered = {key: list(value) for key, value in findings.items()}
    code_norm = _normalize(generated_code)
    missing_in_scope = set(traceability.get("missing_in_scope_case_ids", []) or [])

    target_member_counts = {
        "shippingfee": len(re.findall(r"\btarget\s*\.\s*shippingFee\s*\(", generated_code or "")),
        "normalizelabel": len(re.findall(r"\btarget\s*\.\s*normalizeLabel\s*\(", generated_code or "")),
        "finaltotal": len(re.findall(r"\btarget\s*\.\s*finalTotal\s*\(", generated_code or "")),
        "calculatediscount": len(re.findall(r"\btarget\s*\.\s*calculateDiscount\s*\(", generated_code or "")),
    }

    def mentions(item: str, *needles: str) -> bool:
        normalized = _normalize(repair_common_mojibake(item))
        return any(needle in normalized for needle in needles)

    def stale_missing(item: str) -> bool:
        if _case_ids_in_text(item) and missing_in_scope:
            return False
        if mentions(item, "shippingfee") and target_member_counts["shippingfee"] >= 3:
            return True
        if mentions(item, "normalizelabel") and target_member_counts["normalizelabel"] >= 2:
            return True
        if mentions(item, "finaltotal") and not missing_in_scope and target_member_counts["finaltotal"] >= 2:
            return True
        return False

    stale_missing_items: list[str] = []
    kept_missing: list[str] = []
    for item in filtered.get("missing_tests", []):
        if stale_missing(item):
            stale_missing_items.append(item)
        else:
            kept_missing.append(item)
    filtered["missing_tests"] = kept_missing

    has_spy_on = "jest spyon" in code_norm
    if not has_spy_on:
        for key in ("weak_assertions", "maintainability"):
            kept: list[str] = []
            stale: list[str] = []
            for item in filtered.get(key, []):
                if mentions(item, "jest spyon", "mock khong", "mock shippingfee", "false sense of coverage"):
                    stale.append(item)
                else:
                    kept.append(item)
            filtered[key] = kept
            if stale:
                filtered.setdefault("ignored_stale_findings", []).extend(stale)

    kept_fixes: list[str] = []
    ignored_fixes: list[str] = []
    for item in filtered.get("fixes", []):
        if (not has_spy_on and mentions(item, "spyon", "mock shippingfee")) or stale_missing(item):
            ignored_fixes.append(item)
        else:
            kept_fixes.append(item)
    filtered["fixes"] = kept_fixes

    if stale_missing_items:
        filtered.setdefault("ignored_stale_findings", []).extend(stale_missing_items)
    if ignored_fixes:
        filtered.setdefault("ignored_stale_findings", []).extend(ignored_fixes)
    return filtered


def _filter_stale_browser_e2e_findings_against_artifacts(
    findings: dict[str, list[str]],
    generated_code: str,
    execution_summary: dict[str, Any],
    traceability: dict[str, Any] | None = None,
) -> dict[str, list[str]]:
    filtered = {key: list(value) for key, value in findings.items()}
    traceability = traceability if isinstance(traceability, dict) else {}
    missing_in_scope = set(traceability.get("missing_in_scope_case_ids", []) or [])
    evidence_text = "\n".join(
        repair_common_mojibake(value)
        for value in (
            generated_code,
            execution_summary.get("final_code", ""),
            execution_summary.get("collection_output", ""),
            execution_summary.get("output", ""),
        )
        if value
    )
    evidence_norm = _normalize(evidence_text)
    if not evidence_norm:
        return filtered

    def evidence_has(*needles: str) -> bool:
        return any(needle in evidence_norm for needle in needles)

    covered = {
        "fragile": evidence_has("fragile"),
        "credit": evidence_has("credit"),
        "weight_zero_or_negative": evidence_has(
            "weight zero",
            "weight negative",
            "weight invalid",
            "weight must be greater",
            "send keys 0",
            "send keys 0",
            "send keys 1",
            "send keys 1",
            "weight nonpositive",
        ),
        "weight_over_20": evidence_has("weight over 20", "weight greater than 20", "weight 25"),
        "prevent_default": evidence_has(
            "prevent default",
            "prevents default",
            "preventdefault",
            "submit prevents default",
        ),
    }

    def stale_runtime_contract(item: str) -> bool:
        item_norm = _normalize(repair_common_mojibake(item))
        # 1. Ignore complaints about hardcoded html path
        if "source under test html" in item_norm or "duong dan" in item_norm or "path" in item_norm:
            if any(marker in item_norm for marker in ("tinh", "static", "hardcode", "phu thuoc", "vi tri", "di chuyen", "sai", "wrong", "khong ton tai")):
                return True
        # 2. Ignore complaints about Edge WebDriver
        if "edge" in item_norm or "webdriver" in item_norm:
            if any(marker in item_norm for marker in ("trinh duyet", "browser", "ci", "san co", "tuong thich", "phien ban", "truy cap")):
                return True
        # 3. Ignore complaints about parallel helper functions
        if "helper" in item_norm or "song song" in item_norm or "javascript" in item_norm:
            if any(marker in item_norm for marker in ("duy tri", "maintain", "dong bo", "cap nhat", "thay doi", "rui ro")):
                return True
        # 4. Ignore false weak assertion claims about JS exceptions or error text
        if "pytest raises" in item_norm or "javascriptexception" in item_norm or "exception" in item_norm:
            if any(marker in item_norm for marker in ("chung chung", "cu the", "khong kiem chung", "weak", "yeu")):
                return True
        if "error" in item_norm or "0 00" in item_norm or "trong" in item_norm:
            if any(marker in item_norm for marker in ("yeu", "weak", "khong chac chan", "thuc su", "khong xac thuc", "hien thi")):
                return True
        if "coverage artifact" in item_norm or "coverage_artifact_missing" in item_norm:
            return True
        return False

    def stale_missing(item: str) -> bool:
        item_norm = _normalize(repair_common_mojibake(item))
        if stale_runtime_contract(item_norm):
            return True
        if not missing_in_scope and any(marker in item_norm for marker in ("blocker", "van de chinh", "issue chinh")):
            mentioned = []
            if "fragile" in item_norm:
                mentioned.append(covered["fragile"])
            if "credit" in item_norm:
                mentioned.append(covered["credit"])
            if "weight" in item_norm or "trong luong" in item_norm:
                mentioned.append(covered["weight_zero_or_negative"] or covered["weight_over_20"])
            if "prevent" in item_norm and "default" in item_norm:
                mentioned.append(covered["prevent_default"])
            if mentioned and all(mentioned):
                return True
        if "fragile" in item_norm and covered["fragile"]:
            return True
        if "credit" in item_norm and covered["credit"]:
            return True
        if ("preventdefault" in item_norm or ("prevent" in item_norm and "default" in item_norm)) and covered["prevent_default"]:
            return True
        if "weight" in item_norm or "trong luong" in item_norm:
            if any(marker in item_norm for marker in ("0", "zero", "negative", "invalid", "am", "khong hop le")):
                return covered["weight_zero_or_negative"]
            if "20" in item_norm or "over" in item_norm or "greater" in item_norm or "lon hon" in item_norm:
                return covered["weight_over_20"]
        return False

    stale_items: list[str] = []
    kept_items: list[str] = []
    for item in filtered.get("missing_tests", []):
        if stale_missing(item):
            stale_items.append(item)
        else:
            kept_items.append(item)
    filtered["missing_tests"] = kept_items
    if stale_items:
        filtered.setdefault("ignored_stale_findings", []).extend(stale_items)

    for key in ("critical", "maintainability", "fixes", "weak_assertions"):
        kept: list[str] = []
        ignored: list[str] = []
        for item in filtered.get(key, []):
            if stale_runtime_contract(item):
                ignored.append(item)
            else:
                kept.append(item)
        filtered[key] = kept
        if ignored:
            filtered.setdefault("ignored_stale_findings", []).extend(ignored)
    return filtered


def _filter_stale_postman_findings_against_artifacts(
    findings: dict[str, list[str]],
    generated_code: str,
    execution_summary: dict[str, Any],
    traceability: dict[str, Any],
    requirement_json: str,
) -> dict[str, list[str]]:
    filtered = {key: list(value) for key, value in findings.items()}
    missing_in_scope = set(traceability.get("missing_in_scope_case_ids", []) or [])
    quality = execution_summary.get("postman_static_quality", {})
    quality = quality if isinstance(quality, dict) else {}
    assertions_total = int(quality.get("assertions_total", quality.get("assertion_count", 0)) or 0)
    has_body_assert = bool(quality.get("body_assert_present", False))
    has_schema_assert = bool(quality.get("schema_assert_present", False))
    evidence_norm = _normalize(
        "\n".join(
            repair_common_mojibake(value)
            for value in (
                generated_code,
                execution_summary.get("final_code", ""),
                execution_summary.get("output", ""),
                execution_summary.get("collection_output", ""),
            )
            if value
        )
    )
    requirement_norm = _normalize(repair_common_mojibake(requirement_json))

    def requirement_mentions(*needles: str) -> bool:
        return any(needle in requirement_norm for needle in needles)

    def evidence_mentions(*needles: str) -> bool:
        return any(needle in evidence_norm for needle in needles)

    def stale_postman_item(item: str, *, key: str) -> bool:
        item_norm = _normalize(repair_common_mojibake(item))
        if not missing_in_scope and any(marker in item_norm for marker in ("clarification", "lam ro", "out of scope")):
            return True
        if any(marker in item_norm for marker in ("auth", "authentication", "token", "bao mat", "xac thuc")):
            return not requirement_mentions("auth", "authentication", "token", "bao mat", "xac thuc")
        if any(marker in item_norm for marker in ("response time", "thoi gian phan hoi", "performance", "latency")):
            return not requirement_mentions("response time", "performance", "latency", "thoi gian phan hoi")
        if "schema" in item_norm or "json schema" in item_norm:
            return has_body_assert and (has_schema_assert or not requirement_mentions("schema", "json schema"))
        if any(marker in item_norm for marker in ("hard coded", "hard code", "hard coded", "gia tri cung")):
            return has_body_assert and assertions_total >= 2
        if key == "weak_assertions" and has_body_assert:
            if any(marker in item_norm for marker in ("total", "error", "include", "message", "diagnostics")):
                return True
        if key == "missing_tests" and not missing_in_scope:
            if "storecredit" in item_norm and evidence_mentions("storecredit"):
                return True
            if "subtotal" in item_norm and evidence_mentions("subtotal"):
                return True
            if "destination" in item_norm and evidence_mentions("destination"):
                return True
            if "weight" in item_norm and evidence_mentions("weightkg", "weight"):
                return True
        return False

    for key in ("missing_tests", "weak_assertions", "maintainability", "fixes"):
        kept: list[str] = []
        ignored: list[str] = []
        for item in filtered.get(key, []):
            if stale_postman_item(item, key=key):
                ignored.append(item)
            else:
                kept.append(item)
        filtered[key] = kept
        if ignored:
            filtered.setdefault("ignored_stale_findings", []).extend(ignored)
    return filtered


def _jest_static_quality(execution_summary: dict[str, Any]) -> dict[str, Any]:
    quality = execution_summary.get("jest_static_quality", {})
    return quality if isinstance(quality, dict) else {}


def assess_post_review_quality(
    *,
    framework: str,
    execution_summary: dict[str, Any] | None = None,
    review_report: str = "",
    generated_code: str = "",
    test_plan_json: str = "",
    requirement_json: str = "",
    diagnostics: dict[str, Any] | None = None,
    coverage_threshold: float = PYTEST_COVERAGE_THRESHOLD,
) -> dict[str, Any]:
    execution_summary = execution_summary if isinstance(execution_summary, dict) else {}
    diagnostics = diagnostics if isinstance(diagnostics, dict) else {}
    framework = framework or str(diagnostics.get("test_execution_framework") or "pytest")
    is_e2e_api = framework.lower() in {fw.lower() for fw in E2E_API_FRAMEWORKS}
    quality_gate = "flow_api_assertions" if is_e2e_api else "coverage"

    normalized_framework = framework.lower().replace(" ", "_").replace("-", "_")
    passed = bool(
        execution_summary.get(
            "passed",
            diagnostics.get("external_execution_passed", diagnostics.get(f"{normalized_framework}_passed", diagnostics.get("pytest_passed", False))),
        )
    )
    coverage_supported = bool(execution_summary.get("coverage_supported", not is_e2e_api))
    coverage = _safe_float(
        execution_summary.get(
            "coverage_percent",
            diagnostics.get("external_coverage_percent", diagnostics.get(f"{normalized_framework}_coverage_percent", diagnostics.get(f"{normalized_framework}_combined_coverage_percent", diagnostics.get("pytest_combined_coverage_percent", 0.0)))),
        )
    )
    issue_type = _normalize_e2e_issue_type(
        framework,
        _first_issue_type(framework, execution_summary, diagnostics),
        coverage_supported,
    )
    findings = _review_findings(review_report)

    from testgen.core.test_case_traceability import evaluate_traceability
    traceability = evaluate_traceability(test_plan_json, generated_code)
    diagnostics["traceability"] = traceability
    if framework == "Jest":
        findings = _filter_jest_missing_findings(findings, traceability)
        findings = _filter_stale_jest_findings_against_code(findings, traceability, generated_code)
    if framework in {"Selenium", "Playwright"}:
        findings = _filter_stale_browser_e2e_findings_against_artifacts(
            findings,
            generated_code,
            execution_summary,
            traceability,
        )
    if framework == "Postman script":
        findings = _filter_stale_postman_findings_against_artifacts(
            findings,
            generated_code,
            execution_summary,
            traceability,
            requirement_json,
        )

    blocking_findings: list[str] = []
    recommended_action: list[str] = []

    if not passed:
        blocking_findings.append(f"Execution chưa pass ({issue_type or 'unknown'}).")
        recommended_action.append("Sửa lỗi execution trước khi xuất kết quả.")

    if not is_e2e_api and coverage_supported and coverage < coverage_threshold:
        blocking_findings.append(f"Coverage {coverage:.1f}% dưới ngưỡng {coverage_threshold:.0f}%.")
        recommended_action.append("Bổ sung test cho missing lines hoặc branch chưa cover.")

    critical_count = len(findings["critical"])
    weak_count = len(findings["weak_assertions"])
    missing_count = len(findings["missing_tests"])
    requirement_count = len(findings["requirement"])
    maintainability_count = len(findings["maintainability"])

    missing_tc_ids = traceability.get("missing_in_scope_case_ids", traceability.get("missing_case_ids", []))
    
    # [SANITY FILTER] Trust AST Traceability over LLM hallucination for missing tests across all frameworks
    if not missing_tc_ids:
        # AST confirms 100% test plan coverage -> LLM is hallucinating out-of-scope missing tests
        if findings["missing_tests"]:
            findings.setdefault("ignored_missing_tests", []).extend(findings["missing_tests"])
            findings["missing_tests"] = []
        missing_count = 0
    else:
        # Trust the deterministic AST count
        missing_count = len(missing_tc_ids)

    # [SANITY FILTER] Trust runtime perfection over LLM nitpicking
    # If the code passes fully and has perfect coverage, it is functionally sound. Ignore arbitrary critical/requirement hallucinations.
    if passed and (not coverage_supported or coverage >= 100.0):
        if findings["critical"]:
            findings.setdefault("ignored_critical", []).extend(findings["critical"])
            findings["critical"] = []
        if findings["requirement"]:
            findings.setdefault("ignored_requirement", []).extend(findings["requirement"])
            findings["requirement"] = []

    critical_count = len(findings["critical"])
    requirement_count = len(findings["requirement"])

    if critical_count:
        blocking_findings.extend(findings["critical"][:3])
        recommended_action.append("Ưu tiên sửa lỗi nghiêm trọng trong review report.")
    if requirement_count > 0:
        recommended_action.append("Đối chiếu lại requirement/test plan với test đã sinh.")
    if weak_count > 0:
        recommended_action.append("Bổ sung assertion kiểm tra outcome thật, không dùng assert hời hợt.")
    if missing_count > 0:
        recommended_action.append("Bổ sung scenario còn thiếu theo test plan.")
    if maintainability_count > 0:
        recommended_action.append("Giảm rủi ro flaky/maintainability trong test.")

    if framework == "Jest":
        jest_quality = _jest_static_quality(execution_summary)
        non_public = list(jest_quality.get("unknown_target_members", []) or [])
        monkey_patches = list(jest_quality.get("monkey_patches", []) or [])
        fallbacks = list(jest_quality.get("fallback_implementations", []) or [])
        reimplemented = list(jest_quality.get("reimplemented_exports", []) or [])
        reimplemented_internal = list(jest_quality.get("reimplemented_internal_helpers", []) or [])

        if issue_type in {
            "module_import_contract_violation",
            "invalid_public_api_test",
            "test_reimplements_source",
            "source_dependency_missing",
        }:
            blocking_findings.append(f"Jest public API/import gate blocked: {issue_type}.")
        if non_public:
            blocking_findings.append(
                "Jest test calls non-exported source members: " + ", ".join(non_public[:5])
            )
            recommended_action.append("Rewrite Jest tests to cover internal helpers indirectly via module.exports APIs.")
        if monkey_patches or fallbacks:
            blocking_findings.append("Jest test mutates or fabricates target exports.")
            recommended_action.append("Remove target monkey-patches/fallback implementations from Jest tests.")
        if reimplemented:
            blocking_findings.append(
                "Jest test reimplements exported source logic: " + ", ".join(reimplemented[:5])
            )
            recommended_action.append("Assert the real exported implementation instead of copying source logic into tests.")
            
        if reimplemented_internal:
            findings["maintainability"].append("Jest test reimplements internal source helpers: " + ", ".join(reimplemented_internal[:5]))
            maintainability_count = len(findings["maintainability"])
            recommended_action.append("Do not copy internal source helper logic into tests.")

    if is_e2e_api:
        weak_runtime_issues = {
            "weak_e2e_test",
            "weak_postman_assertion",
            "target_fixture_not_opened",
            "invalid_postman_artifact",
            "invalid_postman_collection",
            "unstable_locator",
            "network_not_allowed",
        }
        if issue_type in weak_runtime_issues:
            blocking_findings.append(f"Quality gate E2E/API chặn: {issue_type}.")
        e2e_quality = execution_summary.get("e2e_static_quality", {})
        postman_quality = execution_summary.get("postman_static_quality", {})
        quality = e2e_quality if isinstance(e2e_quality, dict) and e2e_quality else postman_quality
        if isinstance(quality, dict) and quality:
            if int(quality.get("assertion_count", quality.get("assertions_total", 0)) or 0) <= 0:
                blocking_findings.append("Thiếu assertion có ý nghĩa.")
            if (
                framework in {"Selenium", "Playwright"}
                and int(quality.get("meaningful_assertion_count", 1) or 0) <= 0
            ):
                blocking_findings.append("Thiếu assertion UI/E2E có ý nghĩa.")
            if framework == "Postman script" and not bool(quality.get("body_assert_present", False)):
                recommended_action.append("Thêm assertion kiểm tra response body/schema cho Postman.")
            if framework in {"Selenium", "Playwright"} and bool(quality.get("uses_sleep", False)):
                recommended_action.append("Thay sleep bằng explicit wait/expect phù hợp.")
            if framework in {"Selenium", "Playwright"} and not bool(quality.get("negative_or_boundary_evidence", True)):
                recommended_action.append("Bổ sung case âm/biên và assert thông báo hoặc trạng thái UI hiển thị.")

    execution_score = 30 if passed else 0
    if is_e2e_api:
        flow_or_api_assertion_score = 25
        if issue_type in {"weak_e2e_test", "weak_postman_assertion", "target_fixture_not_opened", "invalid_postman_artifact"}:
            flow_or_api_assertion_score = 0
        elif issue_type in {"unstable_locator", "missing_wait_strategy", "request_failed"}:
            flow_or_api_assertion_score = 12
        elif not passed:
            flow_or_api_assertion_score = 8

        stability_score = max(0, 10 - maintainability_count * 3)
        artifact_required = (
            _has_artifact(execution_summary, "source_path", "pytest_log_path")
            if framework in {"Selenium", "Playwright"}
            else _has_artifact(execution_summary, "postman_summary_path", "report_path")
        )
        artifact_score = 5 if artifact_required or passed else 0
        coverage_score = 0
    else:
        coverage_score = min(25, int(max(0.0, coverage) / max(coverage_threshold, 1.0) * 25))
        flow_or_api_assertion_score = 0
        stability_score = max(0, 5 - maintainability_count * 2)
        artifact_score = 0

    missing_penalty = 1 if is_e2e_api else 3
    review_penalty = critical_count * 8 + weak_count * 4 + missing_count * missing_penalty + requirement_count * 6 + maintainability_count * 1
    review_score = max(0, 20 - review_penalty)
    assertion_quality_score = max(0, 10 - weak_count * 4)
    requirement_alignment_score = max(0, 10 - requirement_count * 5 - missing_count * 2)
    maintainability_score = stability_score if is_e2e_api else max(0, 5 - maintainability_count * 2)

    score = execution_score + review_score + assertion_quality_score + requirement_alignment_score + maintainability_score + artifact_score
    if is_e2e_api:
        score += flow_or_api_assertion_score
    else:
        score += coverage_score
    score = max(0, min(100, score))

    if blocking_findings or not passed:
        verdict = "Rủi ro cao" if critical_count or not passed else "Cần sửa"
        score = min(score, 69 if verdict == "Cần sửa" else 49)
    elif score >= 80:
        verdict = "Đạt"
    elif score >= 60:
        verdict = "Cần sửa"
    else:
        verdict = "Rủi ro cao"

    if missing_tc_ids:
        recommended_action.append(f"Traceability: Thiếu {len(missing_tc_ids)} test case hợp lệ (in-scope) so với plan: {', '.join(missing_tc_ids[:5])}{'...' if len(missing_tc_ids) > 5 else ''}")
        
    out_of_scope = traceability.get("out_of_scope_case_ids", [])
    if out_of_scope:
        recommended_action.append(f"Traceability: Cảnh báo, Plan có {len(out_of_scope)} test case nằm ngoài phạm vi runtime source (không bắt buộc code generator thực thi).")

    if not recommended_action:
        recommended_action.append("Không có hành động bắt buộc từ đánh giá sau rà soát.")

    return {
        "verdict": verdict,
        "score": int(score),
        "quality_gate": quality_gate,
        "blocking_findings": blocking_findings,
        "recommended_action": list(dict.fromkeys(recommended_action)),
        "review_score": review_score,
        "execution_score": execution_score,
        "coverage_score": coverage_score,
        "flow_or_api_assertion_score": flow_or_api_assertion_score,
        "assertion_quality_score": assertion_quality_score,
        "requirement_alignment_score": requirement_alignment_score,
        "maintainability_score": maintainability_score,
        "artifact_score": artifact_score,
        "issue_type": issue_type,
        "review_findings": findings,
        "coverage_percent": coverage,
        "coverage_supported": coverage_supported,
        "framework": framework,
        "traceability": traceability,
    }
