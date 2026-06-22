from __future__ import annotations

from collections.abc import Callable
from typing import Any

from testgen.executors.pytest_runner import (
    execution_result_score,
    run_generated_pytest_with_coverage,
)
from testgen.executors.base import (
    ExecutionScore,
    TestExecutionOutcome,
    TestExecutionRequest,
    TestExecutor,
)


class PytestExecutor(TestExecutor):
    framework = "pytest"
    display_name = "pytest + pytest-cov"
    coverage_supported = True
    retry_supported = True

    def __init__(
        self,
        *,
        runner: Callable[..., dict[str, Any]] = run_generated_pytest_with_coverage,
        scorer: Callable[[dict[str, Any], float], ExecutionScore] = execution_result_score,
    ) -> None:
        self._runner = runner
        self._scorer = scorer

    def execute(self, request: TestExecutionRequest) -> TestExecutionOutcome:
        summary = self._runner(
            source_code_text=request.source_code_text,
            generated_test_code=request.generated_test_code,
            workspace_dir=request.workspace_dir,
            coverage_threshold=request.coverage_threshold,
        )
        return TestExecutionOutcome(framework=self.framework, summary=summary)

    def score_result(
        self,
        summary: dict[str, Any],
        coverage_threshold: float,
    ) -> ExecutionScore:
        return self._scorer(summary, coverage_threshold)


class PytestE2EExecutor(PytestExecutor):
    coverage_supported = False

    def __init__(
        self,
        framework: str,
        *,
        runner: Callable[..., dict[str, Any]] = run_generated_pytest_with_coverage,
        scorer: Callable[[dict[str, Any], float], ExecutionScore] = execution_result_score,
    ) -> None:
        super().__init__(runner=runner, scorer=scorer)
        self.framework = framework
        self.display_name = f"pytest ({framework} E2E)"

    def execute(self, request: TestExecutionRequest) -> TestExecutionOutcome:
        summary = self._runner(
            source_code_text=request.source_code_text,
            generated_test_code=request.generated_test_code,
            workspace_dir=request.workspace_dir,
            coverage_threshold=request.coverage_threshold,
            enable_coverage=False,
            source_filename="source_under_test.html",
            is_e2e=True,
        )
        return TestExecutionOutcome(framework=self.framework, summary=summary)
