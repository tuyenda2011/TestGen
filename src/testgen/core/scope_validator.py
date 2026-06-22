import json
import re
from typing import Any, Dict


JUNIT_FRAMEWORK_MARKERS = {
    "tempdir",
    "path",
    "files",
    "nio",
    "category",
    "runwith",
    "rule",
    "classrule",
    "registerextension",
    "extendwith",
    "tag",
    "parameterizedtest",
    "valuesource",
    "factory",
    "book",
    "listwriter",
}

JUNIT_MARKER_PHRASES = (
    "@tempdir",
    "java.nio",
    "java.io",
    "files.",
    "junit 4",
    "junit4",
    "migration",
    "@category",
    "@runwith",
    "@rule",
    "@classrule",
    "@registerextension",
    "@extendwith",
    "@tag",
    "@parameterizedtest",
    "@valuesource",
    "factory conversion",
)


def _normalize_case_id(value: object) -> str:
    match = re.search(r"(?i)tc[-_]?(\d{1,4})", str(value or ""))
    return f"TC-{match.group(1).zfill(3)}" if match else str(value or "").strip()


def _simple_symbol_name(name: str) -> str:
    return (name or "").rsplit(".", 1)[-1].lower()


def _case_text(case: dict[str, Any]) -> str:
    fields = [
        "target_function",
        "component",
        "title",
        "description",
        "preconditions",
        "test_data",
        "expected_result",
    ]
    return " ".join(str(case.get(field, "") or "") for field in fields).lower()


def _is_junit_framework_case(text: str, words: set[str], source_words: set[str]) -> str:
    phrase_hits = [phrase for phrase in JUNIT_MARKER_PHRASES if phrase in text]
    marker_hits = sorted((words & JUNIT_FRAMEWORK_MARKERS) - source_words)
    if not phrase_hits and not marker_hits:
        return ""
    hits = phrase_hits[:3] + marker_hits[:5]
    return "Refers to JUnit framework/runtime feature outside source API: " + ", ".join(hits)


def validate_plan_scope(test_plan_json: str, source_index: Dict[str, Any]) -> str:
    """
    Attach scope_validation to a test plan by comparing planned cases with
    symbols found in the runtime source under test.
    """
    if not test_plan_json:
        return ""

    try:
        data = json.loads(test_plan_json)
    except Exception:
        return test_plan_json

    source_names = set(source_index.get("names", []))
    source_language = str(source_index.get("language", "") or "").lower()
    lower_source_names = {str(name).lower() for name in source_names}
    simple_source_names = {_simple_symbol_name(name) for name in lower_source_names}

    scenarios = data.get("test_scenarios") or data.get("test_cases") or []

    bound_cases: list[str] = []
    out_of_scope_cases: list[str] = []
    ambiguous_cases: list[str] = []
    case_bindings: dict[str, list[str]] = {}
    case_reasons: dict[str, str] = {}

    for case in scenarios:
        if not isinstance(case, dict):
            continue

        case_id = _normalize_case_id(case.get("id", ""))
        if not case_id:
            continue

        text_to_search = _case_text(case)
        words = set(re.findall(r"\b\w+\b", text_to_search))

        if source_language == "java":
            reason = _is_junit_framework_case(text_to_search, words, simple_source_names)
            if reason:
                out_of_scope_cases.append(case_id)
                case["source_binding_status"] = "out_of_scope"
                case["source_binding_reason"] = reason
                case_reasons[case_id] = reason
                continue

        if "pytester" in words or "makeconftest" in words or "makepyfile" in words:
            reason = "Refers to out-of-scope testing framework APIs (pytester)"
            out_of_scope_cases.append(case_id)
            case["source_binding_status"] = "out_of_scope"
            case["source_binding_reason"] = reason
            case_reasons[case_id] = reason
            continue

        matched_symbols: list[str] = []
        for name in lower_source_names:
            simple_name = _simple_symbol_name(name)
            compact_name = name.replace("_", "")
            compact_simple = simple_name.replace("_", "")
            if name in words or compact_name in words or simple_name in words or compact_simple in words:
                matched_symbols.append(name)

        if matched_symbols:
            bindings = sorted(set(matched_symbols))
            bound_cases.append(case_id)
            case["source_binding_status"] = "bound"
            case["source_binding_symbols"] = bindings
            case_bindings[case_id] = bindings
            continue

        if len(source_names) > 0:
            reason = (
                "Does not reference any exported source symbol"
                if source_language == "javascript"
                else "Does not reference any public source symbol"
            )
            ambiguous_cases.append(case_id)
            case["source_binding_status"] = "ambiguous"
            case["source_binding_reason"] = reason
            case_reasons[case_id] = reason
        else:
            bound_cases.append(case_id)
            case["source_binding_status"] = "bound"

    scope_validation = {
        "bound_cases": bound_cases,
        "out_of_scope_cases": out_of_scope_cases,
        "ambiguous_cases": ambiguous_cases,
        "case_bindings": case_bindings,
        "case_reasons": case_reasons,
        "source_symbols": sorted(source_names),
        "warning": (
            f"{len(out_of_scope_cases)} planned cases reference APIs not present in source"
            if out_of_scope_cases
            else ""
        ),
    }

    data["scope_validation"] = scope_validation
    return json.dumps(data, indent=2, ensure_ascii=False)
