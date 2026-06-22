from __future__ import annotations

from pathlib import Path
import re
from typing import Any
import xml.etree.ElementTree as ET

from testgen.executors.base import TestExecutionOutcome, TestExecutionRequest
from testgen.executors.external_command import ExternalCommandExecutor


class JUnitExecutor(ExternalCommandExecutor):
    framework = "JUnit"
    display_name = "JUnit via Maven/Gradle"
    coverage_supported = True
    retry_supported = True

    def _extract_public_class_name(self, code: str, default_name: str) -> str:
        if not code:
            return default_name
        match = re.search(r"public\s+class\s+(\w+)", code)
        if match:
            return match.group(1)
        return default_name

    def _extract_package_path(self, code: str) -> str:
        if not code:
            return ""
        match = re.search(r"package\s+([a-zA-Z0-9_.]+)\s*;", code)
        if match:
            return match.group(1).replace(".", "/")
        return ""

    def _analyze_junit_static_quality(self, generated_code: str) -> dict | None:
        if not generated_code:
            return None
            
        blocked_imports = []
        blocked_apis = []
        
        if re.search(r"import\s+java\.io\.", generated_code):
            blocked_imports.append("java.io.*")
        if re.search(r"import\s+java\.nio\.", generated_code):
            blocked_imports.append("java.nio.*")
        if re.search(r"import\s+java\.net\.", generated_code):
            blocked_imports.append("java.net.*")
            
        if "@TempDir" in generated_code:
            blocked_apis.append("@TempDir")
        if re.search(r"Files\.(write|delete|copy|move|readAllBytes|createTempDirectory)", generated_code):
            blocked_apis.append("Files.*")
        if "Runtime.getRuntime" in generated_code:
            blocked_apis.append("Runtime.getRuntime")
        if "ProcessBuilder" in generated_code:
            blocked_apis.append("ProcessBuilder")
            
        is_migration_test = "MigrationTest" in generated_code or "TempDirSharedTest" in generated_code
            
        if blocked_imports or blocked_apis or is_migration_test:
            reason = "Generated JUnit test uses unsafe filesystem/network APIs or tests framework extensions."
            return {
                "diagnosis": reason,
                "execution_issue": {
                    "type": "security_block",
                    "hint": "Remove tests that do not exercise the public APIs of the source class. Do not use @TempDir, java.nio, or java.io."
                },
                "security_block_reason": reason,
                "blocked_imports": blocked_imports,
                "blocked_apis": blocked_apis
            }
        return None

    def execute(self, request: TestExecutionRequest) -> TestExecutionOutcome:
        workspace_dir = request.workspace_dir
        workspace_dir.mkdir(parents=True, exist_ok=True)

        test_class_name = self._extract_public_class_name(request.generated_test_code, "GeneratedTest")
        test_pkg_path = self._extract_package_path(request.generated_test_code)
        test_dir = workspace_dir / "src" / "test" / "java"
        if test_pkg_path:
            test_dir = test_dir / test_pkg_path
            
        test_path = self._write_text(
            test_dir / f"{test_class_name}.java",
            request.generated_test_code,
        )
        
        source_path = ""
        source_code = request.source_code_text or ""
        if source_code.strip():
            source_class_name = self._extract_public_class_name(source_code, "SourceUnderTest")
            source_pkg_path = self._extract_package_path(source_code)
            source_dir = workspace_dir / "src" / "main" / "java"
            if source_pkg_path:
                source_dir = source_dir / source_pkg_path
                
            source_path = self._write_text(
                source_dir / f"{source_class_name}.java",
                source_code,
            )

        command = self._command_for_workspace(workspace_dir)
        if command is None:
            self._generate_default_pom(workspace_dir)
            command = ["mvn", "clean", "test", "jacoco:report"]

        static_summary = self._analyze_junit_static_quality(request.generated_test_code)
        if static_summary is not None:
            return TestExecutionOutcome(
                framework=self.framework,
                summary=self._summary(
                    passed=False,
                    command=command,
                    output="",
                    diagnosis=static_summary["diagnosis"],
                    issue_type="security_block",
                    title="JUnit execution blocked",
                    hint=static_summary["execution_issue"]["hint"],
                    coverage_percent=0.0,
                    extra={
                        "test_path": str(test_path),
                        "source_path": str(source_path),
                        "execution_issue": static_summary["execution_issue"],
                        "junit_security_block_reason": static_summary["security_block_reason"],
                        "junit_blocked_imports": static_summary["blocked_imports"],
                        "junit_blocked_apis": static_summary["blocked_apis"],
                        "combined_report": {
                            "passed": False,
                            "coverage_percent": 0.0,
                            "output": static_summary["diagnosis"]
                        }
                    }
                )
            )

        unsafe_summary = self._validate_generated_code(
            request.generated_test_code,
            language="java",
            label="Generated JUnit test",
            command=command,
            extra={"test_path": test_path, "source_path": source_path},
        )
        if unsafe_summary is not None:
            return TestExecutionOutcome(framework=self.framework, summary=unsafe_summary)

        process, early_summary = self._run_command(command, cwd=workspace_dir)
        if early_summary is not None:
            early_summary.update({"test_path": test_path, "source_path": source_path})
            return TestExecutionOutcome(framework=self.framework, summary=early_summary)

        assert process is not None
        output = (process.stdout or "") + (process.stderr or "")
        xml_summary = self._parse_xml_reports(workspace_dir)
        passed = process.returncode == 0 and int(xml_summary.get("failures", 0)) == 0 and int(xml_summary.get("errors", 0)) == 0
        issue_type = "none" if passed else "execution_failed"
        
        coverage_percent, missing_lines, coverage_path, coverage_gaps = self._read_jacoco_coverage(workspace_dir)
        
        diagnosis = "JUnit command passed." if passed else "JUnit command failed."
        execution_issue = {}

        if passed and coverage_percent < request.coverage_threshold:
            issue_type = "low_coverage"
            diagnosis = f"JUnit pass nhưng JaCoCo coverage {coverage_percent:.1f}% thấp hơn ngưỡng {request.coverage_threshold}%."
            execution_issue = {
                "type": "low_coverage",
                "hint": "Bổ sung test cho method/branch/missing lines chưa cover."
            }

        if not passed:
            if "COMPILATION ERROR" in output:
                lines = output.splitlines()
                err_lines = [
                    line.replace("[ERROR]", "").strip() 
                    for line in lines 
                    if line.startswith("[ERROR]") 
                    and "COMPILATION ERROR" not in line 
                    and "Failed to execute" not in line
                    and "Help 1" not in line
                    and "see the full stack trace" not in line
                    and "Re-run Maven" not in line
                    and "For more information" not in line
                    and "->" not in line
                ]
                if err_lines:
                    diagnosis = f"Lỗi biên dịch Java: {err_lines[0]}"
                    if "/src/main/java/" in err_lines[0].replace("\\", "/"):
                        issue_type = "source_compilation_error"
                        execution_issue = {"type": issue_type, "hint": "Sửa lỗi cú pháp trong mã nguồn (Source)."}
                    else:
                        issue_type = "test_compilation_error"
                        execution_issue = {"type": issue_type, "hint": "Sửa lỗi cú pháp trong mã kiểm thử (GeneratedTest)."}
            elif "AssertionFailedError" in output or "AssertionError" in output:
                issue_type = "assertion_error"
                diagnosis = "Có test case thất bại do logic Assertion sai."
                if "delta" in output.lower() or "deprecated" in output.lower():
                    execution_issue = {"type": issue_type, "hint": "Lỗi so sánh số thực. Bạn phải thêm tham số sai số delta vào hàm assertEquals (ví dụ: `assertEquals(expected, actual, 0.001)`)."}
                else:
                    execution_issue = {"type": issue_type, "hint": "Sửa lại giá trị expected hoặc điều kiện assert cho khớp chính xác với kết quả trả về từ source code (ưu tiên Actual value). Nếu code thật văng exception, phải dùng assertThrows thay vì kiểm tra kết quả."}
            elif "NullPointerException" in output:
                issue_type = "null_pointer_error"
                diagnosis = "Gặp lỗi NullPointerException khi chạy test."
                execution_issue = {"type": issue_type, "hint": "Kiểm tra kỹ các đối tượng mock hoặc dữ liệu đầu vào bị null."}
            elif "No tests found" in output or "NoTestsFoundException" in output:
                issue_type = "collection_error"
                diagnosis = "Không tìm thấy bất kỳ test case nào để chạy."
                execution_issue = {"type": issue_type, "hint": "Đảm bảo test class là public và có phương thức @Test."}
            elif "Exception" in output:
                issue_type = "runtime_exception"
                diagnosis = "Có lỗi Runtime Exception khi chạy."
                execution_issue = {"type": issue_type, "hint": "Test thất bại do Runtime Exception văng ra. Vui lòng kiểm tra lại test case và sử dụng assertThrows() để bọc các câu lệnh mà bạn cố tình muốn test lỗi ngoại lệ."}
            else:
                execution_issue = {"type": issue_type, "hint": "Kiểm tra log để tìm nguyên nhân thất bại."}

        # Generate a combined report structure equivalent to pytest
        combined_report = {
            "passed": passed,
            "coverage_percent": coverage_percent,
            "missing_lines": missing_lines,
            "coverage_path": coverage_path,
            "test_paths": [test_path],
            "output": output.strip(),
            "pytest_log_path": "", # using the same key name for UI compatibility
            "collection_log_path": "",
        }

        summary = self._summary(
            passed=passed,
            command=command,
            output=output,
            diagnosis=diagnosis,
            issue_type=issue_type,
            title="JUnit execution passed" if passed else "JUnit execution failed",
            hint="Review Maven/Gradle output and test XML reports." if not passed else "No action required.",
            coverage_percent=coverage_percent,
            extra={
                "test_path": test_path,
                "source_path": source_path,
                "returncode": process.returncode if process else 1,
                "missing_lines": missing_lines,
                "missing_lines_count": str(len(missing_lines)),
                "coverage_path": coverage_path,
                "execution_issue": execution_issue,
                "combined_report": combined_report,
                "combined_coverage_percent": coverage_percent,
                "combined_missing_lines": missing_lines,
                "junit_coverage_gaps": coverage_gaps,
                **xml_summary,
            },
        )
        return TestExecutionOutcome(framework=self.framework, summary=summary)

    def score_result(
        self,
        summary: dict[str, Any],
        coverage_threshold: float,
    ) -> tuple[int, float, float]:
        """Chấm điểm kết quả chạy test tương tự thuật toán của Pytest."""
        passed = bool(summary.get("passed", False))
        coverage_percent = float(summary.get("coverage_percent", 0.0))
        issue = summary.get("execution_issue", {})
        issue_type = issue.get("type", "") if isinstance(issue, dict) else ""
        
        pass_score = 1 if passed else 0
        fail_score = 1.0 if not passed else 0.0
        
        # Penalize certain critical errors
        if issue_type == "source_compilation_error":
            fail_score = 5.0
        elif issue_type == "test_compilation_error":
            fail_score = 4.0
        elif issue_type in ("collection_error", "NoTestsFoundException", "NoClassDefFoundError"):
            fail_score = 3.0
            
        return (pass_score, coverage_percent, -fail_score)

    def _command_for_workspace(self, workspace_dir: Path) -> list[str] | None:
        if (workspace_dir / "pom.xml").exists():
            return ["mvn", "test"]

        gradlew_bat = workspace_dir / "gradlew.bat"
        gradlew = workspace_dir / "gradlew"
        if gradlew_bat.exists():
            return [str(gradlew_bat), "test"]
        if gradlew.exists():
            return [str(gradlew), "test"]

        if (workspace_dir / "build.gradle").exists() or (workspace_dir / "build.gradle.kts").exists():
            return ["gradle", "test"]
        return None

    def _parse_xml_reports(self, workspace_dir: Path) -> dict[str, Any]:
        report_paths = [
            *workspace_dir.glob("target/surefire-reports/TEST-*.xml"),
            *workspace_dir.glob("build/test-results/test/TEST-*.xml"),
        ]
        totals = {
            "tests_total": 0,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "xml_report_paths": [str(path) for path in report_paths],
        }
        for report_path in report_paths:
            try:
                root = ET.parse(report_path).getroot()
            except (OSError, ET.ParseError):
                continue
            suites = list(root.findall(".//testsuite")) if root.tag != "testsuite" else [root]
            if not suites:
                suites = [root]
            for suite in suites:
                totals["tests_total"] += self._int_attr(suite, "tests")
                totals["failures"] += self._int_attr(suite, "failures")
                totals["errors"] += self._int_attr(suite, "errors")
                totals["skipped"] += self._int_attr(suite, "skipped")
        return totals

    def _read_jacoco_coverage(self, workspace_dir: Path) -> tuple[float, list[int], str, dict[str, list[dict]]]:
        jacoco_path = workspace_dir / "target" / "site" / "jacoco" / "jacoco.xml"
        if not jacoco_path.exists():
            return 0.0, [], "", {}
        
        missing_lines: list[int] = []
        coverage_gaps: dict[str, list[dict]] = {"missed_methods": [], "partial_methods": []}
        try:
            root = ET.parse(jacoco_path).getroot()
        except (OSError, ET.ParseError):
            return 0.0, [], str(jacoco_path), {}
            
        covered = 0
        missed = 0
        
        for package in root.findall("package"):
            for cls in package.findall("class"):
                if "GeneratedTest" in cls.attrib.get("name", ""):
                    continue
                
                source_file_node = package.find(f"sourcefile[@name='{cls.attrib.get('sourcefilename', '')}']")
                line_info = {}
                if source_file_node is not None:
                    for line_node in source_file_node.findall("line"):
                        try:
                            line_nr = int(line_node.attrib.get("nr", 0))
                            ci = int(line_node.attrib.get("ci", 0))
                            line_info[line_nr] = ci
                            if ci == 0:
                                missing_lines.append(line_nr)
                        except ValueError:
                            continue
                
                # Check method coverage
                for method in cls.findall("method"):
                    m_name = method.attrib.get("name", "")
                    m_line = int(method.attrib.get("line", 0)) if method.attrib.get("line") else 0
                    
                    m_covered = 0
                    m_missed = 0
                    for counter in method.findall("counter[@type='INSTRUCTION']"):
                        m_covered += int(counter.attrib.get("covered", 0))
                        m_missed += int(counter.attrib.get("missed", 0))
                        
                    m_branches_missed = 0
                    for counter in method.findall("counter[@type='BRANCH']"):
                        m_branches_missed += int(counter.attrib.get("missed", 0))
                        
                    # Calculate method's missed lines by checking the lines around m_line
                    m_missed_lines = []
                    # Just an approximation: check lines from m_line up to next method's line
                    if m_missed > 0 or m_branches_missed > 0:
                        # Find lines with ci == 0 that are >= m_line
                        for lnr, ci in line_info.items():
                            if lnr >= m_line and ci == 0:
                                # We can't strictly bound it without knowing next method line, but it's a hint
                                m_missed_lines.append(lnr)
                        
                        if m_covered == 0:
                            coverage_gaps["missed_methods"].append({
                                "name": m_name,
                                "line": m_line,
                                "missed_lines": sorted(list(set(m_missed_lines)))[:15] # limit size
                            })
                        elif m_missed > 0 or m_branches_missed > 0:
                            coverage_gaps["partial_methods"].append({
                                "name": m_name,
                                "missed_lines": sorted(list(set(m_missed_lines)))[:15],
                                "missed_branches": m_branches_missed
                            })
                
                for counter in cls.findall("counter[@type='INSTRUCTION']"):
                    try:
                        covered += int(counter.attrib.get("covered", 0))
                        missed += int(counter.attrib.get("missed", 0))
                    except ValueError:
                        continue
                        
        total = covered + missed
        percent = (covered / total * 100.0) if total > 0 else 0.0
        
        missing_lines = sorted(list(set(missing_lines)))
        return percent, missing_lines, str(jacoco_path), coverage_gaps

    def _generate_default_pom(self, workspace_dir: Path) -> None:
        pom_content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.testgen</groupId>
    <artifactId>generated-tests</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <junit.jupiter.version>5.10.0</junit.jupiter.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>${junit.jupiter.version}</version>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>${junit.jupiter.version}</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.1.2</version>
            </plugin>
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>0.8.10</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>prepare-agent</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>report</id>
                        <phase>test</phase>
                        <goals>
                            <goal>report</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
"""
        self._write_text(workspace_dir / "pom.xml", pom_content)

    def _int_attr(self, node: ET.Element, key: str) -> int:
        try:
            return int(node.attrib.get(key, 0))
        except (TypeError, ValueError):
            return 0
