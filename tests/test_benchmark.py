from __future__ import annotations

from pathlib import Path

from testgen import benchmark


def test_build_benchmark_inventory_counts_functions(tmp_path):
    source_path = tmp_path / "sample.py"
    source_path.write_text(
        "def f(value):\n"
        "    if value < 0:\n"
        "        raise ValueError('negative')\n"
        "    return value\n",
        encoding="utf-8",
    )

    inventory = benchmark.build_benchmark_inventory(tmp_path)

    assert len(inventory) == 1
    assert inventory[0].function_count == 1
    assert inventory[0].condition_count == 1
    assert inventory[0].exception_count == 1


def test_run_benchmark_dry_run_writes_report(tmp_path):
    benchmark_dir = tmp_path / "bench"
    benchmark_dir.mkdir()
    (benchmark_dir / "calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    report_path = tmp_path / "BENCHMARK_REPORT.md"

    results = benchmark.run_benchmark(
        benchmark_dir=benchmark_dir,
        report_path=report_path,
        execute=False,
    )

    assert len(results) == 1
    assert results[0].status == "inventory"
    report = report_path.read_text(encoding="utf-8")
    assert "Pipeline execution: no" in report
    assert "`calc.py`" in report


def test_run_benchmark_execute_uses_runner(tmp_path):
    benchmark_dir = tmp_path / "bench"
    benchmark_dir.mkdir()
    (benchmark_dir / "calc.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")

    class FakeResult:
        def model_dump(self):
            return {
                "run_id": "run-001",
                "diagnostics": {
                    "pytest_passed": True,
                    "pytest_combined_coverage_percent": 91.0,
                    "pytest_attempts": 2,
                },
                "execution_summary": {},
            }

    def fake_runner(input_data, profile):
        return FakeResult()

    results = benchmark.run_benchmark(
        benchmark_dir=benchmark_dir,
        report_path=tmp_path / "report.md",
        execute=True,
        runner=fake_runner,
    )

    assert results[0].status == "completed"
    assert results[0].passed is True
    assert results[0].coverage_percent == 91.0
    assert results[0].attempts == 2
