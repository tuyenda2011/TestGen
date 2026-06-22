from __future__ import annotations

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from testgen.executors.junit_executor import JUnitExecutor
from testgen.executors.base import TestExecutionRequest


@pytest.fixture
def junit_executor():
    return JUnitExecutor()


def test_extract_public_class_name(junit_executor):
    code = "public class MyTestClass { }"
    assert junit_executor._extract_public_class_name(code, "Default") == "MyTestClass"

    assert junit_executor._extract_public_class_name("", "Default") == "Default"
    assert junit_executor._extract_public_class_name("class NoPublic {}", "Default") == "Default"


def test_extract_package_path(junit_executor):
    assert junit_executor._extract_package_path("package com.example.test;") == "com/example/test"
    assert junit_executor._extract_package_path("") == ""
    assert junit_executor._extract_package_path("public class NoPackage {}") == ""


def test_command_for_workspace(junit_executor, tmp_path):
    assert junit_executor._command_for_workspace(tmp_path) is None

    (tmp_path / "pom.xml").touch()
    assert junit_executor._command_for_workspace(tmp_path) == ["mvn", "test"]

    (tmp_path / "pom.xml").unlink()
    (tmp_path / "gradlew.bat").touch()
    assert junit_executor._command_for_workspace(tmp_path) == [str(tmp_path / "gradlew.bat"), "test"]

    (tmp_path / "gradlew.bat").unlink()
    (tmp_path / "gradlew").touch()
    assert junit_executor._command_for_workspace(tmp_path) == [str(tmp_path / "gradlew"), "test"]

    (tmp_path / "gradlew").unlink()
    (tmp_path / "build.gradle").touch()
    assert junit_executor._command_for_workspace(tmp_path) == ["gradle", "test"]


def test_int_attr(junit_executor):
    import xml.etree.ElementTree as ET
    el = ET.Element("test", {"val": "10", "bad": "not_int"})
    assert junit_executor._int_attr(el, "val") == 10
    assert junit_executor._int_attr(el, "bad") == 0
    assert junit_executor._int_attr(el, "missing") == 0


def test_parse_xml_reports_empty(junit_executor, tmp_path):
    res = junit_executor._parse_xml_reports(tmp_path)
    assert res["tests_total"] == 0
    assert res["failures"] == 0


def test_parse_xml_reports_valid(junit_executor, tmp_path):
    target = tmp_path / "target" / "surefire-reports"
    target.mkdir(parents=True)
    xml_file = target / "TEST-1.xml"
    xml_file.write_text("""<?xml version="1.0"?>
    <testsuites>
        <testsuite tests="5" failures="1" errors="2" skipped="1"></testsuite>
    </testsuites>
    """)
    res = junit_executor._parse_xml_reports(tmp_path)
    assert res["tests_total"] == 5
    assert res["failures"] == 1
    assert res["errors"] == 2
    assert res["skipped"] == 1


def test_read_jacoco_coverage_empty(junit_executor, tmp_path):
    pct, missing, pth = junit_executor._read_jacoco_coverage(tmp_path)
    assert pct == 0.0
    assert missing == []


def test_read_jacoco_coverage_valid(junit_executor, tmp_path):
    jacoco_dir = tmp_path / "target" / "site" / "jacoco"
    jacoco_dir.mkdir(parents=True)
    xml_file = jacoco_dir / "jacoco.xml"
    xml_file.write_text("""<?xml version="1.0"?>
    <report name="test">
        <package name="com/example">
            <class name="com/example/MyClass" sourcefilename="MyClass.java">
                <counter type="INSTRUCTION" missed="2" covered="8"/>
            </class>
            <sourcefile name="MyClass.java">
                <line nr="10" ci="0"/>
                <line nr="11" ci="1"/>
            </sourcefile>
        </package>
    </report>
    """)
    pct, missing, pth = junit_executor._read_jacoco_coverage(tmp_path)
    assert pct == 80.0
    assert missing == [10]


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_success(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=0, stdout="Success", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={"tests_total": 1, "failures": 0, "errors": 0}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(100.0, [], "path")):
         
        req = TestExecutionRequest(
            workspace_dir=tmp_path,
            generated_test_code="package com.test;\npublic class MyTest {}",
            source_code_text="package com.test;\npublic class Source {}"
        )
        
        outcome = junit_executor.execute(req)
        assert outcome.summary["passed"] is True
        assert outcome.summary["coverage_percent"] == 100.0


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_compilation_error(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=1, stdout="[ERROR] COMPILATION ERROR \n[ERROR] /src/main/java/Source.java: syntax error", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(0.0, [], "")):
         
        req = TestExecutionRequest(
            workspace_dir=tmp_path,
            generated_test_code="public class MyTest {}",
            source_code_text="public class Source {}"
        )
        
        outcome = junit_executor.execute(req)
        assert outcome.summary["passed"] is False
        assert outcome.summary["execution_issue"]["type"] == "source_compilation_error"


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_test_compilation_error(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=1, stdout="[ERROR] COMPILATION ERROR \n[ERROR] /src/test/java/Test.java: syntax error", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(0.0, [], "")):
         
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="public class MyTest {}", source_code_text="public class Source {}")
        
        outcome = junit_executor.execute(req)
        assert outcome.summary["passed"] is False
        assert outcome.summary["execution_issue"]["type"] == "test_compilation_error"


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_assertion_error(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=1, stdout="AssertionFailedError: expected 1 but got 2", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(0.0, [], "")):
         
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="public class MyTest {}", source_code_text="public class Source {}")
        outcome = junit_executor.execute(req)
        assert outcome.summary["execution_issue"]["type"] == "assertion_error"


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_null_pointer(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=1, stdout="NullPointerException at line 10", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(0.0, [], "")):
         
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="public class MyTest {}", source_code_text="public class Source {}")
        outcome = junit_executor.execute(req)
        assert outcome.summary["execution_issue"]["type"] == "null_pointer_error"


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_no_tests_found(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=1, stdout="NoTestsFoundException", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(0.0, [], "")):
         
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="public class MyTest {}", source_code_text="public class Source {}")
        outcome = junit_executor.execute(req)
        assert outcome.summary["execution_issue"]["type"] == "collection_error"


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_runtime_exception(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (MagicMock(returncode=1, stdout="RuntimeException: error", stderr=""), None)
    
    with patch.object(junit_executor, "_parse_xml_reports", return_value={}), \
         patch.object(junit_executor, "_read_jacoco_coverage", return_value=(0.0, [], "")):
         
        req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="public class MyTest {}", source_code_text="public class Source {}")
        outcome = junit_executor.execute(req)
        assert outcome.summary["execution_issue"]["type"] == "runtime_exception"


@patch("testgen.executors.junit_executor.JUnitExecutor._run_command")
def test_execute_early_summary(mock_run, junit_executor, tmp_path):
    mock_run.return_value = (None, {"passed": False, "early": True})
    req = TestExecutionRequest(workspace_dir=tmp_path, generated_test_code="public class MyTest {}", source_code_text="public class Source {}")
    outcome = junit_executor.execute(req)
    assert outcome.summary["early"] is True


def test_score_result(junit_executor):
    assert junit_executor.score_result({"passed": True, "coverage_percent": 100}, 80) == (1, 100.0, -0.0)
    assert junit_executor.score_result({"passed": False, "coverage_percent": 50, "execution_issue": {"type": "source_compilation_error"}}, 80) == (0, 50.0, -5.0)
    assert junit_executor.score_result({"passed": False, "coverage_percent": 50, "execution_issue": {"type": "test_compilation_error"}}, 80) == (0, 50.0, -4.0)
    assert junit_executor.score_result({"passed": False, "coverage_percent": 50, "execution_issue": {"type": "collection_error"}}, 80) == (0, 50.0, -3.0)
