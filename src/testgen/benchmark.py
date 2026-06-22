from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from testgen.core.constants import profile_for_mode
from testgen.core.models import PipelineInput, PipelineProfile
from testgen.pipeline_orchestrator import run_pipeline
from testgen.prompts.function_prompt_builder import FunctionPromptBuilder


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BENCHMARK_DIR = PROJECT_ROOT / "examples" / "benchmark_sources"
DEFAULT_REPORT_PATH = PROJECT_ROOT / "BENCHMARK_REPORT.md"


@dataclass(frozen=True)
class BenchmarkSource:
    path: Path
    function_count: int
    condition_count: int
    exception_count: int


@dataclass(frozen=True)
class BenchmarkResult:
    source: BenchmarkSource
    status: str
    passed: bool | None = None
    coverage_percent: float | None = None
    attempts: int | None = None
    model: str = ""
    run_id: str = ""
    error: str = ""


def discover_benchmark_sources(benchmark_dir: Path = DEFAULT_BENCHMARK_DIR) -> list[Path]:
    if not benchmark_dir.exists():
        return []
    return sorted(path for path in benchmark_dir.glob("*.py") if path.is_file())


def summarize_benchmark_source(path: Path) -> BenchmarkSource:
    source_text = path.read_text(encoding="utf-8")
    functions = FunctionPromptBuilder.extract_python_functions(source_text, max_functions=64)
    return BenchmarkSource(
        path=path,
        function_count=len(functions),
        condition_count=sum(len(item.conditions) for item in functions),
        exception_count=sum(len(item.exceptions) for item in functions),
    )


def build_benchmark_inventory(benchmark_dir: Path = DEFAULT_BENCHMARK_DIR) -> list[BenchmarkSource]:
    return [summarize_benchmark_source(path) for path in discover_benchmark_sources(benchmark_dir)]


def _api_key_for_mode(mode: str, explicit_api_key: str = "") -> str:
    if explicit_api_key:
        return explicit_api_key
    if mode == "OpenRouter API Key":
        return os.environ.get("OPENROUTER_API_KEY", "")
    if mode == "API key":
        return os.environ.get("GEMINI_API_KEY", "")
    return ""


def run_benchmark_case(
    source: BenchmarkSource,
    *,
    mode: str,
    api_key: str = "",
    runner: Callable[..., Any] = run_pipeline,
) -> BenchmarkResult:
    source_text = source.path.read_text(encoding="utf-8")
    profile = PipelineProfile(**profile_for_mode(mode))
    model_label = profile.generator_model
    try:
        result = runner(
            PipelineInput(
                requirement_text=(
                    "Sinh pytest unit tests bám đúng source code. "
                    "Ưu tiên branch, boundary, exception và không bịa behavior ngoài source."
                ),
                docs_files=[],
                source_code_text=source_text,
                source_files=[],
                test_code_text="",
                test_files=[],
                retrieval_query=f"Benchmark pytest for {source.path.name}",
                framework="pytest",
                test_technique="White-box",
                workflow_mode="generate_tests",
                api_key=_api_key_for_mode(mode, api_key),
                use_preindexed_docs=False,
            ),
            profile,
        )
    except Exception as exc:
        return BenchmarkResult(source=source, status="failed", model=model_label, error=str(exc))

    result_dict = result.model_dump() if hasattr(result, "model_dump") else dict(result)
    diagnostics = result_dict.get("diagnostics", {})
    execution_summary = result_dict.get("execution_summary", {})
    return BenchmarkResult(
        source=source,
        status="completed",
        passed=bool(diagnostics.get("pytest_passed", execution_summary.get("passed", False))),
        coverage_percent=float(
            diagnostics.get(
                "pytest_combined_coverage_percent",
                diagnostics.get("pytest_coverage_percent", execution_summary.get("coverage_percent", 0.0)),
            )
            or 0.0
        ),
        attempts=int(diagnostics.get("pytest_attempts", 0) or 0),
        model=model_label,
        run_id=str(result_dict.get("run_id", "")),
    )


def build_benchmark_report(
    results: list[BenchmarkResult],
    *,
    executed: bool,
    mode: str = "",
) -> str:
    title = "# BENCHMARK REPORT\n\n"
    status_line = (
        f"Mode: `{mode}`. Pipeline execution: {'yes' if executed else 'no'}.\n\n"
        if mode
        else f"Pipeline execution: {'yes' if executed else 'no'}.\n\n"
    )
    table = [
        "| Source | Functions | Conditions | Exceptions | Status | Passed | Coverage | Attempts | Model | Run ID | Error |",
        "|---|---:|---:|---:|---|---|---:|---:|---|---|---|",
    ]
    for item in results:
        coverage = "" if item.coverage_percent is None else f"{item.coverage_percent:.1f}%"
        attempts = "" if item.attempts is None else str(item.attempts)
        passed = "" if item.passed is None else ("yes" if item.passed else "no")
        table.append(
            "| "
            + " | ".join(
                [
                    f"`{item.source.path.name}`",
                    str(item.source.function_count),
                    str(item.source.condition_count),
                    str(item.source.exception_count),
                    item.status,
                    passed,
                    coverage,
                    attempts,
                    item.model,
                    item.run_id,
                    item.error.replace("|", "\\|").replace("\n", " ")[:240],
                ]
            )
            + " |"
        )

    notes = (
        "\n\n## Notes\n\n"
        "- Dry-run mode only inventories benchmark sources and does not call an LLM.\n"
        "- Execute mode runs the full pytest generation pipeline and records pass/coverage/attempts.\n"
        "- Treat this report as a regression baseline for prompt/model/executor changes.\n"
    )
    return title + status_line + "\n".join(table) + notes


def write_benchmark_report(report: str, report_path: Path = DEFAULT_REPORT_PATH) -> Path:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def run_benchmark(
    *,
    benchmark_dir: Path = DEFAULT_BENCHMARK_DIR,
    report_path: Path = DEFAULT_REPORT_PATH,
    mode: str = "Local AI",
    api_key: str = "",
    execute: bool = False,
    runner: Callable[..., Any] = run_pipeline,
) -> list[BenchmarkResult]:
    sources = build_benchmark_inventory(benchmark_dir)
    if execute:
        results = [
            run_benchmark_case(source, mode=mode, api_key=api_key, runner=runner)
            for source in sources
        ]
    else:
        results = [BenchmarkResult(source=source, status="inventory") for source in sources]
    write_benchmark_report(build_benchmark_report(results, executed=execute, mode=mode), report_path)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run or inventory TestGen benchmark sources.")
    parser.add_argument("--benchmark-dir", default=str(DEFAULT_BENCHMARK_DIR))
    parser.add_argument("--report-path", default=str(DEFAULT_REPORT_PATH))
    parser.add_argument("--mode", default="Local AI", choices=["Local AI", "API key", "OpenRouter API Key"])
    parser.add_argument("--api-key", default="")
    parser.add_argument("--execute", action="store_true", help="Run the full LLM pipeline instead of dry-run inventory.")
    args = parser.parse_args(argv)

    results = run_benchmark(
        benchmark_dir=Path(args.benchmark_dir),
        report_path=Path(args.report_path),
        mode=args.mode,
        api_key=args.api_key,
        execute=args.execute,
    )
    print(f"Wrote benchmark report for {len(results)} source file(s): {args.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
