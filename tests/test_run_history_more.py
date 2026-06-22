import pytest
from pathlib import Path
from testgen import run_history

def test_to_file_size_oserror(tmp_path):
    assert run_history._to_file_size(tmp_path / "missing") == 0

def test_redact_secret_text():
    assert run_history._redact_secret_text("") == ""
    assert run_history._redact_secret_text("short") == "***"
    assert run_history._redact_secret_text("thisisverylongsecret") == "this...cret"

def test_sanitize_manifest_value():
    assert run_history._sanitize_manifest_value("depth test", depth=5) == "<truncated>"
    res = run_history._sanitize_manifest_value({
        "API_KEY": "secret",
        "nested": {"token": "sub"},
        "normal": "value",
        "list": [1, 2, "3"]
    })
    assert res["API_KEY"] == "***"
    assert res["nested"]["token"] == "***"
    assert res["normal"] == "value"
    assert res["list"] == [1, 2, "3"]

def test_safe_manifest_dict():
    assert run_history._safe_manifest_dict(None) == {}
    assert run_history._safe_manifest_dict({"a": 1}) == {"a": 1}

def test_artifact_entry_invalid(tmp_path):
    assert run_history._artifact_entry("k", "l", "") is None
    assert run_history._artifact_entry("k", "l", str(tmp_path / "missing")) is None
    assert run_history._artifact_entry("k", "l", str(tmp_path)) is None

def test_read_json_dict(tmp_path):
    assert run_history._read_json_dict(tmp_path / "missing") is None
    f = tmp_path / "bad.json"
    f.write_text("{bad")
    assert run_history._read_json_dict(f) is None
    f.write_text("[1, 2]")
    assert run_history._read_json_dict(f) is None

def test_artifact_count():
    assert run_history._artifact_count({}) == 0
    assert run_history._artifact_count({"artifacts": ["bad", {"a": 1}]}) == 1

def test_build_index_entry():
    assert run_history._build_index_entry({}, Path("f")) is None

def test_read_index_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(run_history, "HISTORY_INDEX_PATH", tmp_path / "idx")
    assert run_history._read_index_entries() == []
    
    idx = tmp_path / "idx"
    idx.write_text("\n{bad}\n{\"run_id\": 1}")
    assert len(run_history._read_index_entries()) == 1

def test_is_inside_outputs(tmp_path, monkeypatch):
    monkeypatch.setattr(run_history, "OUTPUT_RUNS_PATH", tmp_path / "runs")
    assert run_history._is_inside_outputs(tmp_path / "runs" / "abc") is True
    assert run_history._is_inside_outputs(tmp_path / "other") is False

def test_rebuild_history_index(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setattr(run_history, "OUTPUT_RUNS_PATH", runs)
    monkeypatch.setattr(run_history, "HISTORY_INDEX_PATH", tmp_path / "idx")
    
    run1 = runs / "date" / "run1"
    run1.mkdir(parents=True)
    (run1 / "manifest.json").write_text('{"run_id": "run1"}')
    
    # Missing run_id
    run2 = runs / "date" / "run2"
    run2.mkdir(parents=True)
    (run2 / "manifest.json").write_text('{"other": 1}')
    
    res = run_history.rebuild_history_index()
    assert len(res) == 1
    assert res[0]["run_id"] == "run1"

def test_load_run_manifest_glob(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setattr(run_history, "OUTPUT_RUNS_PATH", runs)
    
    run = runs / "a" / "b" / "run_abc"
    run.mkdir(parents=True)
    (run / "manifest.json").write_text('{"run_id": "run_abc"}')
    
    assert run_history.load_run_manifest("run_abc") is not None
    assert run_history.load_run_manifest("run_missing") is None

def test_cleanup_run_history_invalid_date(tmp_path, monkeypatch):
    monkeypatch.setattr(run_history, "OUTPUT_RUNS_PATH", tmp_path / "runs")
    monkeypatch.setattr(run_history, "HISTORY_INDEX_PATH", tmp_path / "idx")
    
    # fake entries
    def fake_load(*args, **kwargs):
        return [{"run_id": "1", "created_at": "bad-date"}, {"run_id": "2", "created_at": "2026-01-01T00:00:00"}]
    monkeypatch.setattr(run_history, "load_history_entries", fake_load)
    monkeypatch.setattr(run_history, "delete_run_history", lambda x: True)
    
    deleted = run_history.cleanup_run_history(max_runs=0, max_age_days=10)
    assert "2" in deleted
    assert "1" not in deleted
