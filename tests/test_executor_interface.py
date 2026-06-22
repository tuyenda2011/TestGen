from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from testgen.executors import (
    JestExecutor,
    JUnitExecutor,
    NewmanExecutor,
    PytestExecutor,
    TestExecutionRequest,
    get_test_executor,
)


def test_pytest_executor_wraps_runner_and_scorer(tmp_path):
    calls = {}

    def fake_runner(**kwargs):
        calls.update(kwargs)
        return {"passed": True, "coverage_percent": 91.0}

    def fake_scorer(summary, threshold):
        return (9, 8, float(summary["coverage_percent"]) + threshold)

    executor = PytestExecutor(runner=fake_runner, scorer=fake_scorer)
    request = TestExecutionRequest(
        source_code_text="def add(a, b): return a + b",
        generated_test_code="def test_add(): assert add(1, 2) == 3",
        workspace_dir=tmp_path,
        coverage_threshold=80.0,
    )

    outcome = executor.execute(request)

    assert outcome.framework == "pytest"
    assert outcome.summary["coverage_percent"] == 91.0
    assert calls["workspace_dir"] == tmp_path
    assert executor.score_result(outcome.summary, 80.0) == (9, 8, 171.0)


def test_executor_registry_returns_supported_frameworks():
    assert get_test_executor("pytest") is not None
    assert get_test_executor("Pytest") is not None
    assert get_test_executor("Jest").framework == "Jest"
    assert get_test_executor("JUnit").framework == "JUnit"
    assert get_test_executor("Postman script").framework == "Postman script"
    assert get_test_executor("unknown") is None


def test_jest_executor_runs_npm_test_and_reads_coverage(tmp_path):
    (tmp_path / "package.json").write_text('{"scripts":{"test":"jest"}}', encoding="utf-8")

    def fake_runner(command, capture_output, text, cwd, timeout, **kwargs):
        coverage_dir = Path(cwd) / "coverage"
        coverage_dir.mkdir(parents=True, exist_ok=True)
        (coverage_dir / "coverage-summary.json").write_text(
            json.dumps({"total": {"lines": {"pct": 87.5}}}),
            encoding="utf-8",
        )
        return SimpleNamespace(
            returncode=0,
            stdout="Test Suites: 1 passed, 1 total\nTests: 2 passed, 2 total\n",
            stderr="",
        )

    executor = JestExecutor(runner=fake_runner, which_fn=lambda tool: f"/bin/{tool}")
    outcome = executor.execute(
        TestExecutionRequest(
            source_code_text="export function add(a,b){return a+b}",
            generated_test_code="test('ok', () => expect(1 + 1).toBe(2));",
            workspace_dir=tmp_path,
        )
    )

    assert outcome.summary["passed"] is True
    assert outcome.summary["command"][:2] == ["npm", "test"]
    assert outcome.summary["coverage_percent"] == 87.5
    assert outcome.summary["tests_passed"] == 2


def test_jest_executor_reports_missing_toolchain(tmp_path):
    executor = JestExecutor(runner=lambda **kwargs: None, which_fn=lambda tool: None)

    outcome = executor.execute(
        TestExecutionRequest(
            source_code_text="",
            generated_test_code="test('ok', () => expect(true).toBe(true));",
            workspace_dir=tmp_path,
        )
    )

    assert outcome.summary["passed"] is False
    assert outcome.summary["execution_issue"]["type"] == "toolchain_missing"
    assert "Missing toolchain command" in outcome.summary["diagnosis"]


def test_jest_executor_blocks_unsafe_generated_code_before_command(tmp_path):
    calls = {"count": 0}

    def fake_runner(*args, **kwargs):
        calls["count"] += 1
        raise AssertionError("runner should not be called")

    executor = JestExecutor(runner=fake_runner, which_fn=lambda tool: f"/bin/{tool}")
    outcome = executor.execute(
        TestExecutionRequest(
            source_code_text="function add(a, b) { return a + b; }",
            generated_test_code="const cp = require('child_process'); cp.execSync('whoami');",
            workspace_dir=tmp_path,
        )
    )

    assert calls["count"] == 0
    assert outcome.summary["passed"] is False
    assert outcome.summary["execution_issue"]["type"] == "security_block"


def test_junit_executor_runs_maven_and_parses_surefire_xml(tmp_path):
    (tmp_path / "pom.xml").write_text("<project></project>", encoding="utf-8")

    def fake_runner(command, capture_output, text, cwd, timeout, **kwargs):
        report_dir = Path(cwd) / "target" / "surefire-reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "TEST-GeneratedTest.xml").write_text(
            '<testsuite tests="2" failures="0" errors="0" skipped="0"></testsuite>',
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0, stdout="BUILD SUCCESS", stderr="")

    executor = JUnitExecutor(runner=fake_runner, which_fn=lambda tool: f"/bin/{tool}")
    outcome = executor.execute(
        TestExecutionRequest(
            source_code_text="public class SourceUnderTest {}",
            generated_test_code="class GeneratedTest {}",
            workspace_dir=tmp_path,
        )
    )

    assert outcome.summary["passed"] is True
    assert outcome.summary["command"] == ["mvn", "test"]
    assert outcome.summary["tests_total"] == 2
    assert outcome.summary["failures"] == 0





def test_junit_executor_blocks_unsafe_generated_code_before_command(tmp_path):
    (tmp_path / "pom.xml").write_text("<project></project>", encoding="utf-8")
    calls = {"count": 0}

    def fake_runner(*args, **kwargs):
        calls["count"] += 1
        raise AssertionError("runner should not be called")

    executor = JUnitExecutor(runner=fake_runner, which_fn=lambda tool: f"/bin/{tool}")
    outcome = executor.execute(
        TestExecutionRequest(
            source_code_text="public class SourceUnderTest {}",
            generated_test_code="class GeneratedTest { void x(){ Runtime.getRuntime().exec(\"whoami\"); } }",
            workspace_dir=tmp_path,
        )
    )

    assert calls["count"] == 0
    assert outcome.summary["passed"] is False
    assert outcome.summary["execution_issue"]["type"] == "security_block"


def test_newman_executor_runs_collection_and_parses_json_report(tmp_path):
    def fake_runner(command, capture_output, text, cwd, timeout, **kwargs):
        report_path = Path(cwd) / "newman-report.json"
        report_path.write_text(
            json.dumps(
                {
                    "run": {
                        "stats": {
                            "requests": {"total": 1, "failed": 0},
                            "assertions": {"total": 3, "failed": 0},
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0, stdout="newman ok", stderr="")

    executor = NewmanExecutor(runner=fake_runner, which_fn=lambda tool: f"/bin/{tool}")
    outcome = executor.execute(
        TestExecutionRequest(
            source_code_text="",
            generated_test_code='{"info":{"name":"demo"},"item":[]}',
            workspace_dir=tmp_path,
        )
    )

    assert outcome.summary["passed"] is True
    assert outcome.summary["assertions_total"] == 3
    assert outcome.summary["requests_total"] == 1
