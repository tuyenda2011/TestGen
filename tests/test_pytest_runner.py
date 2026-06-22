from __future__ import annotations

import json
from types import SimpleNamespace

from testgen.executors import pytest_runner


def test_run_generated_pytest_with_coverage_parses_report(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        if "--collect-only" in command:
            return SimpleNamespace(returncode=0, stdout="test_generated.py::test_add\n", stderr="")
        coverage_path = tmp_path / "coverage.json"
        coverage_path.write_text(
            json.dumps(
                {
                    "files": {
                        "source_under_test.py": {
                            "summary": {"percent_covered": 85.5},
                            "missing_lines": [10, 11],
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert add(1,2)==3\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert result["passed"] is True
    assert result["collection_passed"] is True
    assert result["coverage_percent"] == 85.5
    assert result["missing_lines"] == [10, 11]
    assert result["coverage_ok"] is True
    assert result["execution_issue"]["type"] == "none"
    assert result["combined_report"]["coverage_percent"] == 85.5
    assert result["combined_report"]["missing_lines"] == [10, 11]
    assert result["combined_coverage_percent"] == 85.5
    assert result["pytest_log_path"]
    assert result["collection_log_path"]
    assert (tmp_path / "source_under_test.py").exists()
    assert (tmp_path / "test_generated.py").exists()
    assert (tmp_path / "pytest.log").exists()
    assert (tmp_path / "pytest_collect_only.log").exists()


def test_run_generated_pytest_with_coverage_handles_missing_report(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        if "--collect-only" in command:
            return SimpleNamespace(returncode=0, stdout="test_generated.py::test_add\n", stderr="")
        return SimpleNamespace(returncode=1, stdout="", stderr="failed")

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert add(1,2)==3\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert result["passed"] is False
    assert result["coverage_percent"] == 0.0
    assert result["missing_lines"] == []
    assert result["coverage_ok"] is False
    assert isinstance(result["diagnosis"], str)


def test_run_generated_pytest_with_coverage_diagnoses_missing_pytest_cov(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        if "--collect-only" in command:
            return SimpleNamespace(returncode=0, stdout="test_generated.py::test_add\n", stderr="")
        return SimpleNamespace(
            returncode=2,
            stdout="",
            stderr="pytest: error: unrecognized arguments: --cov=source_under_test",
        )

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert add(1,2)==3\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert "pytest-cov" in result["diagnosis"]


def test_run_generated_pytest_with_coverage_diagnoses_import_error(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        return SimpleNamespace(returncode=1, stdout="", stderr="ModuleNotFoundError: No module named 'x'")

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert add(1,2)==3\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert "ModuleNotFoundError" in result["diagnosis"]


def test_diagnoses_failed_assertion_even_when_coverage_exists(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        if "--collect-only" in command:
            return SimpleNamespace(returncode=0, stdout="test_generated.py::test_add\n", stderr="")
        coverage_path = tmp_path / "coverage.json"
        coverage_path.write_text(
            json.dumps(
                {
                    "files": {
                        "source_under_test.py": {
                            "summary": {"percent_covered": 100.0},
                            "missing_lines": [],
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=1, stdout="1 failed, 1 passed", stderr="")

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert add(1,2)==4\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert result["passed"] is False
    assert result["coverage_percent"] == 100.0
    assert result["execution_issue"]["type"] == "wrong_expected_value"
    assert "assertion" in result["diagnosis"]
    assert "1 failed" in result["failure_summary"]


def test_execution_result_score_prefers_passing_threshold_over_failed_high_coverage():
    failed_high_coverage = {"passed": False, "coverage_percent": 100.0}
    passed_threshold = {"passed": True, "coverage_percent": 83.0}

    assert pytest_runner.execution_result_score(passed_threshold, 80.0) > (
        pytest_runner.execution_result_score(failed_high_coverage, 80.0)
    )


def test_failure_summary_extracts_failed_node_and_exception(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        if "--collect-only" in command:
            return SimpleNamespace(returncode=0, stdout="test_generated.py::test_wallet_withdraw\n", stderr="")
        return SimpleNamespace(
            returncode=1,
            stdout=(
                "================================== FAILURES ===================================\n"
                "____________________________ test_wallet_withdraw ____________________________\n"
                ">       assert wallet.withdraw(50) == 10\n"
                "E       AssertionError: assert 20 == 10\n"
                "FAILED test_generated.py::test_wallet_withdraw - AssertionError: assert 20 == 10\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def withdraw():\n    return 20\n",
        generated_test_code="def test_wallet_withdraw():\n    assert withdraw() == 10\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert "test_wallet_withdraw" in result["failure_summary"]
    assert "AssertionError" in result["failure_summary"]


def test_collect_only_failure_returns_before_coverage(tmp_path, monkeypatch):
    calls = []

    def fake_run(command, capture_output, text, cwd, **kwargs):
        calls.append(command)
        return SimpleNamespace(
            returncode=2,
            stdout="",
            stderr="ERROR collecting test_generated.py\nSyntaxError: invalid syntax",
        )

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add(:\n    pass\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert result["passed"] is False
    assert result["collection_passed"] is False
    assert result["execution_issue"]["type"] == "syntax_error"
    assert result["coverage_path"] == ""
    assert result["collection_log_path"]
    assert (tmp_path / "pytest_collect_only.log").exists()
    assert "syntax" in result["diagnosis"].lower()
    assert len(calls) == 1
    assert "--collect-only" in calls[0]


def test_collect_only_timeout_keeps_diagnostics_and_log_path(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        raise pytest_runner.subprocess.TimeoutExpired(command, 15, output="partial collect")

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert True\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert result["passed"] is False
    assert result["collection_passed"] is False
    assert result["execution_issue"]["type"] == "collection_timeout"
    assert result["collection_log_path"]
    assert (tmp_path / "pytest_collect_only.log").exists()


def test_execution_timeout_keeps_collect_log_and_pytest_log(tmp_path, monkeypatch):
    def fake_run(command, capture_output, text, cwd, **kwargs):
        if "--collect-only" in command:
            return SimpleNamespace(returncode=0, stdout="test_generated.py::test_add\n", stderr="")
        raise pytest_runner.subprocess.TimeoutExpired(command, 15, output="partial run")

    monkeypatch.setattr(pytest_runner.subprocess, "run", fake_run)

    result = pytest_runner.run_generated_pytest_with_coverage(
        source_code_text="def add(a, b):\n    return a + b\n",
        generated_test_code="def test_add():\n    assert True\n",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    assert result["passed"] is False
    assert result["collection_passed"] is True
    assert result["execution_issue"]["type"] == "execution_timeout"
    assert result["pytest_log_path"]
    assert result["collection_log_path"]
    assert (tmp_path / "pytest.log").exists()


def test_classifies_low_coverage_when_tests_pass():
    issue = pytest_runner.classify_execution_issue(
        "1 passed",
        collection_passed=True,
        passed=True,
        coverage_file_exists=True,
        coverage_percent=50.0,
        coverage_threshold=80.0,
        missing_lines=[3],
    )

    assert issue["type"] == "low_coverage"

