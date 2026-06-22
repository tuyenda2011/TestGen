from __future__ import annotations

from collections.abc import Callable
from typing import Any

from testgen.executors.base import ExecutionScore, TestExecutor
from testgen.executors.jest_executor import JestExecutor
from testgen.executors.junit_executor import JUnitExecutor
from testgen.executors.newman_executor import NewmanExecutor
from testgen.executors.pytest_executor import PytestExecutor


def get_test_executor(
    framework: str,
    *,
    pytest_runner: Callable[..., dict[str, Any]] | None = None,
    pytest_scorer: Callable[[dict[str, Any], float], ExecutionScore] | None = None,
) -> TestExecutor | None:
    normalized = (framework or "").strip().lower()

    if normalized == "jest":
        return JestExecutor()
    if normalized == "junit":
        return JUnitExecutor()
    if normalized in {"newman", "postman", "postman script"}:
        return NewmanExecutor()

    kwargs: dict[str, Any] = {}
    if pytest_runner is not None:
        kwargs["runner"] = pytest_runner
    if pytest_scorer is not None:
        kwargs["scorer"] = pytest_scorer

    if normalized in {"selenium", "playwright"}:
        from testgen.executors.pytest_executor import PytestE2EExecutor
        return PytestE2EExecutor(framework=framework, **kwargs)

    if normalized == "pytest":
        return PytestExecutor(**kwargs)

    return None
