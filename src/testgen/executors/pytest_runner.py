from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

from testgen.core.logger import get_logger
from testgen.core.sandbox import is_safe_python_code

logger = get_logger(__name__)


def execution_result_score(summary: dict[str, Any], coverage_threshold: float) -> tuple[int, int, float]:
    try:
        coverage_percent = float(summary.get("coverage_percent", 0.0))
    except (TypeError, ValueError):
        coverage_percent = 0.0
    passed = bool(summary.get("passed", False))
    return (
        1 if passed and coverage_percent >= coverage_threshold else 0,
        1 if passed else 0,
        coverage_percent,
    )


def _parse_coverage_json(coverage_path: Path) -> tuple[float, list[int]]:
    if not coverage_path.exists():
        return 0.0, []

    try:
        payload = json.loads(coverage_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0.0, []

    files = payload.get("files")
    if not isinstance(files, dict):
        return 0.0, []

    for file_key, file_data in files.items():
        if Path(str(file_key)).stem != "source_under_test":
            continue
        if not isinstance(file_data, dict):
            continue
        summary = file_data.get("summary")
        missing_lines = file_data.get("missing_lines")
        percent = 0.0
        if isinstance(summary, dict):
            try:
                percent = float(summary.get("percent_covered", 0.0))
            except (TypeError, ValueError):
                percent = 0.0
        normalized_missing: list[int] = []
        if isinstance(missing_lines, list):
            for value in missing_lines:
                try:
                    normalized_missing.append(int(value))
                except (TypeError, ValueError):
                    continue
        return percent, normalized_missing

    return 0.0, []


def _write_execution_log(path: Path, text: str) -> str:
    try:
        path.write_text(text or "", encoding="utf-8")
    except OSError:
        return ""
    return str(path)


def _diagnose_execution_issue(
    output: str,
    *,
    coverage_file_exists: bool,
    coverage_percent: float,
    enable_coverage: bool = True,
) -> str:
    text = (output or "").lower()
    if "unrecognized arguments" in text and "--cov" in text:
        return "thiếu plugin pytest-cov trong môi trường chạy"
    if "modulenotfounderror" in text and "playwright" in text:
        return "thiếu package playwright trong môi trường đang chạy"
    if "modulenotfounderror" in text and "selenium" in text:
        return "thiếu package selenium trong môi trường đang chạy"
    if "executable doesn't exist" in text and "playwright" in text:
        return "thiếu trình duyệt playwright, cần chạy playwright install"
    if "modulenotfounderror" in text:
        return "import lỗi (ModuleNotFoundError) trong test hoặc source"
    if "syntaxerror" in text:
        return "syntax lỗi trong source/test sinh ra"
    if "no tests ran" in text:
        return "không có test hợp lệ được collect/chạy"
    if "collected 0 items" in text:
        return "pytest không collect được test nào"
    if "error collecting" in text:
        return "lỗi khi collect test"
    if "failed" in text and coverage_percent == 0.0:
        return "test fail sớm trước khi cover được source"
    if "failed" in text:
        return "test fail do assertion hoặc kỳ vọng exception sai"
    if not coverage_file_exists and enable_coverage:
        return "không tạo được file coverage.json"
    if coverage_percent == 0.0:
        return "test chạy nhưng không chạm được source mục tiêu"
    return ""


def classify_execution_issue(
    output: str,
    *,
    collection_passed: bool,
    passed: bool,
    coverage_file_exists: bool,
    coverage_percent: float,
    coverage_threshold: float,
    missing_lines: list[int] | None = None,
    enable_coverage: bool = True,
) -> dict[str, str]:
    text = (output or "").lower()
    missing_count = len(missing_lines or [])

    if "syntaxerror" in text:
        issue_type = "syntax_error"
        title = "Syntax lỗi trong source/test sinh ra"
        hint = "Sửa cú pháp test trước khi bàn tới coverage."
    elif "modulenotfounderror" in text and "selenium" in text:
        issue_type = "selenium_package_missing"
        title = "Thiếu package selenium"
        hint = "Cài selenium vào đúng Python environment đang chạy ứng dụng."
    elif "modulenotfounderror" in text and "playwright" in text:
        issue_type = "playwright_package_missing"
        title = "Thiếu package playwright"
        hint = "Cài pytest-playwright vào đúng Python environment đang chạy ứng dụng."
    elif "executable doesn't exist" in text and "playwright" in text:
        issue_type = "playwright_browser_missing"
        title = "Thiếu trình duyệt Playwright"
        hint = "Chạy 'playwright install' để cài đặt các trình duyệt cần thiết."
    elif "modulenotfounderror" in text or "importerror" in text:
        issue_type = "import_error"
        title = "Import lỗi trong test hoặc source"
        hint = "Kiểm tra import target từ source_under_test và không bịa dependency."
    elif not collection_passed or "error collecting" in text:
        issue_type = "collection_error"
        title = "Pytest không collect được test"
        hint = "Sửa lỗi collection/import/name/syntax trước khi chạy coverage."
    elif "did not raise" in text:
        issue_type = "wrong_exception_expectation"
        title = "Kỳ vọng exception sai so với source"
        hint = "Đọc lại source; chỉ dùng pytest.raises khi source thật sự raise exception đó."
    elif (
        "assertionerror" in text
        or re.search(r"(?m)^e\s+assert\b", output or "")
        or ("failed" in text and (coverage_file_exists or not enable_coverage))
    ):
        issue_type = "wrong_expected_value"
        title = "Expected value/assertion sai so với source"
        hint = "Sửa expected value theo source code, không sửa source."
    elif passed and coverage_percent < coverage_threshold and missing_count:
        issue_type = "low_coverage"
        title = "Test pass nhưng coverage chưa đạt"
        hint = "Sinh thêm test cho branch/exception chứa missing lines."
    elif "no tests ran" in text or "collected 0 items" in text:
        issue_type = "weak_assertion"
        title = "Không có test hợp lệ được collect/chạy"
        hint = "Sinh test function có tên test_* và assert/pytest.raises rõ ràng."
    elif not coverage_file_exists and enable_coverage:
        issue_type = "coverage_artifact_missing"
        title = "Không tạo được coverage artifact"
        hint = "Kiểm tra pytest-cov và lệnh coverage."
    elif passed:
        issue_type = "none"
        title = "Không phát hiện lỗi execution chắc chắn"
        hint = "Tiếp tục review chất lượng assert và coverage."
    else:
        issue_type = "execution_error"
        title = "Lỗi execution chưa phân loại"
        hint = "Đọc pytest output để xác định lỗi cụ thể."

    return {
        "type": issue_type,
        "title": title,
        "hint": hint,
        "missing_lines_count": str(missing_count),
    }


def _extract_failure_summary(output: str, max_chars: int = 1200) -> str:
    lines = (output or "").splitlines()
    selected: list[str] = []
    patterns = (
        re.compile(r"^FAILED\s+"),
        re.compile(r"^E\s+"),
        re.compile(r"^>"),
        re.compile(r"_{5,}\s+test_"),
    )

    for line in lines:
        stripped = line.rstrip()
        if any(pattern.search(stripped) for pattern in patterns):
            selected.append(stripped)
        if len("\n".join(selected)) >= max_chars:
            break

    if not selected:
        for line in lines:
            stripped = line.strip()
            if re.search(r"\b(failed|error|failed,|errors?)\b", stripped, flags=re.IGNORECASE):
                selected.append(stripped)
            if len("\n".join(selected)) >= max_chars:
                break

    summary = "\n".join(selected).strip()
    if len(summary) <= max_chars:
        return summary
    return summary[:max_chars].rstrip() + "\n..."


def _combined_report_payload(
    *,
    passed: bool,
    coverage_percent: float,
    missing_lines: list[int],
    output: str,
    coverage_path: Path,
    test_paths: list[Path],
    pytest_log_path: str = "",
    collection_log_path: str = "",
) -> dict[str, Any]:
    return {
        "passed": passed,
        "coverage_percent": coverage_percent,
        "missing_lines": missing_lines,
        "coverage_path": str(coverage_path) if coverage_path.exists() else "",
        "test_paths": [str(path) for path in test_paths],
        "output": (output or "").strip(),
        "pytest_log_path": pytest_log_path,
        "collection_log_path": collection_log_path,
    }

def _analyze_pytest_static_quality(generated_code: str, is_e2e: bool) -> dict[str, Any]:
    if not generated_code:
        return {}
    
    try:
        tree = ast.parse(generated_code)
    except SyntaxError:
        return {}
        
    assertions_total = 0
    meaningful_assertions = 0
    uses_sleep = False
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            assertions_total += 1
            meaningful_assertions += 1
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                if is_e2e and method_name in {
                    "find_element", "find_elements", "locator", "click", "fill", "send_keys", "expect"
                }:
                    meaningful_assertions += 1
                if method_name == "sleep":
                    uses_sleep = True
            elif isinstance(node.func, ast.Name):
                if node.func.id == "sleep":
                    uses_sleep = True
                if node.func.id == "expect":
                    meaningful_assertions += 1
        elif isinstance(node, ast.With):
            for item in node.items:
                if isinstance(item.context_expr, ast.Call):
                    if isinstance(item.context_expr.func, ast.Attribute) and item.context_expr.func.attr == "raises":
                        meaningful_assertions += 1
                    elif isinstance(item.context_expr.func, ast.Name) and item.context_expr.func.id == "raises":
                        meaningful_assertions += 1

    return {
        "assertions_total": assertions_total,
        "assertion_count": assertions_total,
        "meaningful_assertion_count": meaningful_assertions,
        "uses_sleep": uses_sleep,
        "negative_or_boundary_evidence": True
    }

def _is_safe_code(code: str) -> tuple[bool, str]:
    return is_safe_python_code(code)

def run_generated_pytest_with_coverage(
    *,
    source_code_text: str,
    generated_test_code: str,
    workspace_dir: Path,
    coverage_threshold: float = 80.0,
    enable_coverage: bool = True,
    source_filename: str = "source_under_test.py",
    is_e2e: bool = False,
) -> dict[str, Any]:
    workspace_dir.mkdir(parents=True, exist_ok=True)

    is_safe, reason = is_safe_python_code(generated_test_code, allow_e2e=is_e2e)
    if not is_safe:
        logger.error(f"Soft Sandbox block: {reason}")
        return {
            "passed": False,
            "coverage_percent": 0.0,
            "missing_lines": [],
            "coverage_ok": False,
            "output": f"Bảo mật: Mã kiểm thử bị từ chối do chứa lệnh nguy hiểm.\nLý do: {reason}",
            "diagnosis": "Mã chứa hàm/thư viện nguy hiểm (os, subprocess, eval...)",
            "execution_issue": {
                "type": "security_block",
                "title": "Mã test chứa thao tác bị chặn",
                "hint": "Loại bỏ import/hàm nguy hiểm trước khi chạy test.",
                "missing_lines_count": "0",
            },
            "failure_summary": f"Security Block: {reason}",
            "source_path": "",
            "test_path": "",
            "coverage_path": "",
            "pytest_log_path": "",
            "collection_log_path": "",
        }

    source_path = workspace_dir / source_filename
    test_path = workspace_dir / "test_generated.py"
    coverage_path = workspace_dir / "coverage.json"
    pytest_ini_path = workspace_dir / "pytest.ini"
    pytest_log_path = workspace_dir / "pytest.log"
    collection_log_path = workspace_dir / "pytest_collect_only.log"

    source_path.write_text(source_code_text or "", encoding="utf-8")
    test_path.write_text(generated_test_code or "", encoding="utf-8")
    pytest_ini_path.write_text("[pytest]\naddopts =\n", encoding="utf-8")

    collect_command = [
        sys.executable,
        "-m",
        "pytest",
        str(test_path),
        "--collect-only",
        "-q",
        "-c",
        str(pytest_ini_path),
    ]

    try:
        collect_process = subprocess.run(
            collect_command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(workspace_dir),
            timeout=30,
        )
        collect_output = (collect_process.stdout or "") + (collect_process.stderr or "")
    except subprocess.TimeoutExpired as e:
        logger.error("Pytest collection timeout expired!")
        output = f"Lỗi: Quá trình collect test chạy quá 30 giây.\n{e.stdout or ''}"
        return {
            "passed": False,
            "coverage_percent": 0.0,
            "missing_lines": [],
            "coverage_ok": False,
            "output": output,
            "diagnosis": "Timeout 30s khi collect test",
            "execution_issue": {
                "type": "collection_timeout",
                "title": "Timeout khi collect test",
                "hint": "Loại bỏ import/side effect làm treo quá trình collect.",
                "missing_lines_count": "0",
            },
            "failure_summary": "Test collection timed out after 30 seconds.",
            "source_path": str(source_path),
            "test_path": str(test_path),
            "coverage_path": "",
            "pytest_log_path": "",
            "collection_log_path": _write_execution_log(collection_log_path, output),
            "collection_passed": False,
            "collection_output": output,
        }

    if collect_process.returncode != 0:
        diagnosis = _diagnose_execution_issue(
            collect_output,
            coverage_file_exists=False,
            coverage_percent=0.0,
            enable_coverage=enable_coverage,
        ) or "lỗi khi collect test"
        execution_issue = classify_execution_issue(
            collect_output,
            collection_passed=False,
            passed=False,
            coverage_file_exists=False,
            coverage_percent=0.0,
            coverage_threshold=coverage_threshold,
            missing_lines=[],
            enable_coverage=enable_coverage,
        )
        failure_summary = _extract_failure_summary(collect_output) or collect_output.strip()[:1200]
        return {
            "passed": False,
            "coverage_percent": 0.0,
            "missing_lines": [],
            "coverage_ok": False,
            "output": collect_output.strip(),
            "diagnosis": diagnosis,
            "execution_issue": execution_issue,
            "failure_summary": failure_summary,
            "source_path": str(source_path),
            "test_path": str(test_path),
            "coverage_path": "",
            "pytest_log_path": "",
            "collection_log_path": _write_execution_log(collection_log_path, collect_output.strip()),
            "collection_passed": False,
            "collection_output": collect_output.strip(),
        }



    command_eval = [
        sys.executable,
        "-m",
        "pytest",
        str(test_path),
        "-q",
        "-c",
        str(pytest_ini_path),
    ]
    if enable_coverage:
        command_eval[4:4] = [
            f"--cov={Path(source_filename).stem}",
            f"--cov-report=json:{coverage_path.name}",
            "--cov-report=term-missing"
        ]
        
    try:
        # Chạy kiểm tra sạch để đo coverage và lấy Exit Code chuẩn
        process = subprocess.run(
            command_eval,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(workspace_dir),
            timeout=120,
            stdin=subprocess.DEVNULL, 
        )
        output = (process.stdout or "") + (process.stderr or "")
        
        final_generated_code = test_path.read_text(encoding="utf-8")

    except subprocess.TimeoutExpired as e:
        logger.error("Subprocess timeout expired during evaluation!")
        output = f"Lỗi: Quá trình kiểm thử chạy quá 120 giây (có thể do lặp vô hạn hoặc sleep).\n{e.stdout or ''}"
        return {
            "passed": False,
            "coverage_percent": 0.0,
            "missing_lines": [],
            "coverage_ok": False,
            "output": output,
            "diagnosis": "Timeout 120s - Test bị treo",
            "execution_issue": {
                "type": "execution_timeout",
                "title": "Timeout khi chạy test",
                "hint": "Loại bỏ vòng lặp/sleep/side effect làm test treo.",
                "missing_lines_count": "0",
            },
            "failure_summary": "Test execution timed out after 120 seconds.",
            "source_path": str(source_path),
            "test_path": str(test_path),
            "coverage_path": "",
            "pytest_log_path": _write_execution_log(pytest_log_path, output),
            "collection_log_path": _write_execution_log(collection_log_path, collect_output.strip()),
            "collection_passed": True,
            "collection_output": collect_output.strip(),
        }

    coverage_percent, missing_lines = _parse_coverage_json(coverage_path) if enable_coverage else (0.0, [])
    saved_pytest_log = _write_execution_log(pytest_log_path, output.strip())
    saved_collection_log = _write_execution_log(collection_log_path, collect_output.strip())
    diagnosis = _diagnose_execution_issue(
        output,
        coverage_file_exists=coverage_path.exists(),
        coverage_percent=coverage_percent,
        enable_coverage=enable_coverage,
    )
    failure_summary = _extract_failure_summary(output) if process.returncode != 0 else ""
    passed = process.returncode == 0
    output_text = output.strip()
    execution_issue = classify_execution_issue(
        output_text,
        collection_passed=True,
        passed=passed,
        coverage_file_exists=coverage_path.exists(),
        coverage_percent=coverage_percent,
        coverage_threshold=coverage_threshold,
        missing_lines=missing_lines,
        enable_coverage=enable_coverage,
    )
    combined_report = _combined_report_payload(
        passed=passed,
        coverage_percent=coverage_percent,
        missing_lines=missing_lines,
        output=output_text,
        coverage_path=coverage_path,
        test_paths=[test_path],
        pytest_log_path=saved_pytest_log,
        collection_log_path=saved_collection_log,
    )
    
    issue_type = execution_issue["type"]
    if issue_type in ["selenium_package_missing", "playwright_package_missing"]:
        failure_stage = "preflight"
    elif issue_type == "import_error":
        failure_stage = "import"
    elif issue_type in ["driver_missing", "playwright_browser_missing"]:
        failure_stage = "browser_boot"
    elif issue_type in ["target_fixture_not_opened", "network_not_allowed"]:
        failure_stage = "fixture_navigation"
    elif issue_type in ["unstable_locator", "locator_not_found", "timeout_wait_error"]:
        failure_stage = "interaction"
    elif issue_type in ["wrong_expected_value", "assertion_error"]:
        failure_stage = "assertion"
    else:
        failure_stage = "unknown"

    static_quality = _analyze_pytest_static_quality(final_generated_code, is_e2e)

    return {
        "e2e_static_quality": static_quality if is_e2e else {},
        "pytest_static_quality": static_quality if not is_e2e else {},
        "passed": passed,
        "coverage_percent": coverage_percent,
        "missing_lines": missing_lines,
        "coverage_ok": coverage_percent >= coverage_threshold if enable_coverage else True,
        "output": output_text,
        "diagnosis": diagnosis,
        "execution_issue": execution_issue,
        "failure_summary": failure_summary,
        "source_path": str(source_path),
        "test_path": str(test_path),
        "coverage_path": str(coverage_path) if coverage_path.exists() else "",
        "pytest_log_path": saved_pytest_log,
        "collection_log_path": saved_collection_log,
        "collection_passed": True,
        "collection_output": collect_output.strip(),
        "final_code": final_generated_code,
        "coverage_supported": enable_coverage,
        "coverage_available": coverage_path.exists() if enable_coverage else False,
        "coverage_status": "supported" if enable_coverage else "not_supported",
        "quality_gate": "coverage" if enable_coverage else "e2e_flow_assertions",
        "failure_stage": failure_stage if not passed else "",
        "combined_report": combined_report,
        "combined_coverage_percent": coverage_percent,
        "combined_missing_lines": missing_lines,
    }
