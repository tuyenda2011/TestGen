from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from shutil import rmtree
from typing import Any

from testgen.agents.formatter_agent import resolve_run_dir
from testgen.core.config import OUTPUT_RUNS_PATH as DEFAULT_OUTPUT_RUNS_PATH


OUTPUT_RUNS_PATH = DEFAULT_OUTPUT_RUNS_PATH
HISTORY_INDEX_PATH = OUTPUT_RUNS_PATH / "history_index.jsonl"
MANIFEST_FILENAME = "manifest.json"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _to_file_size(path: Path) -> int:
    try:
        return int(path.stat().st_size)
    except OSError:
        return 0


def _as_clean_str(value: Any) -> str:
    return str(value or "").strip()


def _redact_secret_text(value: str) -> str:
    cleaned = _as_clean_str(value)
    if not cleaned:
        return ""
    if len(cleaned) <= 8:
        return "***"
    return f"{cleaned[:4]}...{cleaned[-4:]}"


def _sanitize_manifest_value(value: Any, depth: int = 0) -> Any:
    if depth > 4:
        return "<truncated>"
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            lower_key = key_text.lower()
            if any(marker in lower_key for marker in ("api_key", "apikey", "token", "secret", "authorization")):
                sanitized[key_text] = _redact_secret_text(str(item))
            else:
                sanitized[key_text] = _sanitize_manifest_value(item, depth + 1)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_manifest_value(item, depth + 1) for item in value[:200]]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _safe_manifest_dict(value: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    sanitized = _sanitize_manifest_value(value)
    return sanitized if isinstance(sanitized, dict) else {}


def _artifact_entry(kind: str, label: str, path: str) -> dict[str, Any] | None:
    candidate = _as_clean_str(path)
    if not candidate:
        return None

    file_path = Path(candidate)
    if not file_path.exists() or file_path.is_dir():
        return None

    return {
        "kind": kind,
        "label": label,
        "path": str(file_path.resolve()),
        "name": file_path.name,
        "size_bytes": _to_file_size(file_path),
        "extension": file_path.suffix.lower(),
    }


def _read_json_dict(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(payload, dict):
        return None
    return payload


def _artifact_count(manifest: dict[str, Any]) -> int:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return 0
    return len([item for item in artifacts if isinstance(item, dict)])


def _build_index_entry(manifest: dict[str, Any], manifest_path: Path) -> dict[str, Any] | None:
    run_id = _as_clean_str(manifest.get("run_id"))
    if not run_id:
        return None

    run_dir = manifest_path.parent
    return {
        "run_id": run_id,
        "created_at": _as_clean_str(manifest.get("created_at")),
        "workflow": _as_clean_str(manifest.get("workflow")),
        "mode": _as_clean_str(manifest.get("mode")),
        "backend": _as_clean_str(manifest.get("backend")),
        "framework": _as_clean_str(manifest.get("framework")),
        "test_technique": _as_clean_str(manifest.get("test_technique")),
        "artifact_count": _artifact_count(manifest),
        "run_dir": str(run_dir.resolve()),
        "manifest_path": str(manifest_path.resolve()),
    }


def _read_index_entries() -> list[dict[str, Any]]:
    if not HISTORY_INDEX_PATH.exists():
        return []

    try:
        lines = HISTORY_INDEX_PATH.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []

    entries: list[dict[str, Any]] = []
    for line in lines:
        payload = line.strip()
        if not payload:
            continue
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            entries.append(data)
    return entries


def _sort_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        entries,
        key=lambda item: (_as_clean_str(item.get("created_at")), _as_clean_str(item.get("run_id"))),
        reverse=True,
    )


def _deduplicate_by_run_id(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduplicated: dict[str, dict[str, Any]] = {}
    for item in entries:
        run_id = _as_clean_str(item.get("run_id"))
        if run_id:
            deduplicated[run_id] = item
    return list(deduplicated.values())


def _write_index_entries(entries: list[dict[str, Any]]) -> None:
    OUTPUT_RUNS_PATH.mkdir(parents=True, exist_ok=True)

    ordered = _sort_entries(_deduplicate_by_run_id(entries))
    lines = [json.dumps(entry, ensure_ascii=False) for entry in ordered]
    HISTORY_INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")


def _is_inside_outputs(path: Path) -> bool:
    try:
        path.resolve().relative_to(OUTPUT_RUNS_PATH.resolve())
        return True
    except ValueError:
        return False


def _entry_paths_exist(entry: dict[str, Any]) -> bool:
    manifest_path = Path(_as_clean_str(entry.get("manifest_path")))
    run_dir = Path(_as_clean_str(entry.get("run_dir")))
    return manifest_path.exists() and run_dir.exists()


def persist_run_history(
    *,
    run_id: str,
    workflow: str,
    mode: str,
    backend: str,
    framework: str,
    test_technique: str,
    code_path: str = "",
    test_plan_path: str = "",
    review_path: str = "",
    review_md_path: str = "",
    coverage_report_path: str = "",
    coverage_json_path: str = "",
    coverage_raw_path: str = "",
    pytest_log_path: str = "",
    collection_log_path: str = "",
    diagnostics: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    run_dir = resolve_run_dir(run_id, ensure_exists=True)
    artifacts = [
        _artifact_entry("generated_code", "Mã kiểm thử", code_path),
        _artifact_entry("test_plan", "Kế hoạch kiểm thử", test_plan_path),
        _artifact_entry("review_report", "Báo cáo rà soát", review_path),
        _artifact_entry("review_report_markdown", "Báo cáo rà soát Markdown", review_md_path),
        _artifact_entry("coverage_report", "Combined coverage report", coverage_report_path),
        _artifact_entry("coverage_json", "Combined coverage JSON", coverage_json_path),
        _artifact_entry("coverage_raw_json", "Raw coverage JSON", coverage_raw_path),
        _artifact_entry("pytest_log", "Pytest log", pytest_log_path),
        _artifact_entry("collect_only_log", "Pytest collect-only log", collection_log_path),
    ]
    artifact_entries = [item for item in artifacts if item is not None]

    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "created_at": _now_iso(),
        "workflow": workflow,
        "mode": mode,
        "backend": backend,
        "framework": framework,
        "test_technique": test_technique,
        "diagnostics": _safe_manifest_dict(diagnostics),
        "metadata": _safe_manifest_dict(metadata),
        "artifacts": artifact_entries,
    }

    manifest_path = run_dir / MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    entry = _build_index_entry(manifest, manifest_path)
    if not entry:
        return {}

    entries = _read_index_entries()
    entries = [item for item in entries if _as_clean_str(item.get("run_id")) != run_id]
    entries.append(entry)
    _write_index_entries(entries)
    return entry


def rebuild_history_index() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for manifest_path in OUTPUT_RUNS_PATH.glob(f"*/*/{MANIFEST_FILENAME}"):
        manifest = _read_json_dict(manifest_path)
        if manifest is None:
            continue

        entry = _build_index_entry(manifest, manifest_path)
        if entry is None:
            continue

        run_dir = Path(_as_clean_str(entry.get("run_dir")))
        if not run_dir.exists():
            continue
        entries.append(entry)

    _write_index_entries(entries)
    return _sort_entries(entries)


def load_history_entries(limit: int = 200) -> list[dict[str, Any]]:
    entries = _read_index_entries()
    if not entries:
        entries = rebuild_history_index()

    cleaned = [entry for entry in entries if _entry_paths_exist(entry)]
    if len(cleaned) != len(entries):
        _write_index_entries(cleaned)

    ordered = _sort_entries(cleaned)
    if limit <= 0:
        return ordered
    return ordered[:limit]


def load_run_manifest(run_id: str) -> dict[str, Any] | None:
    run_dir = resolve_run_dir(run_id, ensure_exists=False)
    manifest_path = run_dir / MANIFEST_FILENAME
    if manifest_path.exists():
        return _read_json_dict(manifest_path)

    for candidate in OUTPUT_RUNS_PATH.glob(f"*/*/{run_id}/{MANIFEST_FILENAME}"):
        manifest = _read_json_dict(candidate)
        if manifest is not None:
            return manifest
    return None


def delete_run_history(run_id: str) -> bool:
    run_dir = resolve_run_dir(run_id, ensure_exists=False)
    deleted = False

    if run_dir.exists() and _is_inside_outputs(run_dir):
        rmtree(run_dir, ignore_errors=False)
        deleted = True
        day_dir = run_dir.parent
        if day_dir.exists() and day_dir.is_dir() and not any(day_dir.iterdir()):
            day_dir.rmdir()

    entries = _read_index_entries()
    filtered = [item for item in entries if _as_clean_str(item.get("run_id")) != run_id]
    if len(filtered) != len(entries):
        _write_index_entries(filtered)
        deleted = True

    return deleted


def cleanup_run_history(max_runs: int = 100, max_age_days: int | None = None) -> list[str]:
    entries = load_history_entries(limit=0)
    now = datetime.now()
    to_delete: list[str] = []

    if max_age_days is not None and max_age_days >= 0:
        cutoff = now - timedelta(days=max_age_days)
        for entry in entries:
            created_at = _as_clean_str(entry.get("created_at"))
            try:
                created_dt = datetime.fromisoformat(created_at)
            except ValueError:
                continue
            if created_dt < cutoff:
                run_id = _as_clean_str(entry.get("run_id"))
                if run_id:
                    to_delete.append(run_id)

    if max_runs > 0:
        for entry in entries[max_runs:]:
            run_id = _as_clean_str(entry.get("run_id"))
            if run_id:
                to_delete.append(run_id)

    deleted: list[str] = []
    seen: set[str] = set()
    for run_id in to_delete:
        if run_id in seen:
            continue
        seen.add(run_id)
        if delete_run_history(run_id):
            deleted.append(run_id)
    return deleted


