from __future__ import annotations

import json
from pathlib import Path
import re
import socket
from typing import Any
from urllib.parse import urlparse

from testgen.executors.base import TestExecutionOutcome, TestExecutionRequest
from testgen.executors.external_command import ExternalCommandExecutor


class NewmanExecutor(ExternalCommandExecutor):
    framework = "Postman script"
    display_name = "Newman"
    retry_supported = False

    def execute(self, request: TestExecutionRequest) -> TestExecutionOutcome:
        workspace_dir = request.workspace_dir
        workspace_dir.mkdir(parents=True, exist_ok=True)

        prepared = self._prepare_collection_payload(request.generated_test_code)
        if prepared["issue_type"]:
            return TestExecutionOutcome(
                framework=self.framework,
                summary=self._artifact_failure_summary(prepared, workspace_dir),
            )

        collection_text = str(prepared["collection_text"])
        static_quality = self._analyze_postman_static_quality(collection_text)
        
        has_assertions = int(static_quality.get("assertions_total", 0) or 0) > 0
        has_body_or_schema = bool(static_quality.get("body_assert_present", False) or static_quality.get("schema_assert_present", False))

        if not has_assertions or not has_body_or_schema:
            prepared["issue_type"] = "weak_postman_assertion"
            prepared["static_quality"] = static_quality
            return TestExecutionOutcome(
                framework=self.framework,
                summary=self._artifact_failure_summary(prepared, workspace_dir),
            )
        
        collection_path = workspace_dir / "collection.json"
        self._write_text(collection_path, collection_text)
        report_path = workspace_dir / "report.json"
        
        command = ["newman", "run", str(collection_path), "--reporters", "cli,json", "--reporter-json-export", str(report_path)]
        process, early_summary = self._run_command(command, cwd=workspace_dir)
        if early_summary is not None:
            return TestExecutionOutcome(framework=self.framework, summary=early_summary)
            
        passed = process.returncode == 0
        output = (process.stdout or "") + (process.stderr or "")
        
        failures = []
        stats = {}
        if report_path.exists():
            try:
                report_data = json.loads(report_path.read_text(encoding="utf-8"))
                failures = report_data.get("run", {}).get("failures", [])
                stats = report_data.get("run", {}).get("stats", {})
            except Exception:
                pass

        rows: list[dict[str, str]] = []
        for failure in failures[:10]:
            if not isinstance(failure, dict):
                continue
            source = failure.get("source")
            error = failure.get("error")
            rows.append(
                {
                    "name": self._failure_name(source),
                    "message": self._failure_message(error),
                }
            )

        issue_type = "none" if passed else "test_failed"
        diagnosis = "Postman tests passed." if passed else "Postman tests failed."
        title = "Postman Passed" if passed else "Postman Failed"

        if not passed and not report_path.exists():
            issue_type = "environment_error"
            diagnosis = "Newman failed to run or generate report."
            title = "Newman Error"

        summary = self._summary(
            passed=passed,
            command=command,
            output=output,
            diagnosis=diagnosis,
            issue_type=issue_type,
            title=title,
            hint="Review failures." if not passed else "",
            coverage_percent=0.0,
            extra={
                "postman_summary_path": self._write_postman_summary(workspace_dir, {"failures": rows, "stats": stats}) if report_path.exists() else "",
                "postman_static_quality": static_quality,
                "execution_issue": {
                    "type": issue_type,
                    "title": title,
                    "hint": "Check newman output.",
                },
                "tests_total": self._stat(stats, "tests", "total"),
                "tests_passed": self._stat(stats, "tests", "total") - self._stat(stats, "tests", "failed"),
                "tests_failed": self._stat(stats, "tests", "failed"),
                "assertions_total": self._stat(stats, "assertions", "total"),
                "assertions_failed": self._stat(stats, "assertions", "failed"),
            }
        )
        return TestExecutionOutcome(framework=self.framework, summary=summary)

    def _failure_name(self, value: Any) -> str:
        if isinstance(value, dict):
            for key in ("name", "id", "ref"):
                if value.get(key):
                    return str(value.get(key))
        return str(value or "")

    def _failure_message(self, value: Any) -> str:
        if isinstance(value, dict):
            for key in ("message", "stack", "name"):
                if value.get(key):
                    return str(value.get(key))
        return str(value or "")

    def _write_postman_summary(self, workspace_dir: Path, summary: dict[str, Any]) -> str:
        summary_path = workspace_dir / "postman_summary.json"
        payload = dict(summary)
        payload.pop("output", None)
        try:
            summary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            return ""
        return str(summary_path)

    def _stat(self, stats: dict[str, Any], section: str, key: str) -> int:
        value = stats.get(section)
        if not isinstance(value, dict):
            return 0
        try:
            return int(value.get(key, 0))
        except (TypeError, ValueError):
            return 0

    def _prepare_collection_payload(self, generated_code: str) -> dict[str, Any]:
        prepared = {
            "issue_type": "",
            "collection_text": (generated_code or "").strip(),
            "collection_data": {},
            "static_quality": {},
        }
        if not prepared["collection_text"]:
            prepared["issue_type"] = "invalid_postman_artifact"
            return prepared
        try:
            prepared["collection_data"] = json.loads(prepared["collection_text"])
        except json.JSONDecodeError:
            prepared["issue_type"] = "invalid_postman_artifact"
        return prepared

    def _analyze_postman_static_quality(self, collection_text: str) -> dict[str, Any]:
        text = collection_text or ""
        assertions = text.count("pm.test")
        body_assert = "pm.response.json()" in text or "pm.response.text()" in text
        schema_assert = "tv4.validate" in text or "ajv.validate" in text
        return {
            "assertions_total": assertions,
            "meaningful_assertion_count": assertions,
            "body_assert_present": body_assert,
            "schema_assert_present": schema_assert,
        }

    def _artifact_failure_summary(self, prepared: dict[str, Any], workspace_dir: Path) -> dict[str, Any]:
        return self._summary(
            passed=False,
            command=[],
            output="Invalid or missing Postman collection.",
            diagnosis="Generated code is not a valid JSON collection or lacks assertions.",
            issue_type=prepared.get("issue_type", "invalid_postman_artifact"),
            title="Artifact Failure",
            hint="Ensure the generated code is a valid Postman collection JSON.",
            coverage_percent=0.0,
            extra={
                "postman_static_quality": prepared.get("static_quality", {}),
                "execution_issue": {
                    "type": prepared.get("issue_type", "invalid_postman_artifact"),
                    "title": "Artifact Failure",
                    "hint": "Check generated code.",
                }
            }
        )
