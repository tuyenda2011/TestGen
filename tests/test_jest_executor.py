import pytest
from pathlib import Path
from testgen.executors.jest_executor import JestExecutor


def test_jest_command_for_workspace(tmp_path):
    ex = JestExecutor()
    base_flags = ["--coverage", "--runInBand", "--json", "--outputFile=jest_results.json", "--forceExit", "--env=jsdom"]
    assert ex._command_for_workspace(tmp_path) == ["npx", "--no-install", "jest"] + base_flags
    
    (tmp_path / "package.json").touch()
    assert ex._command_for_workspace(tmp_path) == ["npm", "test", "--"] + base_flags


def test_jest_read_coverage_not_exists(tmp_path):
    ex = JestExecutor()
    pct, pth = ex._read_coverage(tmp_path)
    assert pct == 0.0
    assert pth == ""


def test_jest_read_coverage_invalid_json(tmp_path):
    ex = JestExecutor()
    cov_path = tmp_path / "coverage" / "coverage-summary.json"
    cov_path.parent.mkdir(parents=True, exist_ok=True)
    cov_path.write_text("invalid json")
    
    pct, pth = ex._read_coverage(tmp_path)
    assert pct == 0.0
    assert pth == str(cov_path)


def test_jest_read_coverage_total_not_dict(tmp_path):
    ex = JestExecutor()
    cov_path = tmp_path / "coverage" / "coverage-summary.json"
    cov_path.parent.mkdir(parents=True, exist_ok=True)
    cov_path.write_text('{"total": "not a dict"}')
    
    pct, pth = ex._read_coverage(tmp_path)
    assert pct == 0.0
    assert pth == str(cov_path)


def test_jest_read_coverage_pct_not_float(tmp_path):
    ex = JestExecutor()
    cov_path = tmp_path / "coverage" / "coverage-summary.json"
    cov_path.parent.mkdir(parents=True, exist_ok=True)
    cov_path.write_text('{"total": {"lines": {"pct": "invalid"}}}')
    
    pct, pth = ex._read_coverage(tmp_path)
    assert pct == 0.0
    assert pth == str(cov_path)


def test_jest_read_coverage_valid(tmp_path):
    ex = JestExecutor()
    cov_path = tmp_path / "coverage" / "coverage-summary.json"
    cov_path.parent.mkdir(parents=True, exist_ok=True)
    cov_path.write_text('{"total": {"lines": {"pct": 85.5}}}')
    
    pct, pth = ex._read_coverage(tmp_path)
    assert pct == 85.5
    assert pth == str(cov_path)
