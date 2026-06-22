import pytest
import json
from pathlib import Path
from testgen.executors import pytest_runner

def test_execution_result_score_bad_coverage():
    res = pytest_runner.execution_result_score({"passed": True, "coverage_percent": "bad"}, 80)
    assert res == (0, 1, 0.0)

def test_parse_coverage_json_not_exists(tmp_path):
    pct, missing = pytest_runner._parse_coverage_json(tmp_path / "not_exists.json")
    assert pct == 0.0
    assert missing == []

def test_parse_coverage_json_invalid(tmp_path):
    p = tmp_path / "cov.json"
    p.write_text("invalid")
    assert pytest_runner._parse_coverage_json(p) == (0.0, [])

def test_parse_coverage_json_files_not_dict(tmp_path):
    p = tmp_path / "cov.json"
    p.write_text('{"files": "not_dict"}')
    assert pytest_runner._parse_coverage_json(p) == (0.0, [])

def test_parse_coverage_json_wrong_file(tmp_path):
    p = tmp_path / "cov.json"
    p.write_text('{"files": {"other.py": {"summary": {"percent_covered": 100}}}}')
    assert pytest_runner._parse_coverage_json(p) == (0.0, [])

def test_parse_coverage_json_file_data_not_dict(tmp_path):
    p = tmp_path / "cov.json"
    p.write_text('{"files": {"source_under_test.py": "bad"}}')
    assert pytest_runner._parse_coverage_json(p) == (0.0, [])

def test_parse_coverage_json_bad_percent(tmp_path):
    p = tmp_path / "cov.json"
    p.write_text('{"files": {"source_under_test.py": {"summary": {"percent_covered": "bad"}, "missing_lines": ["bad", 1]}}}')
    pct, missing = pytest_runner._parse_coverage_json(p)
    assert pct == 0.0
    assert missing == [1]

def test_write_execution_log(tmp_path):
    assert pytest_runner._write_execution_log(tmp_path / "log.txt", "hello") == str(tmp_path / "log.txt")
    
    # trigger OSError
    bad_path = tmp_path / "non_existent_dir" / "log.txt"
    assert pytest_runner._write_execution_log(bad_path, "hello") == ""

def test_diagnose_execution_issue():
    assert pytest_runner._diagnose_execution_issue("no tests ran", coverage_file_exists=True, coverage_percent=0.0) == "không có test hợp lệ được collect/chạy"
    assert pytest_runner._diagnose_execution_issue("collected 0 items", coverage_file_exists=True, coverage_percent=0.0) == "pytest không collect được test nào"
    assert pytest_runner._diagnose_execution_issue("error collecting", coverage_file_exists=True, coverage_percent=0.0) == "lỗi khi collect test"
    assert pytest_runner._diagnose_execution_issue("failed", coverage_file_exists=True, coverage_percent=0.0) == "test fail sớm trước khi cover được source"
    assert pytest_runner._diagnose_execution_issue("failed", coverage_file_exists=True, coverage_percent=10.0) == "test fail do assertion hoặc kỳ vọng exception sai"
    assert pytest_runner._diagnose_execution_issue("ok", coverage_file_exists=False, coverage_percent=0.0) == "không tạo được file coverage.json"
    assert pytest_runner._diagnose_execution_issue("ok", coverage_file_exists=True, coverage_percent=0.0) == "test chạy nhưng không chạm được source mục tiêu"
