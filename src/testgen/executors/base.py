from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ExecutionScore = tuple[int, int, float]


@dataclass(frozen=True)
class TestExecutionRequest:
    __test__ = False

    source_code_text: str
    generated_test_code: str
    workspace_dir: Path
    coverage_threshold: float = 80.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TestExecutionOutcome:
    __test__ = False

    framework: str
    summary: dict[str, Any]


class TestExecutor(ABC):
    __test__ = False

    framework: str
    display_name: str
    coverage_supported: bool = False
    retry_supported: bool = False

    @abstractmethod
    def execute(self, request: TestExecutionRequest) -> TestExecutionOutcome:
        raise NotImplementedError

    def score_result(
        self,
        summary: dict[str, Any],
        coverage_threshold: float,
    ) -> ExecutionScore:
        try:
            coverage_percent = float(summary.get("coverage_percent", 0.0))
        except (TypeError, ValueError):
            coverage_percent = 0.0
        passed = bool(summary.get("passed", False))
        coverage_supported = bool(summary.get("coverage_supported", getattr(self, "coverage_supported", False)))
        if passed and not coverage_supported:
            return (1, 1, coverage_percent)
        return (
            1 if passed and coverage_percent >= coverage_threshold else 0,
            1 if passed else 0,
            coverage_percent,
        )
