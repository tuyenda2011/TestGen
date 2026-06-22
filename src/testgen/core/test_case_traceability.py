import json
import re
from typing import Any


def _normalize_case_id(value: object) -> str:
    match = re.search(r"(?i)tc[-_]?(\d{1,4})", str(value or ""))
    return f"TC-{match.group(1).zfill(3)}" if match else str(value or "").strip()


def _normalize_case_ids(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    normalized = [_normalize_case_id(value) for value in values]
    return sorted({value for value in normalized if value})


def _simple_symbol_name(name: str) -> str:
    return (name or "").rsplit(".", 1)[-1].lower()


def extract_implemented_test_cases(generated_code: str) -> list[str]:
    """Find TC IDs in generated test code."""
    if not generated_code:
        return []
    raw_matches = re.findall(r"(?i)tc[-_]?(\d{1,4})", generated_code)
    return sorted({f"TC-{str(match).zfill(3)}" for match in raw_matches})


def count_test_blocks(generated_code: str) -> int:
    """Count runnable test blocks for fallback traceability."""
    if not generated_code:
        return 0
    pytest_tests = len(re.findall(r"(?m)^[ \t]*def\s+test_", generated_code))
    jest_tests = len(re.findall(r"(?m)^[ \t]*(?:test|it)\s*\(", generated_code))
    junit_tests = len(re.findall(r"(?m)^[ \t]*@(?:org\.junit\.jupiter\.api\.)?Test\b", generated_code))
    selenium_tests = pytest_tests
    postman_items = len(re.findall(r'"name":\s*"[^"]*"', generated_code)) if "pm.test" in generated_code else 0

    return max(pytest_tests, jest_tests, junit_tests, selenium_tests, postman_items)


def extract_planned_test_cases(test_plan_json: str) -> list[str]:
    """Extract normalized TC IDs from test plan JSON."""
    if not test_plan_json:
        return []
    try:
        data = json.loads(test_plan_json)
        scenarios = data.get("test_scenarios") or data.get("test_cases") or []
        if isinstance(scenarios, list):
            ids = [_normalize_case_id(s.get("id", "")) for s in scenarios if isinstance(s, dict)]
            return sorted({case_id for case_id in ids if case_id})
    except Exception:
        pass
    return []


def _case_bindings_from_scope(scope: dict[str, Any]) -> dict[str, list[str]]:
    raw_bindings = scope.get("case_bindings", {})
    if not isinstance(raw_bindings, dict):
        return {}
    bindings: dict[str, list[str]] = {}
    for raw_case_id, raw_symbols in raw_bindings.items():
        case_id = _normalize_case_id(raw_case_id)
        if not case_id or not isinstance(raw_symbols, list):
            continue
        symbols = [str(symbol).lower() for symbol in raw_symbols if str(symbol or "").strip()]
        if symbols:
            bindings[case_id] = symbols
    return bindings


def _semantically_implemented_cases(
    *,
    planned: list[str],
    implemented: list[str],
    case_bindings: dict[str, list[str]],
    generated_code: str,
) -> list[str]:
    code = (generated_code or "").lower()
    semantic_ids: list[str] = []
    for case_id in planned:
        if case_id in implemented:
            continue
        bindings = case_bindings.get(case_id, [])
        if not bindings:
            continue
        for binding in bindings:
            simple = _simple_symbol_name(binding)
            if not simple:
                continue
            # Avoid treating a class-only mention as proof for every scenario.
            if "." not in binding and re.search(r"\bclass\s+" + re.escape(simple) + r"\b", code):
                continue
            if re.search(r"\b" + re.escape(simple) + r"\b", code):
                semantic_ids.append(case_id)
                break
    return sorted(set(semantic_ids))


def evaluate_traceability(test_plan_json: str, generated_code: str) -> dict[str, Any]:
    planned = extract_planned_test_cases(test_plan_json)
    implemented = extract_implemented_test_cases(generated_code)

    out_of_scope_case_ids: list[str] = []
    ambiguous_case_ids: list[str] = []
    bound_case_ids: list[str] = []
    case_bindings: dict[str, list[str]] = {}
    case_reasons: dict[str, str] = {}

    try:
        data = json.loads(test_plan_json)
        scope = data.get("scope_validation", {})
        if isinstance(scope, dict) and scope:
            out_of_scope_case_ids = _normalize_case_ids(scope.get("out_of_scope_cases", []))
            ambiguous_case_ids = _normalize_case_ids(scope.get("ambiguous_cases", []))
            bound_case_ids = _normalize_case_ids(scope.get("bound_cases", []))
            case_bindings = _case_bindings_from_scope(scope)
            raw_reasons = scope.get("case_reasons", {})
            if isinstance(raw_reasons, dict):
                case_reasons = {
                    _normalize_case_id(case_id): str(reason)
                    for case_id, reason in raw_reasons.items()
                    if _normalize_case_id(case_id)
                }
    except Exception:
        pass

    semantic_implemented = _semantically_implemented_cases(
        planned=planned,
        implemented=implemented,
        case_bindings=case_bindings,
        generated_code=generated_code,
    )
    all_implemented = sorted(set(implemented) | set(semantic_implemented))

    # Fallback: if the model did not emit TC IDs, map runnable test blocks to
    # required in-scope IDs. JUnit 5 package-private @Test methods count here.
    if not all_implemented and planned:
        test_count = count_test_blocks(generated_code)
        if test_count > 0:
            fallback_pool = bound_case_ids or [
                case_id
                for case_id in planned
                if case_id not in out_of_scope_case_ids and case_id not in ambiguous_case_ids
            ]
            all_implemented = fallback_pool[:test_count]

    if bound_case_ids:
        in_scope_planned = bound_case_ids
    else:
        in_scope_planned = [
            case_id
            for case_id in planned
            if case_id not in out_of_scope_case_ids and case_id not in ambiguous_case_ids
        ]

    missing = [case_id for case_id in planned if case_id not in all_implemented]
    missing_in_scope = [case_id for case_id in in_scope_planned if case_id not in all_implemented]
    implemented_in_scope = [case_id for case_id in in_scope_planned if case_id in all_implemented]

    return {
        "planned_cases": len(planned),
        "implemented_cases": len(all_implemented),
        "required_in_scope_cases": len(in_scope_planned),
        "implemented_in_scope_cases": len(implemented_in_scope),
        "missing_in_scope_case_ids": missing_in_scope,
        "out_of_scope_case_ids": out_of_scope_case_ids,
        "ambiguous_case_ids": ambiguous_case_ids,
        "semantically_implemented_case_ids": semantic_implemented,
        "missing_case_ids": missing,
        "raw_missing_case_ids": missing,
        "case_bindings": case_bindings,
        "case_binding_reasons": case_reasons,
    }
