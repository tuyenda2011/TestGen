"""pdf_sources.py ? C?u h?nh metadata v? rule l?c section cho PDF seed RAG.

P0.2: PDF_RAG_SOURCE_RULES ? mapping filename -> framework/priority/keywords.
P0.3: should_keep_pdf_page_or_section() ? l?c page nhi?u tru?c khi chunk.
"""
from __future__ import annotations

import re
from testgen.core.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# P0.2: Metadata rules cho t?ng PDF seed file
# ---------------------------------------------------------------------------

PDF_RAG_SOURCE_RULES: dict[str, dict[str, object]] = {
    "pytest_official.pdf": {
        "framework": "pytest",
        "priority": "P0",
        "source_type": "official_pdf",
        "include_keywords": [
            "assert",
            "raises",
            "fixture",
            "fixtures",
            "test discovery",
            "import",
            "conftest",
            "parametrize",
            "mark",
        ],
        "exclude_keywords": [
            "changelog",
            "license",
            "contributing",
            "contributors",
            "history",
            "index",
            "copyright",
            "release notes",
            "credits",
        ],
    },
    "pytest_cov_official.pdf": {
        "framework": "pytest",
        "priority": "P0",
        "source_type": "official_pdf",
        "include_keywords": [
            "coverage",
            "cov",
            "--cov",
            "missing lines",
            "json report",
            "branch",
            "omit",
        ],
        "exclude_keywords": [
            "changelog",
            "license",
            "contributing",
            "history",
            "index",
            "copyright",
        ],
    },
    "coveragepy_official.pdf": {
        "framework": "pytest",
        "priority": "P0",
        "source_type": "official_pdf",
        "include_keywords": [
            "coverage",
            "missing",
            "branch",
            "json",
            "report",
            "omit",
            "include",
        ],
        "exclude_keywords": [
            "changelog",
            "license",
            "contributing",
            "history",
            "index",
            "copyright",
            "release notes",
        ],
    },
    "junit5_user_guide_official.pdf": {
        "framework": "JUnit",
        "priority": "P0",
        "source_type": "official_pdf",
        "include_keywords": [
            "assertthrows",
            "assertequals",
            "asserttrue",
            "test",
            "@test",
            "annotation",
            "jupiter",
            "extension",
            "parameterized",
        ],
        "exclude_keywords": [
            "changelog",
            "license",
            "contributing",
            "history",
            "index",
            "copyright",
            "release notes",
        ],
    },
    "jest_official_docs.md": {
        "framework": "Jest",
        "priority": "P1",
        "source_type": "official_web_export",
        "include_keywords": ["jest", "expect", "mock"],
        "exclude_keywords": [],
    },
    "playwright_python_official_docs.md": {
        "framework": "Playwright",
        "priority": "P1",
        "source_type": "official_web_export",
        "include_keywords": ["playwright", "page", "locator"],
        "exclude_keywords": [],
    },
    "postman_focused_docs.md": {
        "framework": "Postman script",
        "priority": "P1",
        "source_type": "official_web_export",
        "include_keywords": ["postman", "pm", "test"],
        "exclude_keywords": [],
    },
    "selenium_python_bindings_unofficial.pdf": {
        "framework": "Selenium",
        "priority": "P1",
        "source_type": "unofficial_pdf",
        "include_keywords": [
            "webdriver",
            "selenium",
            "locator",
            "locators",
            "wait",
            "expected conditions",
            "find_element",
        ],
        "exclude_keywords": [
            "changelog",
            "license",
            "contributing",
            "contributors",
            "history",
            "index",
            "copyright",
            "release notes",
            "credits",
        ],
    },
}

# C?c exclude keyword m?c d?nh ?p d?ng cho m?i PDF n?u kh?ng c? rule ri?ng
_DEFAULT_EXCLUDE_KEYWORDS: list[str] = [
    "changelog",
    "license",
    "contributing",
    "contributors",
    "history",
    "index",
    "copyright",
    "release notes",
    "credits",
]


def get_source_rules(source_name: str) -> dict[str, object]:
    """Tra c?u rule cho PDF theo t?n file (case-insensitive).

    Tr? v? rule n?u t?m th?y, ngu?c l?i tr? v? dict r?ng.
    """
    lower = (source_name or "").strip().lower()
    for key, rules in PDF_RAG_SOURCE_RULES.items():
        if key.lower() == lower:
            return dict(rules)
    return {}


# ---------------------------------------------------------------------------
# P0.3: L?c section/page nhi?u tru?c khi chunk
# ---------------------------------------------------------------------------

def should_keep_pdf_page_or_section(text: str, rules: dict[str, object]) -> bool:
    """Quy?t d?nh c? gi? page/section n?y d? chunk v?o RAG kh?ng.

    Logic:
    1. N?u text r?ng ? b?.
    2. N?u ch?a exclude keyword m?nh ? b? (log).
    3. N?u c? include keyword ? gi?.
    4. N?u kh?ng c? include keyword nhung kh?ng c? exclude ? gi? (tr?nh l?c qu? m?nh).

    Args:
        text: N?i dung page/section.
        rules: Dict rule t? PDF_RAG_SOURCE_RULES (c? th? r?ng).

    Returns:
        True n?u n?n gi? l?i, False n?u n?n b?.
    """
    stripped = (text or "").strip()
    if not stripped:
        return False

    lower_text = stripped.lower()

    # L?y exclude keywords: uu ti?n t? rules, fallback v? default
    raw_excludes: list[str] = list(rules.get("exclude_keywords", []) or [])
    excludes = raw_excludes or _DEFAULT_EXCLUDE_KEYWORDS

    # Ki?m tra exclude ? ch? b? n?u keyword xu?t hi?n ? d?u trang ho?c chi?m do?n ch?nh
    for kw in excludes:
        kw_lower = kw.lower()
        # B? n?u keyword xu?t hi?n trong 200 k? t? d?u (ti?u d? trang/section)
        if kw_lower in lower_text[:200]:
            logger.debug("RAG PDF filter: b? page/section v? exclude keyword '%s'", kw)
            return False

    # Ki?m tra include keywords
    raw_includes: list[str] = list(rules.get("include_keywords", []) or [])
    if raw_includes:
        for kw in raw_includes:
            if kw.lower() in lower_text:
                return True
        # Có include list nhưng không match thì vẫn giữ nếu page ngắn/trung bình
        # (tránh bỏ page có nội dung liên quan nhưng không chứa đúng keyword)
        if len(stripped) < 500:
            return True
        logger.debug(
            "RAG PDF filter: page dài (%d chars) không có include keyword bị bỏ", len(stripped)
        )
        return False

    # Không có include list thì giữ mọi page không bị exclude
    return True


def filter_pdf_pages(
    pages: list[dict[str, object]],
    rules: dict[str, object],
) -> tuple[list[dict[str, object]], int, int]:
    """L?c danh s?ch page theo rules, log s? trang gi?/b?.

    Args:
        pages: K?t qu? t? load_pdf_pages().
        rules: Dict rule t? get_source_rules().

    Returns:
        Tuple (kept_pages, kept_count, dropped_count).
    """
    kept: list[dict[str, object]] = []
    dropped = 0
    for page in pages:
        text = str(page.get("text", "") or "")
        if should_keep_pdf_page_or_section(text, rules):
            kept.append(page)
        else:
            dropped += 1

    source_name = rules.get("source_name", "unknown")
    logger.info(
        "RAG PDF filter '%s': gi? %d/%d pages, b? %d pages.",
        source_name,
        len(kept),
        len(kept) + dropped,
        dropped,
    )
    return kept, len(kept), dropped
