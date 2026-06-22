import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from testgen.executors.newman_executor import NewmanExecutor
from testgen.executors.base import TestExecutionRequest


def test_newman_early_summary(tmp_path):
    ex = NewmanExecutor()
    with patch.object(ex, "_run_command", return_value=(None, {"early": True})):
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="{}", source_code_text="")
        outcome = ex.execute(req)
        assert outcome.summary["early"] is True


def test_newman_parse_json_empty(tmp_path):
    ex = NewmanExecutor()
    assert ex._parse_json_report(tmp_path / "missing.json") == {}


def test_newman_parse_json_invalid(tmp_path):
    ex = NewmanExecutor()
    pth = tmp_path / "bad.json"
    pth.write_text("invalid json")
    assert ex._parse_json_report(pth) == {"report_parse_error": True}


def test_newman_parse_json_no_run(tmp_path):
    ex = NewmanExecutor()
    pth = tmp_path / "norun.json"
    pth.write_text('{"other": 1}')
    assert ex._parse_json_report(pth) == {}


def test_newman_parse_json_no_stats(tmp_path):
    ex = NewmanExecutor()
    pth = tmp_path / "nostats.json"
    pth.write_text('{"run": {"other": 1}}')
    assert ex._parse_json_report(pth) == {}


def test_newman_stat_not_dict():
    ex = NewmanExecutor()
    assert ex._stat({"requests": 1}, "requests", "total") == 0


def test_newman_stat_not_int():
    ex = NewmanExecutor()
    assert ex._stat({"requests": {"total": "bad"}}, "requests", "total") == 0


def test_newman_execute_success(tmp_path):
    ex = NewmanExecutor()
    with patch.object(ex, "_run_command", return_value=(MagicMock(returncode=0, stdout="", stderr=""), None)):
        pth = tmp_path / "newman-report.json"
        pth.write_text('{"run": {"stats": {"assertions": {"failed": 0}}}}')
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="{}", source_code_text="")
        outcome = ex.execute(req)
        assert outcome.summary["passed"] is True
