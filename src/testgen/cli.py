from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from testgen.benchmark import build_benchmark_report, run_benchmark, write_benchmark_report
from testgen.core.config import (
    CODE_GENERATOR_MODEL,
    CODE_REVIEW_MODEL,
    EMBED_MODEL,
    GEMINI_CODE_GENERATOR_MODEL,
    GEMINI_CODE_REVIEW_MODEL,
    GEMINI_REQUIREMENT_MODEL,
    GEMINI_TEST_PLANNING_MODEL,
    OLLAMA_CODE_GENERATOR_MODEL,
    OLLAMA_CODE_REVIEW_MODEL,
    OLLAMA_REQUIREMENT_MODEL,
    OLLAMA_TEST_PLANNING_MODEL,
    REQUIREMENT_MODEL,
    TEST_PLANNING_MODEL,
)
from testgen.core.constants import GENERATE_WORKFLOW
from testgen.core.models import PipelineInput, PipelineProfile
from testgen.pipeline_orchestrator import run_pipeline


def _profile_for_backend(backend: str) -> PipelineProfile:
    if backend == "gemini":
        return PipelineProfile(
            backend="gemini",
            mode_label="CLI / Gemini",
            requirement_model=GEMINI_REQUIREMENT_MODEL,
            planning_model=GEMINI_TEST_PLANNING_MODEL,
            generator_model=GEMINI_CODE_GENERATOR_MODEL,
            review_model=GEMINI_CODE_REVIEW_MODEL,
            embed_model=EMBED_MODEL,
            embedding_backend="gemini",
        )
    if backend == "openrouter":
        return PipelineProfile(
            backend="openrouter",
            mode_label="CLI / OpenRouter",
            requirement_model=REQUIREMENT_MODEL,
            planning_model=TEST_PLANNING_MODEL,
            generator_model=CODE_GENERATOR_MODEL,
            review_model=CODE_REVIEW_MODEL,
            embed_model=EMBED_MODEL,
            embedding_backend="ollama",
        )
    return PipelineProfile(
        backend="ollama",
        mode_label="CLI / Ollama",
        requirement_model=OLLAMA_REQUIREMENT_MODEL,
        planning_model=OLLAMA_TEST_PLANNING_MODEL,
        generator_model=OLLAMA_CODE_GENERATOR_MODEL,
        review_model=OLLAMA_CODE_REVIEW_MODEL,
        embed_model=EMBED_MODEL,
        embedding_backend="ollama",
    )


def _cmd_generate(args: argparse.Namespace) -> int:
    source_path = Path(args.source).expanduser().resolve()
    if not source_path.exists() or not source_path.is_file():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")
    if args.backend in {"gemini", "openrouter"} and not (args.api_key or "").strip():
        raise ValueError(f"{args.backend} API key is required for CLI generate. Pass --api-key.")
    source_text = source_path.read_text(encoding="utf-8")
    input_data = PipelineInput(
        requirement_text=args.requirement or f"Generate pytest tests for {source_path.name}",
        source_code_text=source_text,
        retrieval_query=args.query or args.requirement or source_path.stem,
        framework=args.framework,
        test_technique=args.technique,
        workflow_mode=GENERATE_WORKFLOW,
        api_key=args.api_key or "",
        use_preindexed_docs=False,
    )
    result = run_pipeline(input_data=input_data, profile=_profile_for_backend(args.backend))
    payload: dict[str, Any] = result.model_dump() if hasattr(result, "model_dump") else dict(result)
    print(
        json.dumps(
            {
                "run_id": payload.get("run_id"),
                "code_path": payload.get("code_path"),
                "test_plan_path": payload.get("test_plan_path"),
                "review_path": payload.get("review_path"),
                "coverage_report_path": payload.get("coverage_report_path"),
                "diagnostics": payload.get("diagnostics", {}),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _cmd_benchmark(args: argparse.Namespace) -> int:
    results = run_benchmark(mode=args.mode, execute=args.execute, api_key=args.api_key or "")
    report = build_benchmark_report(results)
    report_path = write_benchmark_report(report, args.report_path) if args.report_path else write_benchmark_report(report)
    print(f"Benchmark cases: {len(results)}")
    print(f"Report: {report_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="testgen", description="TestGen CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate tests for a source file")
    generate.add_argument("source", help="Path to source file")
    generate.add_argument("--framework", default="pytest")
    generate.add_argument("--technique", default="Hybrid")
    generate.add_argument("--backend", choices=["ollama", "gemini", "openrouter"], default="ollama")
    generate.add_argument("--api-key", default="")
    generate.add_argument("--requirement", default="")
    generate.add_argument("--query", default="")
    generate.set_defaults(func=_cmd_generate)

    benchmark = subparsers.add_parser("benchmark", help="Run benchmark inventory or execution")
    benchmark.add_argument("--mode", default="Ollama")
    benchmark.add_argument("--execute", action="store_true")
    benchmark.add_argument("--api-key", default="")
    benchmark.add_argument("--report-path", type=Path, default=None)
    benchmark.set_defaults(func=_cmd_benchmark)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
