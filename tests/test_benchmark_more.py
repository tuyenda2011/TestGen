import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from testgen import benchmark

def test_discover_benchmark_sources_missing_dir(tmp_path):
    assert benchmark.discover_benchmark_sources(tmp_path / "missing") == []

def test_api_key_for_mode():
    assert benchmark._api_key_for_mode("mode", "abc") == "abc"
    with patch("os.environ.get", return_value="env_open"):
        assert benchmark._api_key_for_mode("OpenRouter", "") == "env_open"
    with patch("os.environ.get", return_value="env_gemini"):
        assert benchmark._api_key_for_mode("API key", "") == "env_gemini"
    assert benchmark._api_key_for_mode("Other", "") == ""

def test_run_benchmark_case_exception(tmp_path):
    source = benchmark.BenchmarkSource(tmp_path / "bench.py", 1, 0, 0)
    source.path.write_text("def f(): pass")
    
    def failing_runner(*args, **kwargs):
        raise ValueError("Simulated error")
        
    res = benchmark.run_benchmark_case(source, mode="Multi-agent", runner=failing_runner)
    assert res.status == "failed"
    assert "Simulated error" in res.error

def test_run_benchmark_case_fallback_model_dump(tmp_path):
    source = benchmark.BenchmarkSource(tmp_path / "bench2.py", 1, 0, 0)
    source.path.write_text("def g(): pass")
    
    class ResultWithoutModelDump(dict):
        pass
    
    def dummy_runner(*args, **kwargs):
        return ResultWithoutModelDump({
            "run_id": "dummy_123",
            "diagnostics": {"pytest_coverage_percent": 80.0},
            "execution_summary": {"passed": True}
        })
        
    res = benchmark.run_benchmark_case(source, mode="Multi-agent", runner=dummy_runner)
    assert res.status == "completed"
    assert res.run_id == "dummy_123"
    assert res.passed is True
    assert res.coverage_percent == 80.0

def test_main(monkeypatch):
    calls = []
    def fake_run(*args, **kwargs):
        calls.append(kwargs)
        return []
    monkeypatch.setattr(benchmark, "run_benchmark", fake_run)
    benchmark.main(["--mode", "OpenRouter"])
    assert len(calls) == 1
    assert calls[0]["mode"] == "OpenRouter"
