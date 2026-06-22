import pytest
from pathlib import Path
from testgen.executors.base import TestExecutor, TestExecutionRequest, TestExecutionOutcome

class DummyExecutor(TestExecutor):
    framework = "dummy"
    display_name = "Dummy"
    def execute(self, req: TestExecutionRequest) -> TestExecutionOutcome:
        return super().execute(req)

def test_executor_base_execute_not_implemented():
    executor = DummyExecutor()
    req = TestExecutionRequest(workspace_dir=Path("."), generated_test_code="", source_code_text="")
    with pytest.raises(NotImplementedError):
        executor.execute(req)

def test_executor_score_result_bad_coverage():
    executor = DummyExecutor()
    score = executor.score_result({"passed": True, "coverage_percent": "bad"}, 80)
    assert score == (1, 1, 0.0)

def test_executor_score_result_no_coverage_supported():
    executor = DummyExecutor()
    # By default, coverage_supported is False on DummyExecutor
    score = executor.score_result({"passed": True, "coverage_percent": 0.0}, 80)
    assert score == (1, 1, 0.0)
    
    # Test passed=True, coverage_supported=True in summary
    score2 = executor.score_result({"passed": True, "coverage_supported": True, "coverage_percent": 90.0}, 80)
    assert score2 == (1, 1, 90.0)
