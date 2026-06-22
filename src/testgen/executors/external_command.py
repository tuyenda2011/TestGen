from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
from typing import Any, Callable

from testgen.core.sandbox import validate_code_safety
from testgen.executors.base import TestExecutor


CommandRunner = Callable[..., subprocess.CompletedProcess[str]]
WhichFn = Callable[[str], str | None]


class ExternalCommandExecutor(TestExecutor):
    timeout_seconds = 60
    coverage_supported = False
    retry_supported = False

    def __init__(
        self,
        *,
        runner: CommandRunner = subprocess.run,
        which_fn: WhichFn = shutil.which,
        timeout_seconds: int | None = None,
    ) -> None:
        self._runner = runner
        self._which = which_fn
        if timeout_seconds is not None:
            self.timeout_seconds = timeout_seconds

    def _write_text(self, path: Path, text: str) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text or "", encoding="utf-8")
        return str(path)

    def _tool_exists(self, tool: str) -> bool:
        candidate = Path(tool)
        if candidate.parent != Path(".") and candidate.exists():
            return True
        return self._which(tool) is not None

    def _security_block_summary(
        self,
        *,
        command: list[str],
        reason: str,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._summary(
            passed=False,
            command=command,
            output=f"Security block: {reason}",
            diagnosis=f"Generated test code failed sandbox checks: {reason}",
            issue_type="security_block",
            title="Generated test code blocked by sandbox",
            hint="Remove process, filesystem, network, eval/exec, or dynamic import behavior from generated tests.",
            extra=extra,
        )

    def _validate_generated_code(
        self,
        code: str,
        *,
        language: str,
        label: str,
        command: list[str],
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        is_safe, reason = validate_code_safety(code, language=language, label=label)
        if is_safe:
            return None
        return self._security_block_summary(command=command, reason=reason, extra=extra)

    def _summary(
        self,
        *,
        passed: bool,
        command: list[str],
        output: str,
        diagnosis: str,
        issue_type: str,
        title: str,
        hint: str,
        coverage_percent: float = 0.0,
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        extra_payload = dict(extra or {})
        command_text = " ".join(command)
        coverage_path = str(extra_payload.get("coverage_path", "") or "")
        coverage_available = bool(coverage_path) or (self.coverage_supported and coverage_percent > 0.0)
        if coverage_available:
            coverage_status = "available"
        elif self.coverage_supported:
            coverage_status = "artifact_missing"
        else:
            coverage_status = "not_supported"
        summary: dict[str, Any] = {
            "passed": passed,
            "coverage_percent": coverage_percent,
            "coverage_ok": coverage_percent > 0.0,
            "coverage_supported": self.coverage_supported,
            "coverage_available": coverage_available,
            "coverage_status": coverage_status,
            "retry_supported": self.retry_supported,
            "output": (output or "").strip(),
            "diagnosis": diagnosis,
            "failure_summary": self._failure_summary(output),
            "command": command,
            "command_text": command_text,
            "execution_issue": {
                "type": issue_type,
                "title": title,
                "hint": hint,
                "missing_lines_count": "0",
            },
        }
        if extra_payload:
            summary.update(extra_payload)
        return summary

    def _run_command(
        self,
        command: list[str],
        *,
        cwd: Path,
    ) -> tuple[subprocess.CompletedProcess[str] | None, dict[str, Any] | None]:
        tool = command[0]
        resolved_tool = self._which(tool)
        candidate = Path(tool)
        
        if not resolved_tool and not (candidate.parent != Path(".") and candidate.exists()):
            return None, self._summary(
                passed=False,
                command=command,
                output="",
                diagnosis=f"Missing toolchain command: {tool}",
                issue_type="toolchain_missing",
                title=f"Missing command: {tool}",
                hint=f"Install {tool} or make it available on PATH before running this executor.",
                extra={"toolchain_missing": True},
            )

        # Build the actual command array to run
        run_command = list(command)
        if resolved_tool:
            run_command[0] = resolved_tool

        try:
            process = self._runner(
                run_command,
                capture_output=True,
                text=True,
                errors="replace",
                cwd=str(cwd),
                timeout=self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            output = (exc.stdout or "") + (exc.stderr or "")
            return None, self._summary(
                passed=False,
                command=command,
                output=output,
                diagnosis=f"Command timed out after {self.timeout_seconds} seconds.",
                issue_type="execution_timeout",
                title="External test command timed out",
                hint="Reduce test side effects or increase the executor timeout.",
            )
        except OSError as exc:
            return None, self._summary(
                passed=False,
                command=command,
                output=str(exc),
                diagnosis=f"Cannot run external test command: {exc}",
                issue_type="execution_error",
                title="External test command failed to start",
                hint="Check the project path and toolchain installation.",
            )

        return process, None

    def _failure_summary(self, output: str, max_chars: int = 1200) -> str:
        lines = (output or "").splitlines()
        selected = [
            line.strip()
            for line in lines
            if any(marker in line.lower() for marker in ("fail", "error", "exception"))
        ]
        summary = "\n".join(line for line in selected if line).strip()
        if not summary:
            summary = (output or "").strip()
        if len(summary) <= max_chars:
            return summary
        return summary[:max_chars].rstrip() + "\n..."
