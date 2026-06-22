from __future__ import annotations

import re
from pathlib import Path


_EXTENSION_LANGUAGE = {
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "javascript",
    ".tsx": "javascript",
    ".html": "html",
    ".css": "css",
}

_FRAMEWORK_LANGUAGE = {
    "pytest": "python",
    "JUnit": "java",
    "Jest": "javascript",
    "Postman script": "javascript",
    "Selenium": "python",
    "Playwright": "python",
}

_E2E_FRAMEWORKS = {"Selenium", "Playwright", "Postman script"}


def _detect_language_from_text(text: str) -> str:
    source = (text or "").strip()
    if not source:
        return "unknown"

    patterns = [
        ("python", r"(?m)^\s*(def\s+\w+\(|class\s+\w+|from\s+\w+\s+import\s+|import\s+\w+)"),
        ("python", r"if __name__\s*==\s*['\"]__main__['\"]"),
        ("java", r"\bpublic\s+class\b|\bimport\s+java\.|\bSystem\.out\.println\("),
        ("java", r"\b@Test\b|\bthrows\b"),
        ("javascript", r"\bfunction\s+\w+\s*\(|\b(const|let|var)\s+\w+\s*=|=>"),
        ("javascript", r"\bdescribe\s*\(|\bit\s*\(|\bpm\.test\s*\("),
    ]
    for language, pattern in patterns:
        if re.search(pattern, source):
            return language
    return "unknown"


def detect_section_language(name: str, text: str) -> str:
    suffix = Path((name or "").strip()).suffix.lower()
    extension_language = _EXTENSION_LANGUAGE.get(suffix)
    if extension_language:
        return extension_language
    return _detect_language_from_text(text)


def detect_languages(sections: list[tuple[str, str]]) -> set[str]:
    languages: set[str] = set()
    for name, text in sections:
        language = detect_section_language(name, text)
        if language != "unknown":
            languages.add(language)
    return languages


def expected_language_for_framework(framework: str) -> str | None:
    return _FRAMEWORK_LANGUAGE.get((framework or "").strip())


def validate_framework_sections(framework: str, sections: list[tuple[str, str]]) -> str | None:
    expected = expected_language_for_framework(framework)
    if not expected:
        return None

    if (framework or "").strip() in _E2E_FRAMEWORKS:
        return None

    languages = detect_languages(sections)
    if not languages:
        return None
    if expected in languages:
        return None

    detected = ", ".join(sorted(languages))
    return (
        f"Framework đã chọn là `{framework}` (mong đợi code `{expected}`), "
        f"nhưng code đầu vào đang giống `{detected}`. "
        "Hãy đổi framework hoặc đổi code đầu vào cho khớp."
    )