from __future__ import annotations

from testgen.agents import formatter_agent
from testgen import run_history


def _configure_history_paths(tmp_path, monkeypatch):
    runs_root = tmp_path / "runs"
    monkeypatch.setattr(formatter_agent, "OUTPUT_PATH", runs_root)
    monkeypatch.setattr(run_history, "OUTPUT_RUNS_PATH", runs_root)
    monkeypatch.setattr(run_history, "HISTORY_INDEX_PATH", runs_root / "history_index.jsonl")
    return runs_root


def test_persist_and_load_history(tmp_path, monkeypatch):
    _configure_history_paths(tmp_path, monkeypatch)

    run_id = "run_20260528_190000_000001"
    run_dir = formatter_agent.resolve_run_dir(run_id, ensure_exists=True)
    code_path = run_dir / "test_code" / "sample.py"
    plan_path = run_dir / "test_plan" / "sample.xlsx"
    review_path = run_dir / "review_report" / "sample.pdf"
    review_md_path = run_dir / "review_report" / "sample.md"
    code_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    code_path.write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    plan_path.write_bytes(b"PK\x03\x04")
    review_path.write_bytes(b"%PDF")
    review_md_path.write_text("# Review\nOK", encoding="utf-8")

    run_history.persist_run_history(
        run_id=run_id,
        workflow="Sinh mã kiểm thử",
        mode="Multi-agent / Ollama",
        backend="ollama",
        framework="pytest",
        test_technique="Hybrid",
        code_path=str(code_path),
        test_plan_path=str(plan_path),
        review_path=str(review_path),
        review_md_path=str(review_md_path),
    )

    entries = run_history.load_history_entries(limit=10)
    assert len(entries) == 1
    assert entries[0]["run_id"] == run_id
    assert entries[0]["artifact_count"] == 4

    manifest = run_history.load_run_manifest(run_id)
    assert manifest is not None
    assert manifest.get("run_id") == run_id
    assert len(manifest.get("artifacts", [])) == 4
    labels = [item.get("label") for item in manifest.get("artifacts", [])]
    assert labels == ["Mã kiểm thử", "Kế hoạch kiểm thử", "Báo cáo rà soát", "Báo cáo rà soát Markdown"]


def test_delete_run_history_updates_index(tmp_path, monkeypatch):
    runs_root = _configure_history_paths(tmp_path, monkeypatch)

    run_id = "run_20260528_191500_000002"
    run_dir = formatter_agent.resolve_run_dir(run_id, ensure_exists=True)
    review_path = run_dir / "review_report" / "sample.pdf"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_bytes(b"%PDF")

    run_history.persist_run_history(
        run_id=run_id,
        workflow="Rà soát test code",
        mode="Multi-agent / Ollama",
        backend="ollama",
        framework="pytest",
        test_technique="Hybrid",
        review_path=str(review_path),
    )

    index_path = runs_root / "history_index.jsonl"
    assert index_path.exists()
    assert run_dir.exists()

    assert run_history.delete_run_history(run_id)
    assert not run_dir.exists()

    entries = run_history.load_history_entries(limit=10)
    assert entries == []

    index_content = index_path.read_text(encoding="utf-8").strip()
    assert index_content == ""


def test_persist_history_sanitizes_metadata_and_diagnostics(tmp_path, monkeypatch):
    _configure_history_paths(tmp_path, monkeypatch)

    run_id = "run_20260528_192000_000003"
    run_dir = formatter_agent.resolve_run_dir(run_id, ensure_exists=True)
    review_path = run_dir / "review_report" / "sample.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text("# Review", encoding="utf-8")

    run_history.persist_run_history(
        run_id=run_id,
        workflow="Review",
        mode="OpenRouter",
        backend="openrouter",
        framework="pytest",
        test_technique="Hybrid",
        review_md_path=str(review_path),
        diagnostics={"llm_calls_estimated": 2, "api_key": "sk-secret-value"},
        metadata={"token": "abcd1234secret", "models": {"review": "qwen"}},
    )

    manifest = run_history.load_run_manifest(run_id)
    assert manifest is not None
    assert manifest["diagnostics"]["api_key"] == "sk-s...alue"
    assert manifest["metadata"]["token"] == "abcd...cret"
    assert manifest["metadata"]["models"]["review"] == "qwen"


def test_persist_history_includes_pytest_log_artifacts(tmp_path, monkeypatch):
    _configure_history_paths(tmp_path, monkeypatch)

    run_id = "run_20260528_192500_000007"
    run_dir = formatter_agent.resolve_run_dir(run_id, ensure_exists=True)
    pytest_log = run_dir / "logs" / "pytest.log"
    collect_log = run_dir / "logs" / "pytest_collect_only.log"
    pytest_log.parent.mkdir(parents=True, exist_ok=True)
    pytest_log.write_text("1 passed", encoding="utf-8")
    collect_log.write_text("collected 1 item", encoding="utf-8")

    run_history.persist_run_history(
        run_id=run_id,
        workflow="Generate",
        mode="Ollama",
        backend="ollama",
        framework="pytest",
        test_technique="Hybrid",
        pytest_log_path=str(pytest_log),
        collection_log_path=str(collect_log),
    )

    manifest = run_history.load_run_manifest(run_id)
    labels = [item.get("label") for item in manifest.get("artifacts", [])]
    assert "Pytest log" in labels
    assert "Pytest collect-only log" in labels


def test_cleanup_run_history_keeps_newest_runs(tmp_path, monkeypatch):
    _configure_history_paths(tmp_path, monkeypatch)

    run_ids = [
        "run_20260528_193000_000004",
        "run_20260528_193100_000005",
        "run_20260528_193200_000006",
    ]
    for run_id in run_ids:
        run_dir = formatter_agent.resolve_run_dir(run_id, ensure_exists=True)
        review_path = run_dir / "review_report" / "sample.md"
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_text("# Review", encoding="utf-8")
        run_history.persist_run_history(
            run_id=run_id,
            workflow="Review",
            mode="Ollama",
            backend="ollama",
            framework="pytest",
            test_technique="Hybrid",
            review_md_path=str(review_path),
        )

    deleted = run_history.cleanup_run_history(max_runs=2)
    entries = run_history.load_history_entries(limit=10)

    assert len(deleted) == 1
    assert len(entries) == 2

