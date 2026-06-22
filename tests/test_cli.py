from __future__ import annotations

from argparse import Namespace
from types import SimpleNamespace

import pytest

from testgen import cli
from testgen.cli import _cmd_benchmark, _cmd_generate, _profile_for_backend, build_parser


def test_cli_generate_parser_accepts_source_and_backend():
    args = build_parser().parse_args(["generate", "sample.py", "--backend", "ollama"])

    assert args.command == "generate"
    assert args.source == "sample.py"
    assert args.backend == "ollama"


def test_cli_benchmark_parser_defaults_to_inventory_mode():
    args = build_parser().parse_args(["benchmark"])

    assert args.command == "benchmark"
    assert args.execute is False


def test_profile_for_backend_uses_expected_backend_defaults():
    assert _profile_for_backend("ollama").backend == "ollama"
    assert _profile_for_backend("gemini").embedding_backend == "gemini"
    assert _profile_for_backend("openrouter").embedding_backend == "ollama"


def test_cmd_generate_prints_artifact_summary(tmp_path, monkeypatch, capsys):
    source = tmp_path / "calc.py"
    source.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")

    captured = {}

    def fake_run_pipeline(*, input_data, profile):
        captured["input_data"] = input_data
        captured["profile"] = profile
        return SimpleNamespace(
            model_dump=lambda: {
                "run_id": "run-cli",
                "code_path": "/tmp/test_calc.py",
                "diagnostics": {"pytest_passed": True},
            }
        )

    monkeypatch.setattr(cli, "run_pipeline", fake_run_pipeline)

    exit_code = _cmd_generate(
        Namespace(
            source=str(source),
            requirement="test calc",
            query="calc",
            framework="pytest",
            technique="Hybrid",
            backend="ollama",
            api_key="",
        )
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "run-cli" in output
    assert captured["input_data"].source_code_text.startswith("def add")
    assert captured["profile"].backend == "ollama"


def test_cmd_generate_raises_clear_error_for_missing_source(tmp_path):
    missing = tmp_path / "missing.py"

    with pytest.raises(FileNotFoundError, match="Source file does not exist"):
        _cmd_generate(
            Namespace(
                source=str(missing),
                requirement="test calc",
                query="calc",
                framework="pytest",
                technique="Hybrid",
                backend="ollama",
                api_key="",
            )
        )


def test_cmd_generate_raises_clear_error_for_missing_backend_api_key(tmp_path):
    source = tmp_path / "calc.py"
    source.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")

    with pytest.raises(ValueError, match="openrouter API key is required"):
        _cmd_generate(
            Namespace(
                source=str(source),
                requirement="test calc",
                query="calc",
                framework="pytest",
                technique="Hybrid",
                backend="openrouter",
                api_key="",
            )
        )


def test_cmd_benchmark_writes_report(monkeypatch, capsys):
    monkeypatch.setattr(cli, "run_benchmark", lambda **kwargs: ["case"])
    monkeypatch.setattr(cli, "build_benchmark_report", lambda results: "report")
    monkeypatch.setattr(cli, "write_benchmark_report", lambda report: "BENCHMARK_REPORT.md")

    exit_code = _cmd_benchmark(Namespace(mode="Ollama", execute=False, api_key="", report_path=None))

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Benchmark cases: 1" in output
    assert "BENCHMARK_REPORT.md" in output
