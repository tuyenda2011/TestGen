import json

from testgen.core.scope_validator import validate_plan_scope
from testgen.core.source_analyzer import analyze_source_symbols
from testgen.core.test_case_traceability import count_test_blocks, evaluate_traceability


def test_java_source_analyzer_extracts_public_symbols():
    source = """
public class BankAccount {
    private double balance;

    public BankAccount(String accountNumber, double initialBalance) {}
    public void deposit(double amount) {}
    public double getBalance() { return balance; }
    private void checkActive() {}
}
"""

    index = analyze_source_symbols(source)

    assert index["language"] == "java"
    assert "BankAccount" in index["names"]
    assert "deposit" in index["names"]
    assert "BankAccount.deposit" in index["names"]
    assert "checkActive" not in index["names"]


def test_javascript_source_analyzer_exposes_only_commonjs_exports():
    source = """
function roundMoney(value) {
  return Math.round(value * 100) / 100;
}

function finalTotal(order) {
  return roundMoney(order.subtotal);
}

module.exports = {
  finalTotal,
};
"""

    index = analyze_source_symbols(source)

    assert index["language"] == "javascript"
    assert "finalTotal" in index["names"]
    assert "roundMoney" not in index["names"]
    assert index["public_exports"] == ["finalTotal"]


def test_jest_scope_validator_treats_private_helper_cases_as_not_required_in_scope():
    source_index = analyze_source_symbols(
        """
function roundMoney(value) {
  return Math.round(value * 100) / 100;
}

function finalTotal(order) {
  return roundMoney(order.subtotal);
}

module.exports = {
  finalTotal,
};
"""
    )
    plan = {
        "test_scenarios": [
            {
                "id": "TC-001",
                "title": "finalTotal rounds the final amount",
                "target_function": "finalTotal",
                "expected_result": "Rounded total",
            },
            {
                "id": "TC-002",
                "title": "roundMoney rounds positive number to two decimals",
                "target_function": "roundMoney",
                "expected_result": "Rounded helper result",
            },
        ]
    }

    scoped = json.loads(validate_plan_scope(json.dumps(plan), source_index))
    scope = scoped["scope_validation"]
    generated = """
const target = require('./source_under_test');

test('finalTotal rounds the final amount - TC-001', () => {
  expect(target.finalTotal({ subtotal: 1.235 })).toBe(1.24);
});
"""

    result = evaluate_traceability(json.dumps(scoped), generated)

    assert scope["bound_cases"] == ["TC-001"]
    assert scope["ambiguous_cases"] == ["TC-002"]
    assert result["missing_in_scope_case_ids"] == []
    assert result["raw_missing_case_ids"] == ["TC-002"]


def test_junit_scope_validator_marks_framework_cases_out_of_scope():
    source_index = analyze_source_symbols(
        """
public class BankAccount {
    public BankAccount(String accountNumber, double initialBalance) {}
    public void deposit(double amount) {}
}
"""
    )
    plan = {
        "test_scenarios": [
            {
                "id": "TC-001",
                "title": "Ki?m tra @TempDir static Path du?c chia s? gi?a c�c test method",
                "expected_result": "Files.write succeeds",
            },
            {
                "id": "TC-002",
                "title": "Deposit increases balance",
                "target_function": "deposit",
                "expected_result": "Balance increases",
            },
        ]
    }

    scoped = json.loads(validate_plan_scope(json.dumps(plan, ensure_ascii=False), source_index))
    scope = scoped["scope_validation"]

    assert scope["out_of_scope_cases"] == ["TC-001"]
    assert scope["bound_cases"] == ["TC-002"]
    assert scoped["test_scenarios"][0]["source_binding_status"] == "out_of_scope"
    assert scoped["test_scenarios"][1]["source_binding_symbols"]


def test_traceability_ignores_out_of_scope_junit_cases_and_counts_junit5_tests():
    test_plan = {
        "test_scenarios": [
            {"id": "TC-001", "title": "TempDir migration"},
            {"id": "TC-002", "title": "Deposit increases balance"},
        ],
        "scope_validation": {
            "bound_cases": ["TC-002"],
            "out_of_scope_cases": ["TC-001"],
            "ambiguous_cases": [],
            "case_bindings": {"TC-002": ["BankAccount.deposit", "deposit"]},
            "case_reasons": {
                "TC-001": "Refers to JUnit framework/runtime feature outside source API: @tempdir"
            },
        },
    }
    generated = """
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BankAccountTest {
    @Test
    void coversDeposit() {
        BankAccount account = new BankAccount("A1", 10.0);
        account.deposit(5.0);
        assertEquals(15.0, account.getBalance(), 0.001);
    }
}
"""

    result = evaluate_traceability(json.dumps(test_plan), generated)

    assert count_test_blocks(generated) == 1
    assert result["missing_in_scope_case_ids"] == []
    assert result["out_of_scope_case_ids"] == ["TC-001"]
    assert result["raw_missing_case_ids"] == ["TC-001"]
    assert result["semantically_implemented_case_ids"] == ["TC-002"]
