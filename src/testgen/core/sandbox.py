from __future__ import annotations

import ast
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SandboxRule:
    pattern: re.Pattern[str]
    reason: str


_COMMON_RULES = [
    SandboxRule(re.compile(r"\b(?:rm\s+-rf|curl\s+|wget\s+|powershell\b|cmd\.exe\b)", re.IGNORECASE), "shell/network command"),
    SandboxRule(re.compile(r"\b(?:http|https|ftp)://", re.IGNORECASE), "network URL literal"),
]

_PYTHON_RULES = [
    SandboxRule(re.compile(r"\b(?:eval|exec|__import__|compile|open|input)\s*\(", re.IGNORECASE), "dangerous Python builtin"),
    SandboxRule(re.compile(r"\b(?:os|subprocess|shutil|socket)\s*\.", re.IGNORECASE), "dangerous Python module call"),
]

_JAVASCRIPT_RULES = [
    SandboxRule(re.compile(r"\brequire\s*\(\s*['\"](?:child_process|fs|http|https|net|dgram)['\"]", re.IGNORECASE), "dangerous Node module"),
    SandboxRule(re.compile(r"\b(?:child_process|process\.env|process\.exit)\b", re.IGNORECASE), "dangerous JavaScript API"),
    SandboxRule(re.compile(r"\beval\s*\(", re.IGNORECASE), "dangerous JavaScript eval"),
    SandboxRule(re.compile(r"\bFunction\s*\("), "dangerous JavaScript Function constructor"),
    SandboxRule(re.compile(r"\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(", re.IGNORECASE), "network JavaScript API"),
]

_JAVA_RULES = [
    SandboxRule(re.compile(r"\b(?:Runtime\.getRuntime|ProcessBuilder|System\.exit)\b", re.IGNORECASE), "dangerous Java API"),
    SandboxRule(re.compile(r"\bimport\s+java\.(?:io|nio|net)\.", re.IGNORECASE), "dangerous Java package"),
    SandboxRule(re.compile(r"\bFiles\.(?:delete|write|copy|move)\s*\(", re.IGNORECASE), "dangerous Java file operation"),
]

_PYTHON_BLOCKED_IMPORTS = {"os", "subprocess", "shutil", "socket"}
_PYTHON_BLOCKED_CALLS = {
    "__import__",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "input",
    "locals",
    "open",
    "setattr",
}
_PYTHON_BLOCKED_ATTRIBUTES = {
    "call",
    "check_call",
    "check_output",
    "connect",
    "move",
    "Popen",
    "rename",
    "request",
    "rmtree",
    "run",
    "system",
    "unlink",
    "urlopen",
}


def _regex_rules_for_language(language: str) -> list[SandboxRule]:
    normalized = (language or "").strip().lower()
    rules = list(_COMMON_RULES)
    if normalized == "python":
        rules.extend(_PYTHON_RULES)
    elif normalized in {"javascript", "js", "typescript", "ts", "postman"}:
        rules.extend(_JAVASCRIPT_RULES)
    elif normalized == "java":
        rules.extend(_JAVA_RULES)
    return rules


def _regex_check(code: str, language: str, allow_e2e: bool = False) -> tuple[bool, str]:
    for rule in _regex_rules_for_language(language):
        if allow_e2e and rule.reason == "network URL literal":
            continue
        if rule.pattern.search(code or ""):
            return False, f"Regex sandbox blocked {rule.reason}."
    return True, ""


def _python_ast_check(code: str, allow_e2e: bool = False) -> tuple[bool, str]:
    try:
        tree = ast.parse(code or "")
    except SyntaxError:
        return True, ""

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                root_name = (alias.name or "").split(".", 1)[0]
                if root_name in _PYTHON_BLOCKED_IMPORTS:
                    return False, f"Blocked unsafe Python import: {root_name}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in _PYTHON_BLOCKED_CALLS:
                return False, f"Blocked unsafe Python call: {node.func.id}()"
            if isinstance(node.func, ast.Attribute) and node.func.attr in _PYTHON_BLOCKED_ATTRIBUTES:
                return False, f"Blocked unsafe Python attribute call: {node.func.attr}()"
    return True, ""


def validate_code_safety(code: str, *, language: str, label: str = "code", allow_e2e: bool = False) -> tuple[bool, str]:
    ok, reason = _regex_check(code, language, allow_e2e)
    if not ok:
        return False, f"{label}: {reason}"

    if (language or "").strip().lower() == "python":
        ok, reason = _python_ast_check(code, allow_e2e)
        if not ok:
            return False, f"{label}: {reason}"

    return True, ""


def is_safe_python_code(code: str, allow_e2e: bool = False) -> tuple[bool, str]:
    return validate_code_safety(code, language="python", label="Python test code", allow_e2e=allow_e2e)
