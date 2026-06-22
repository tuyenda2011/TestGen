from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from testgen.executors.base import TestExecutionOutcome, TestExecutionRequest
from testgen.executors.external_command import ExternalCommandExecutor


class JestExecutor(ExternalCommandExecutor):
    framework = "Jest"
    display_name = "Jest"
    coverage_supported = True

    def execute(self, request: TestExecutionRequest) -> TestExecutionOutcome:
        workspace_dir = request.workspace_dir
        workspace_dir.mkdir(parents=True, exist_ok=True)

        test_path = workspace_dir / "generated.test.js"
        self._write_text(test_path, request.generated_test_code)
        source_path = ""
        if (request.source_code_text or "").strip():
            source_path = self._write_text(workspace_dir / "source_under_test.js", request.source_code_text)

        self._prepare_environment(workspace_dir)

        command = self._command_for_workspace(workspace_dir)
        unsafe_summary = self._validate_generated_code(
            request.generated_test_code,
            language="javascript",
            label="Generated Jest test",
            command=command,
            extra={"test_path": str(test_path), "source_path": source_path},
        )
        if unsafe_summary is not None:
            return TestExecutionOutcome(framework=self.framework, summary=unsafe_summary)

        process, early_summary = self._run_command(command, cwd=workspace_dir)
        if early_summary is not None:
            early_summary.update({"test_path": str(test_path), "source_path": source_path})
            return TestExecutionOutcome(framework=self.framework, summary=early_summary)

        assert process is not None
        output = (process.stdout or "") + (process.stderr or "")
        coverage_percent, coverage_path = self._read_coverage(workspace_dir)
        passed = process.returncode == 0
        
        json_path = workspace_dir / "jest_results.json"
        jest_json = {}
        if json_path.exists():
            try:
                jest_json = json.loads(json_path.read_text(encoding="utf-8"))
            except Exception:
                pass
                
        if jest_json:
            test_counts = {
                "tests_failed": jest_json.get("numFailedTests", 0),
                "tests_passed": jest_json.get("numPassedTests", 0),
                "tests_total": jest_json.get("numTotalTests", 0),
                "suites_failed": jest_json.get("numFailedTestSuites", 0),
                "suites_passed": jest_json.get("numPassedTestSuites", 0),
                "suites_total": jest_json.get("numTotalTestSuites", 0),
            }
            # Dịch ngược JSON thành Text dễ hiểu
            human_msgs = []
            for tr in jest_json.get("testResults", []):
                msg = tr.get("message")
                if msg:
                    human_msgs.append(msg)
            if human_msgs:
                output = "--- JEST ERROR DETAILS ---\n" + "\n\n".join(human_msgs)
        else:
            test_counts = self._parse_test_counts(output)
        
        issue_type = "none" if passed else "execution_failed"
        diagnosis = "Jest command passed." if passed else "Jest command failed."
        title = "Jest execution passed" if passed else "Jest execution failed"
        
        if not passed:
            if jest_json and jest_json.get("success") is False:
                issue_type = "test_failed"
                diagnosis = "Test logic failed (assertions or execution errors)."
                title = "Test Failure"
                for tr in jest_json.get("testResults", []):
                    message = tr.get("message", "")
                    if "SyntaxError" in message:
                        issue_type = "syntax_error"
                        diagnosis = "Syntax error in generated test code or source code."
                        title = "Syntax Error"
                        break
                    elif "Cannot find module" in message:
                        issue_type = "module_not_found"
                        diagnosis = "Import path incorrect or missing module."
                        title = "Module Not Found"
                        break
                    elif "TypeError" in message or "ReferenceError" in message or "Cannot read properties" in message:
                        issue_type = "runtime_type_error"
                        diagnosis = "Runtime error: TypeError or ReferenceError."
                        title = "Runtime Error"
                        break
                    elif "Expected" in message and "Received" in message or "expect(" in message:
                        issue_type = "assertion_error"
                        diagnosis = "Assertion failed. Test logic mismatch."
                        title = "Assertion Error"
                        break
            else:
                if "SyntaxError" in output:
                    issue_type = "syntax_error"
                    diagnosis = "Syntax error in generated test code or source code."
                    title = "Syntax Error"
                elif "Cannot find module" in output:
                    issue_type = "module_not_found"
                    diagnosis = "Import path incorrect or missing module."
                    title = "Module Not Found"
                elif "Command failed" in output or "npm ERR" in output or "npm error" in output:
                    issue_type = "environment_error"
                    diagnosis = "Failed to run Jest. Environment or dependencies missing."
                    title = "Environment Error"
                elif "TypeError" in output or "ReferenceError" in output or "Cannot read properties" in output:
                    issue_type = "runtime_type_error"
                    diagnosis = "Runtime error: TypeError or ReferenceError."
                    title = "Runtime Error"
                elif "Expected" in output and "Received" in output or "expect(" in output:
                    issue_type = "assertion_error"
                    diagnosis = "Assertion failed. Test logic mismatch."
                    title = "Assertion Error"
                else:
                    issue_type = "test_failed"
                    diagnosis = "Test logic failed (assertions or execution errors)."
                    title = "Test Failure"

        missing_lines = self._parse_clover_missing_lines(workspace_dir)

        summary = self._summary(
            passed=passed,
            command=command,
            output=output,
            diagnosis=diagnosis,
            issue_type=issue_type,
            title=title,
            hint="Review Jest output for failing suites or assertions." if not passed else "No action required.",
            coverage_percent=coverage_percent,
            extra={
                "test_path": str(test_path),
                "source_path": source_path,
                "coverage_path": coverage_path,
                "returncode": process.returncode,
                "execution_issue": {
                    "type": issue_type,
                    "title": title,
                    "hint": "Cập nhật lại test code dựa trên lỗi." if not passed else "",
                },
                "missing_lines": missing_lines,
                **test_counts,
            },
        )
        return TestExecutionOutcome(framework=self.framework, summary=summary)

    def _prepare_environment(self, workspace_dir: Path) -> None:
        package_json_path = workspace_dir / "package.json"
        # Luôn ghi đè package.json để đảm bảo cấu hình collectCoverageFrom luôn chính xác
        package_json_content = {
            "name": "test-workspace",
            "version": "1.0.0",
            "scripts": {
                "test": "jest"
            },
            "jest": {
                "coverageReporters": ["json-summary", "clover"],
                "collectCoverageFrom": ["source_under_test.js"]
            },
            "devDependencies": {
                "jest": "^29.0.0",
                "jest-environment-jsdom": "^29.0.0"
            }
        }
        self._write_text(package_json_path, json.dumps(package_json_content, indent=2))
        
        if not (workspace_dir / "node_modules").exists():
            import subprocess
            npm_cmd = self._which("npm") or "npm"
            try:
                subprocess.run(
                    [npm_cmd, "install", "--no-fund", "--no-audit", "--loglevel=error"], 
                    cwd=workspace_dir, 
                    capture_output=True, 
                    check=True
                )
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

    def _command_for_workspace(self, workspace_dir: Path) -> list[str]:
        base_flags = ["--coverage", "--runInBand", "--json", "--outputFile=jest_results.json", "--forceExit", "--env=jsdom"]
        if (workspace_dir / "package.json").exists():
            return ["npm", "test", "--"] + base_flags
        return ["npx", "--no-install", "jest"] + base_flags

    def _read_coverage(self, workspace_dir: Path) -> tuple[float, str]:
        coverage_path = workspace_dir / "coverage" / "coverage-summary.json"
        if not coverage_path.exists():
            return 0.0, ""
        try:
            payload = json.loads(coverage_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return 0.0, str(coverage_path)
        total = payload.get("total")
        if not isinstance(total, dict):
            return 0.0, str(coverage_path)
        for key in ("lines", "statements"):
            section = total.get(key)
            if isinstance(section, dict):
                pct_val = section.get("pct", 0.0)
                # Xử lý trường hợp Jest trả về chuỗi "Unknown" khi không có file nào được đo
                if isinstance(pct_val, str):
                    try:
                        pct_val = float(pct_val)
                    except (ValueError, TypeError):
                        continue
                try:
                    return float(pct_val), str(coverage_path)
                except (TypeError, ValueError):
                    continue
        return 0.0, str(coverage_path)

    def _parse_test_counts(self, output: str) -> dict[str, Any]:
        result: dict[str, Any] = {}
        tests_line = next(
            (line for line in (output or "").splitlines() if line.strip().startswith("Tests:")),
            "",
        )
        for key in ("failed", "passed", "total"):
            match = re.search(rf"(\d+)\s+{key}", tests_line)
            if match:
                result[f"tests_{key}"] = int(match.group(1))
        suites_line = next(
            (line for line in (output or "").splitlines() if line.strip().startswith("Test Suites:")),
            "",
        )
        for key in ("failed", "passed", "total"):
            match = re.search(rf"(\d+)\s+{key}", suites_line)
            if match:
                result[f"suites_{key}"] = int(match.group(1))
        return result

    def _parse_clover_missing_lines(self, workspace_dir: Path) -> list[int]:
        clover_path = workspace_dir / "coverage" / "clover.xml"
        if not clover_path.exists():
            return []
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(clover_path)
            root = tree.getroot()
            missing = []
            for file_elem in root.findall(".//file"):
                if "source_under_test" in file_elem.get("name", ""):
                    for line_elem in file_elem.findall("line"):
                        if line_elem.get("count") == "0":
                            num = line_elem.get("num")
                            if num and num.isdigit():
                                missing.append(int(num))
            return sorted(set(missing))
        except Exception:
            return []
