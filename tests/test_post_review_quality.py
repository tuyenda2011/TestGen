from __future__ import annotations

import json

from testgen.core.post_review_quality import assess_post_review_quality


def test_post_review_quality_keeps_coverage_gate_for_unit_frameworks():
    result = assess_post_review_quality(
        framework="Jest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 92.0,
            "execution_issue": {"type": "none"},
        },
        review_report="## Review\nKhong phot hi?n.",
    )

    assert result["quality_gate"] == "coverage"
    assert result["coverage_score"] > 0
    assert result["flow_or_api_assertion_score"] == 0
    assert result["verdict"] == "Đạt"


def test_post_review_quality_uses_flow_gate_for_e2e_api():
    result = assess_post_review_quality(
        framework="Selenium",
        execution_summary={
            "passed": True,
            "coverage_supported": False,
            "coverage_percent": 0.0,
            "quality_gate": "e2e_flow_assertions",
            "source_path": "source_under_test.html",
            "e2e_static_quality": {
                "assertion_count": 2,
                "opens_target_fixture": True,
                "uses_sleep": False,
            },
            "execution_issue": {"type": "none"},
        },
        review_report="## Review\nKhong phot hi?n.",
    )

    assert result["quality_gate"] == "flow_api_assertions"
    assert result["coverage_score"] == 0
    assert result["flow_or_api_assertion_score"] == 25
    assert result["coverage_supported"] is False


def test_post_review_quality_blocks_e2e_without_meaningful_ui_assertions():
    result = assess_post_review_quality(
        framework="Selenium",
        execution_summary={
            "passed": True,
            "coverage_supported": False,
            "coverage_percent": 0.0,
            "quality_gate": "e2e_flow_assertions",
            "source_path": "source_under_test.html",
            "e2e_static_quality": {
                "assertion_count": 1,
                "meaningful_assertion_count": 0,
                "opens_target_fixture": True,
                "uses_sleep": False,
            },
            "execution_issue": {"type": "none"},
        },
        review_report="## Review\nKhong phot hi?n.",
    )

    assert result["verdict"] != "Đạt"
    assert any("UI/E2E" in item for item in result["blocking_findings"])


def test_post_review_quality_blocks_critical_review_findings():
    result = assess_post_review_quality(
        framework="pytest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 95.0,
            "execution_issue": {"type": "none"},
        },
        review_report="""
## L?i nghiem trong
- Import sai target Calculator.
""",
    )

    assert result["verdict"] == "Rủi ro cao"
    assert result["score"] < 50
    assert result["blocking_findings"]


def test_post_review_quality_flags_weak_postman_assertions():
    result = assess_post_review_quality(
        framework="Postman script",
        execution_summary={
            "passed": False,
            "coverage_supported": False,
            "coverage_percent": 0.0,
            "postman_static_quality": {
                "assertions_total": 1,
                "status_code_assert_present": True,
                "body_assert_present": False,
            },
            "execution_issue": {"type": "weak_postman_assertion"},
        },
        review_report="",
    )

    assert result["quality_gate"] == "flow_api_assertions"
    assert result["verdict"] == "Rủi ro cao"
    assert any("weak_postman_assertion" in item for item in result["blocking_findings"])
    assert any("body/schema" in item for item in result["recommended_action"])


def test_jest_post_review_ignores_missing_private_helper_case_when_not_in_scope():
    plan = {
        "test_scenarios": [
            {"id": "TC-001", "title": "finalTotal rounds total", "target_function": "finalTotal"},
            {"id": "TC-002", "title": "roundMoney rounds positive number", "target_function": "roundMoney"},
        ],
        "scope_validation": {
            "bound_cases": ["TC-001"],
            "out_of_scope_cases": [],
            "ambiguous_cases": ["TC-002"],
            "case_bindings": {"TC-001": ["finalTotal"]},
        },
    }

    result = assess_post_review_quality(
        framework="Jest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 96.0,
            "execution_issue": {"type": "none"},
            "jest_static_quality": {
                "public_exports": ["finalTotal"],
                "used_target_members": ["finalTotal"],
                "unknown_target_members": [],
                "monkey_patches": [],
                "fallback_implementations": [],
                "reimplemented_exports": [],
            },
        },
        review_report="""
## Missing tests
- Missing TC-002 roundMoney helper case.
""",
        generated_code="""
const target = require('./source_under_test');
test('finalTotal rounds total - TC-001', () => expect(target.finalTotal({ subtotal: 1.235 })).toBe(1.24));
""",
        test_plan_json=json.dumps(plan),
    )

    assert result["traceability"]["missing_in_scope_case_ids"] == []
    assert result["review_findings"]["missing_tests"] == []
    assert result["review_findings"]["ignored_missing_tests"]
    assert result["score"] >= 80
    assert result["blocking_findings"] == []


def test_jest_post_review_ignores_mojibake_tc_ids_for_ambiguous_helper_cases():
    plan = {
        "test_scenarios": [
            {"id": "TC-001", "title": "finalTotal rounds total", "target_function": "finalTotal"},
            {"id": "TC-003", "title": "roundMoney rounds down", "target_function": "roundMoney"},
            {"id": "TC-004", "title": "roundMoney rounds up", "target_function": "roundMoney"},
        ],
        "scope_validation": {
            "bound_cases": ["TC-001"],
            "out_of_scope_cases": [],
            "ambiguous_cases": ["TC-003", "TC-004"],
            "case_bindings": {"TC-001": ["finalTotal"]},
            "case_reasons": {
                "TC-003": "Does not reference any exported source symbol",
                "TC-004": "Does not reference any exported source symbol",
            },
        },
    }

    result = assess_post_review_quality(
        framework="Jest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 96.66,
            "execution_issue": {"type": "none"},
            "jest_static_quality": {
                "public_exports": ["finalTotal"],
                "used_target_members": ["finalTotal"],
                "unknown_target_members": [],
                "monkey_patches": [],
                "fallback_implementations": [],
                "reimplemented_exports": [],
            },
        },
        review_report=(
            "## Test con thieu\n"
            "- Thieu TC\u2011003 va TC\u00e2\u20ac\u2018004 cho helper roundMoney."
        ),
        generated_code=(
            "const target = require('./source_under_test');\n"
            "test('TC-001 finalTotal rounds total', () => expect(target.finalTotal({ subtotal: 1.235 })).toBe(1.24));"
        ),
        test_plan_json=json.dumps(plan),
    )

    assert result["traceability"]["missing_in_scope_case_ids"] == []
    assert result["review_findings"]["missing_tests"] == []
    assert result["review_findings"]["ignored_missing_tests"]
    assert result["score"] >= 80


def test_jest_post_review_ignores_non_public_helper_followup_bullets():
    plan = {
        "test_scenarios": [
            {"id": "TC-001", "title": "normalizeLabel trims input", "target_function": "normalizeLabel"},
            {"id": "TC-002", "title": "roundMoney rounds", "target_function": "roundMoney"},
            {"id": "TC-003", "title": "calculateDiscount VIP", "target_function": "calculateDiscount"},
        ],
        "scope_validation": {
            "bound_cases": ["TC-001", "TC-003"],
            "out_of_scope_cases": [],
            "ambiguous_cases": ["TC-002"],
            "case_bindings": {"TC-001": ["normalizeLabel"], "TC-003": ["calculateDiscount"]},
            "case_reasons": {"TC-002": "Does not reference any exported source symbol"},
        },
    }

    result = assess_post_review_quality(
        framework="Jest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 100.0,
            "execution_issue": {"type": "none"},
            "jest_static_quality": {
                "public_exports": ["calculateDiscount", "normalizeLabel"],
                "used_target_members": ["calculateDiscount", "normalizeLabel"],
                "unknown_target_members": [],
                "monkey_patches": [],
                "fallback_implementations": [],
                "reimplemented_exports": [],
            },
        },
        review_report="""
## Test con thieu
- **TC-002**: Kiem thu `roundMoney` khong duoc thuc thi ve ham nay **khong duoc export** trong `source_under_test.js`.
  - **B?ng ch?ng:** `module.exports` ch? bao g?m `calculateDiscount, normalizeLabel`; khong ce `roundMoney`.
  - **?nh hu?ng:** Khong ce kiem thu cho ham noi bo `roundMoney`, tuy nhien ve khong duoc export nen khong thu kiem thu truc ti?p t? ben ngoai.
  - **Cech s?a:** N?u mu?n kiem thu `roundMoney`, can **export** ham nay trong module ho?c vi?t test gien ti?p theng qua cec ham cang khai.

## R?i ro maintainability
- Cec test hi?n t?i ph? thu?c veo gie tri s? thuc ve s? d?ng `toBeCloseTo`, di?u ney ?n nhung can che e n?u logic lem tren thay d?i.
- Khong ce mock ho?c ph? thu?c ben ngoai, do de it rui ro flaky.
""",
        generated_code="""
const target = require('./source_under_test');
test('TC-001 normalizeLabel trims input', () => expect(target.normalizeLabel(' A ')).toBe('a'));
test('TC-003 calculateDiscount VIP', () => expect(target.calculateDiscount(300, 'vip')).toBeCloseTo(36));
""",
        test_plan_json=json.dumps(plan),
    )

    assert result["traceability"]["missing_in_scope_case_ids"] == []
    assert result["review_findings"]["missing_tests"] == []
    assert len(result["review_findings"]["ignored_missing_tests"]) == 1
    assert len(result["review_findings"]["maintainability"]) == 1
    assert result["score"] > 90


def test_jest_post_review_ignores_stale_findings_contradicted_by_generated_code():
    plan = {
        "test_scenarios": [{"id": f"TC-{i:03d}"} for i in range(1, 19)],
        "scope_validation": {
            "bound_cases": [
                "TC-001",
                "TC-004",
                "TC-005",
                "TC-006",
                "TC-007",
                "TC-008",
                "TC-009",
                "TC-010",
                "TC-011",
                "TC-012",
                "TC-013",
                "TC-014",
                "TC-015",
                "TC-016",
                "TC-017",
                "TC-018",
            ],
            "out_of_scope_cases": [],
            "ambiguous_cases": ["TC-002", "TC-003"],
            "case_bindings": {},
            "case_reasons": {
                "TC-002": "Does not reference any exported source symbol",
                "TC-003": "Does not reference any exported source symbol",
            },
        },
    }
    generated_code = """
const target = require('./source_under_test');
// TC-004 TC-005 TC-006 TC-007 TC-008 TC-009 TC-010 TC-011 are covered by calculateDiscount cases in the full generated file.
test('TC-001 normalizeLabel', () => expect(target.normalizeLabel(' A ')).toBe('a'));
test('TC-002 normalizeLabel empty', () => expect(target.normalizeLabel('   ')).toBe(''));
test('TC-003 normalizeLabel non-strong', () => expect(() => target.normalizeLabel(null)).toThrow());
test('TC-012 finalTotal floors', () => expect(target.finalTotal({subtotal:20, customerTier:'standard', storeCredit:30, weightKg:1, destination:'domestic', fragile:false})).toBe(0));
test('TC-013 finalTotal vip', () => expect(target.finalTotal({subtotal:200, customerTier:'vip', storeCredit:20, weightKg:3, destination:'domestic', fragile:false})).toBe(161));
test('TC-014 shippingFee weight', () => expect(() => target.shippingFee(0, 'domestic')).toThrow());
test('TC-015 shippingFee destination', () => expect(() => target.shippingFee(2, 'moon')).toThrow());
test('TC-016 shippingFee light', () => expect(target.shippingFee(4, 'domestic', false)).toBe(5));
test('TC-017 shippingFee medium fragile', () => expect(target.shippingFee(10, 'domestic', true)).toBe(22.5));
test('TC-018 shippingFee heavy intl', () => expect(target.shippingFee(25, 'international', false)).toBe(43));
"""

    result = assess_post_review_quality(
        framework="Jest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 100.0,
            "execution_issue": {"type": "none"},
            "jest_static_quality": {
                "public_exports": ["calculateDiscount", "finalTotal", "normalizeLabel", "shippingFee"],
                "used_target_members": ["calculateDiscount", "finalTotal", "normalizeLabel", "shippingFee"],
                "unknown_target_members": [],
                "monkey_patches": [],
                "fallback_implementations": [],
                "reimplemented_exports": [],
            },
        },
        review_report="""
## Test con thieu
- **Kiem thu `shippingFee`**: Khong ce test cho cec tru?ng hop:
  - Tr?ng luong <= 0 -> nem loi.
  - Destination khong hop l? -> nem loi.
  - Kiem thu tenh pho cho cec m?c trong luong khec nhau.
- **Kiem thu `normalizeLabel`**: Ch? ce mat test (TC-001).

## Assertion y?u
- **TC-012 & TC-013**: M?c de ce `jest.spyOn` d? mock `shippingFee`, mock khong ?nh hu?ng ve `finalTotal` g?i ham `shippingFee` noi bo.

## R?i ro maintainability
- **Mock khong hi?u qu?** (TC-012, TC-013) t?o ra false sense of coverage.
""",
        generated_code=generated_code,
        test_plan_json=json.dumps(plan),
    )

    assert result["traceability"]["missing_in_scope_case_ids"] == []
    assert result["review_findings"]["missing_tests"] == []
    assert result["review_findings"]["weak_assertions"] == []
    assert result["review_findings"]["maintainability"] == []
    assert result["review_findings"]["ignored_stale_findings"]
    assert result["score"] > 90


def test_selenium_post_review_ignores_stale_missing_findings_when_final_artifacts_cover_cases():
    generated_code = """
def test_TC_003_shippingFee_weight_over_20(driver):
    weight.send_keys("25")
    assert "43" in total.text

def test_TC_003_shippingFee_fragile_addition(driver):
    fragile.click()
    assert "fragile" in summary.text.lower()

def test_TC_003_shippingFee_weight_zero_error(driver):
    weight.send_keys("0")
    assert "Weight must be greater than 0" in error.text

def test_TC_003_shippingFee_weight_negative_error(driver):
    weight.send_keys("-1")
    assert "Weight must be greater than 0" in error.text

def test_TC_004_submit_prevents_default(driver):
    submit.click()
    assert "checkout" in driver.current_url

def test_TC_004_total_calculation_with_credit(driver):
    credit.send_keys("20")
    assert "161" in total.text
"""

    result = assess_post_review_quality(
        framework="Selenium",
        execution_summary={
            "passed": True,
            "coverage_supported": False,
            "coverage_percent": 0.0,
            "execution_issue": {"type": "none"},
            "source_path": r"D:\Chatbot\outputs\runs\tmp_execution\run\final\source_under_test.html",
            "e2e_failure_log_path": r"D:\Chatbot\outputs\runs\tmp_execution\run\final\pytest.log",
            "e2e_static_quality": {
                "assertion_count": 6,
                "meaningful_assertion_count": 6,
                "uses_sleep": False,
                "negative_or_boundary_evidence": True,
            },
            "collection_output": """
test_generated.py::test_TC_003_shippingFee_weight_over_20
test_generated.py::test_TC_003_shippingFee_fragile_addition
test_generated.py::test_TC_003_shippingFee_weight_zero_error
test_generated.py::test_TC_003_shippingFee_weight_negative_error
test_generated.py::test_TC_004_submit_prevents_default
test_generated.py::test_TC_004_total_calculation_with_credit
""",
        },
        review_report="""
## Test con thieu
- Thieu kiem tra loi weight <= 0.
- Thieu kiem tra khi fragile duoc ch?n.
- Thieu kiem tra khi weight > 20.
- Thieu kiem tra ?nh hu?ng c?a credit.
- Thieu kiem tra event.preventDefault().

## Maintainability
- DOM mutation trong setup ce thu khe bao tre.
- M?t s? expected total dang hard-code.
""",
        generated_code=generated_code,
        test_plan_json=json.dumps(
            {
                "test_scenarios": [
                    {"id": "TC-003", "title": "shipping fee boundaries"},
                    {"id": "TC-004", "title": "checkout submit total"},
                ]
            }
        ),
    )

    assert result["review_findings"]["missing_tests"] == []
    assert len(result["review_findings"]["ignored_stale_findings"]) == 5
    assert result["blocking_findings"] == []
    assert result["score"] >= 90


def test_playwright_post_review_ignores_runtime_contract_and_coverage_noise():
    generated_code = """
from pathlib import Path

def test_checkout_boundaries(page):
    page.goto((Path.cwd() / "source_under_test.html").resolve().as_uri())
    page.fill("#weight", "0")
    page.click("#calculate")
    expect(page.locator("#error")).to_have_text("weight must be greater than zero")
"""

    result = assess_post_review_quality(
        framework="Playwright",
        execution_summary={
            "passed": True,
            "coverage_supported": False,
            "coverage_percent": 0.0,
            "execution_issue": {"type": "coverage_artifact_missing"},
            "source_path": r"D:\Chatbot\outputs\runs\tmp_execution\run\final\source_under_test.html",
            "e2e_failure_log_path": r"D:\Chatbot\outputs\runs\tmp_execution\run\final\pytest.log",
            "e2e_static_quality": {
                "assertion_count": 1,
                "meaningful_assertion_count": 1,
                "uses_sleep": False,
                "negative_or_boundary_evidence": True,
            },
            "collection_output": "test_generated.py::test_checkout_boundaries",
        },
        review_report="""
## L?i nghiem trong
- eu?ng d?n HTML sai: source_under_test.html khong t?n t?i, file thut le ui_checkout_fixture.html.

## Test con thieu
- K?t qu? ch?y pass nhung coverage artifact missing nen thieu coverage.
- Thieu kiem tra loi weight <= 0.
""",
        generated_code=generated_code,
    )

    assert result["issue_type"] == "none"
    assert result["review_findings"]["critical"] == []
    assert result["review_findings"]["missing_tests"] == []
    assert result["blocking_findings"] == []
    assert result["score"] >= 90


def test_postman_post_review_ignores_schema_auth_and_hardcoded_noise_when_not_required():
    generated_code = """
pm.test("status is OK", function () { pm.response.to.have.status(200); });
pm.test("response has expected total", function () {
  const body = pm.response.json();
  pm.expect(body.total).to.eql(100.5);
  pm.expect(body.diagnostics.discount).to.eql(12);
});
pm.test("validation error", function () {
  const body = pm.response.json();
  pm.expect(body.error).to.include("subtotal");
});
"""

    result = assess_post_review_quality(
        framework="Postman script",
        execution_summary={
            "passed": True,
            "coverage_supported": False,
            "coverage_percent": 0.0,
            "execution_issue": {"type": "none"},
            "postman_summary_path": r"D:\Chatbot\outputs\runs\tmp_execution\run\postman_summary.json",
            "report_path": r"D:\Chatbot\outputs\runs\tmp_execution\run\newman_report.json",
            "postman_static_quality": {
                "assertions_total": 3,
                "status_code_assert_present": True,
                "body_assert_present": True,
                "schema_assert_present": False,
            },
        },
        review_report="""
## Test con thieu
- Thieu kiem tra schema JSON phan hoi.
- Thieu kiem thu bao mat / xec thuc token.

## Assertion y?u
- TC-001 hard-coded expected total 100.5.
- TC-002 ch? kiem tra body.error include subtotal.

## Maintainability
- Hard-coded gie tri trong assertion.
""",
        generated_code=generated_code,
        requirement_json=json.dumps(
            {
                "features": ["quote order pricing"],
                "validations": ["missing subtotal returns validation error"],
            }
        ),
    )

    assert result["review_findings"]["missing_tests"] == []
    assert result["review_findings"]["weak_assertions"] == []
    assert result["review_findings"]["maintainability"] == []
    assert result["blocking_findings"] == []
    assert result["score"] >= 90


def test_jest_post_review_blocks_non_exported_api_usage_from_static_quality():
    result = assess_post_review_quality(
        framework="Jest",
        execution_summary={
            "passed": True,
            "coverage_supported": True,
            "coverage_percent": 95.0,
            "execution_issue": {"type": "none"},
            "jest_static_quality": {
                "public_exports": ["finalTotal"],
                "used_target_members": ["finalTotal", "roundMoney"],
                "unknown_target_members": ["roundMoney"],
                "monkey_patches": [],
                "fallback_implementations": [],
                "reimplemented_exports": [],
            },
        },
        review_report="## Review\nKhông phát hiện.",
        generated_code="const target = require('./source_under_test'); test('x', () => expect(target.roundMoney(1.235)).toBe(1.24));",
    )

    assert result["score"] <= 69
    assert result["blocking_findings"]
    assert any("non-exported" in item for item in result["blocking_findings"])
    assert any("module.exports" in item for item in result["recommended_action"])


def test_jest_static_quality_does_not_affect_pytest_or_junit():
    for framework in ("pytest", "JUnit"):
        result = assess_post_review_quality(
            framework=framework,
            execution_summary={
                "passed": True,
                "coverage_supported": True,
                "coverage_percent": 95.0,
                "execution_issue": {"type": "none"},
                "jest_static_quality": {
                    "unknown_target_members": ["roundMoney"],
                    "monkey_patches": ["roundMoney"],
                    "fallback_implementations": ["roundMoney"],
                    "reimplemented_exports": ["finalTotal"],
                },
            },
            review_report="## Review\nKhong phat hien.",
        )

        assert result["framework"] == framework
        assert result["blocking_findings"] == []
        assert result["score"] >= 80
