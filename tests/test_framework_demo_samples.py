from __future__ import annotations

from pathlib import Path

import pytest

from testgen.core.language_guard import detect_section_language, validate_framework_sections


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("framework", "relative_path", "expected_language"),
    [
        ("pytest", "examples/demo/framework_samples/pytest/pytest_order_pricing_demo.py", "python"),
        ("Selenium", "examples/demo/framework_samples/selenium/selenium_checkout_demo.py", "python"),
        ("Playwright", "examples/demo/framework_samples/playwright/playwright_checkout_demo.py", "python"),
        ("JUnit", "examples/demo/framework_samples/junit/OrderPricingJUnitDemo.java", "java"),
        ("Jest", "examples/demo/framework_samples/jest/orderPricing.jest.demo.js", "javascript"),
        (
            "Postman script",
            "examples/demo/framework_samples/postman/order-pricing.postman_collection.json",
            "javascript",
        ),
        ("Postman script", "examples/demo/framework_samples/postman/postman_script_demo.js", "javascript"),
    ],
)
def test_framework_demo_samples_match_language_guard(
    framework: str,
    relative_path: str,
    expected_language: str,
) -> None:
    path = ROOT / relative_path
    text = path.read_text(encoding="utf-8")

    assert detect_section_language(path.name, text) == expected_language
    assert validate_framework_sections(framework, [(path.name, text)]) is None
