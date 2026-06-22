import pytest
import subprocess
from pathlib import Path
from testgen.executors.external_command import ExternalCommandExecutor
from testgen.executors.base import TestExecutionRequest

class DummyExternalExecutor(ExternalCommandExecutor):
    def execute(self, req: TestExecutionRequest): pass


def test_executor_timeout_override():
    ex = DummyExternalExecutor(timeout_seconds=99)
    assert ex.timeout_seconds == 99


def test_tool_exists(tmp_path):
    ex = DummyExternalExecutor(which_fn=lambda x: "found" if x == "cmd" else None)
    assert ex._tool_exists("cmd") is True
    assert ex._tool_exists("missing") is False
    
    # Tool exists as local file
    tool_file = tmp_path / "my_script.sh"
    tool_file.touch()
    assert ex._tool_exists(str(tool_file)) is True


def test_summary_extra_payload():
    ex = DummyExternalExecutor()
    res = ex._summary(
        passed=True, command=["cmd"], output="out", diagnosis="diag", 
        issue_type="issue", title="title", hint="hint", extra={"my_key": "val"}
    )
    assert res["my_key"] == "val"


def test_run_command_resolved_tool():
    def fake_runner(cmd, **kwargs):
        return subprocess.CompletedProcess(args=cmd, returncode=0, stdout="out", stderr="")
    
    ex = DummyExternalExecutor(runner=fake_runner, which_fn=lambda x: "/bin/tool" if x == "tool" else None)
    process, err = ex._run_command(["tool", "arg1"], cwd=Path("."))
    assert err is None
    assert process.args == ["/bin/tool", "arg1"]


def test_run_command_timeout():
    def fake_runner_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="cmd", timeout=10, output="partial", stderr="err")
    
    ex = DummyExternalExecutor(runner=fake_runner_timeout, which_fn=lambda x: "tool")
    process, err = ex._run_command(["tool"], cwd=Path("."))
    assert process is None
    assert err["execution_issue"]["type"] == "execution_timeout"
    assert "partial" in err["output"]


def test_run_command_oserror():
    def fake_runner_oserror(*args, **kwargs):
        raise OSError("Permission denied")
    
    ex = DummyExternalExecutor(runner=fake_runner_oserror, which_fn=lambda x: "tool")
    process, err = ex._run_command(["tool"], cwd=Path("."))
    assert process is None
    assert err["execution_issue"]["type"] == "execution_error"
    assert "Permission denied" in err["output"]


def test_failure_summary_fallback():
    ex = DummyExternalExecutor()
    assert ex._failure_summary("") == ""
    assert ex._failure_summary("no keywords here") == "no keywords here"
    
    long_text = "a" * 1500
    assert len(ex._failure_summary(long_text)) <= 1204
    assert ex._failure_summary(long_text).endswith("...")
