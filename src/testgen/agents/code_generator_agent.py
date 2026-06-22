from __future__ import annotations

from testgen.core.logger import get_logger
logger = get_logger(__name__)

from functools import lru_cache
import re
import json

from testgen.core.utils import extract_json_payload

from testgen.core.config import (
    GEMINI_CODE_GENERATOR_MODEL,
    OLLAMA_CODE_GENERATOR_MODEL,
    PROMPTS_PATH,
    PYTEST_FUNCTION_BATCH_SIZE,
    GENERATOR_MAX_WORKERS,
)
from testgen.core.llm import call_llm_chat
from testgen.prompts.function_prompt_builder import (
    FunctionInfo as _FunctionInfo,
    FunctionPromptBuilder,
    batched_function_infos as _batched,
    build_function_batch_prompt as _build_function_batch_prompt,
    build_function_level_prompt as _build_function_level_prompt,
    extract_python_functions as _extract_python_functions,
    function_prompt_block as _function_prompt_block,
    module_context_symbols as _module_context_symbols,
    safe_unparse as _safe_unparse,
)
from testgen.prompts.templates import CODE_GENERATOR_PROMPT

import concurrent.futures


_FALLBACK_PROMPT = """You are a senior test automation engineer.
Task: Generate executable test code for the {framework} framework.
{framework_notes}
Test Technique: {test_technique}.

Mandatory Rules:
- Only use APIs, classes, functions, parameters, selectors, routes, or schemas provided in the context.
- The source code is the ultimate source of truth. If the test plan contradicts the source, follow the source.
- Do not invent behaviors, expected values, exception types, exception messages, selectors, routes, or schemas.
- If there is not enough information to write a test case, skip it instead of inventing data or creating placeholders.
- Prefer fewer but runnable tests with strong assertions over many weak tests.
- For pytest, output must be Python code that can be run immediately by pytest WITHOUT any additional flags.
- For pytest, always import the target from source_under_test as instructed in the user prompt.
- For pytest, ABSOLUTELY DO NOT use snapshot() or import inline_snapshot. Every assert MUST have a concrete value derived from the source.
- For pytest, if the source raises an exception, use pytest.raises with the correct type/message if the message is in the source.
- For pytest, DO NOT use pytest.raises if the source DOES NOT contain a raise statement.
- For pytest, all test function names must start with the mandatory prefix if the user prompt provides one.
- For pytest, each test must have a clear assertion or a clear pytest.raises.
- For pytest, do not use TODO, pass, print-only tests, arbitrary sleep, or always-true assertions.
- For pytest, only mock external dependencies when the actual source calls that dependency and mocking is the only way to stabilize the test.
- For pytest, do not rely on fixtures, helpers, or conftest that do not appear in the provided source/context. Do not invent fixtures like client, app, db_session, mock_user.
- Do not use markdown fences, do not explain, do not add text outside the code.

Reasoning process before writing code:
1. Identify the target to test and how to import it.
2. Read branches, returns, and raises in the source.
3. Select minimal test data to cover success, boundary, and failure paths.
4. Write expected values by deriving them directly from the source.
5. Avoid duplicate test names across targets.

Output only clean test code.
"""

_FRAMEWORK_NOTES = {
    "pytest": "Write pytest test functions in Python. Every assert MUST have a concrete value derived from the source code logic. ABSOLUTELY DO NOT use snapshot(), inline_snapshot, or any placeholders as expected values.",
    "JUnit": "Write JUnit 5 tests in Java with assertEquals or assertTrue. IMPORTANT: Strictly adhere to the existing constructors and method signatures in the Source Code (correct data types, number of parameters). Absolutely do not use empty constructors if the class does not support it. DO NOT call private/protected methods. MUST use the assertThrows(ExceptionType.class, () -> {...}) syntax to wrap functions that intentionally throw exceptions. CRITICAL RULES: 1. DO NOT hard-code exact exception messages (e.g. do not use assertEquals(\"message\", exception.getMessage())). If you need to check message, use assertTrue(exception.getMessage().contains(\"...\")). 2. MUST use @BeforeEach to initialize shared mock data and objects to avoid duplication. 3. MUST perform State Verification (assert properties using getter) after calling functions that change state. DO NOT USE @TempDir, java.io, java.nio, java.net, Files.* or framework features that do not directly call the source.",
    "Jest": "Write Jest tests in JavaScript with expect statements. IMPORTANT: The first line MUST be `const target = require('./source_under_test');` or equivalent destructuring. ABSOLUTELY DO NOT import from any other virtual path. Use jest.mock() if you need to mock dependencies. ABSOLUTELY DO NOT redefine/mock internal helper functions of the same module. CRITICAL: 1. Absolutely DO NOT generate unused helper functions (e.g. computeDiscount). 2. Keep comments concise. DO NOT write manual math calculations in comments. 3. Because JavaScript lacks static typing, you MUST explicitly implement test cases for `null`, `undefined`, and missing object properties.",
    "Selenium": "Write Selenium tests in Python using webdriver.Edge() ONLY (do NOT use Chrome). Prefer headless EdgeOptions if possible to speed up execution. Only use explicitly provided selectors or locators. CRITICAL RULES: 1. You MUST implement ALL planned test cases. Skipping ANY test case is strictly forbidden. You MUST include the exact case ID (e.g., 'TC-001') in the test function name, docstring, or parametrized arguments so it can be tracked by Traceability. 2. When interacting with `<select>` dropdowns, you MUST inspect the HTML source and use ONLY the exact values present in the `<option value=\"...\">` tags. Absolutely DO NOT invent arbitrary string values. 3. Derive expected values by strictly following the JS math logic in the HTML. 4. DO NOT manually calculate expected results in your head and hardcode them in `@pytest.mark.parametrize`! You MUST translate the JS math logic into Python helper functions, call them AT RUNTIME inside the test function to compute expected values dynamically. IMPORTANT: After computing the expected value dynamically, you MUST use Selenium WebDriver to interact with the UI, click the calculate button, extract the actual output from the UI, and assert that the UI output matches your dynamically computed expected value. ABSOLUTELY DO NOT just assert your Python helper function's output against the expected string! 5. ABSOLUTELY DO NOT call `.clear()`, `.send_keys()`, or other interaction methods on read-only elements like `<output>`, `<div>`, or `<span>`. This will cause an `InvalidElementStateException`. 6. ABSOLUTELY DO NOT use `eval()`, `exec()`, `os`, `subprocess`, `open()`, or any restricted Python built-ins. All mathematical calculations must be done using standard Python math operators (+, -, *, /, max, min) ONLY. 7. Be aware of HTML5 `<input type=\"number\">` behavior: if non-numeric text is sent via `.send_keys()`, the browser rejects it and its `.value` property becomes an empty string `\"\"` (which JavaScript `Number(\"\")` evaluates to `0`), NOT `NaN`. Therefore, when calculating expected values for non-numeric inputs on number fields, you MUST treat them as `0`. 8. For negative/boundary test cases that trigger JavaScript `throw new Error(...)` in the provided HTML, you MUST NOT use Selenium `.click()` or `fill_form` to test them, because Selenium DOES NOT catch internal browser JS exceptions. Instead, you MUST use `pytest.raises(JavascriptException)` AND directly call the JS function using `driver.execute_script('return functionName(...)')`. DO NOT assert on the UI `#error` element. 9. DOUBLE CHECK YOUR SYNTAX! Do not write invalid Python like `assert elem.text == \"\")` with a dangling parenthesis! 10. ABSOLUTELY DO NOT call `.clear()` on `<select>` dropdown elements, as it will crash with `InvalidElementStateException`. Use `.send_keys()` or Selenium's `Select` class instead. 11. MUST use `pathlib.Path` to construct the local HTML file URI. The target file is ALWAYS exactly named 'source_under_test.html'. Example: `from pathlib import Path; html_path = Path(__file__).with_name('source_under_test.html').as_uri()`. DO NOT hallucinate the file name. ABSOLUTELY DO NOT use `webdriver.common.utils.Path`.",
    "Playwright": "Write Playwright tests in Python. CRITICAL: You MUST use MS Edge (channel='msedge') instead of default Chromium. Prefer headless mode. Only use explicitly provided selectors or locators. CRITICAL RULES: 1. You MUST implement ALL planned test cases. Skipping ANY test case is strictly forbidden. You MUST include the exact case ID (e.g., 'TC-001') in the test function name, docstring, or parametrized arguments so it can be tracked. 2. When interacting with `<select>`, use ONLY exact values present in `<option value=\"...\">`. 3. Derive expected values by strictly following the JS math logic. 4. DO NOT manually calculate expected results in your head and hardcode them in `@pytest.mark.parametrize`! MUST translate JS logic into Python helper functions and call them AT RUNTIME. IMPORTANT: After computing the expected value dynamically, you MUST use the Playwright `page` object to interact with the UI, click the calculate button, extract the actual output from the UI, and assert that the UI output matches your dynamically computed expected value. ABSOLUTELY DO NOT just assert your Python helper function's output! 5. ABSOLUTELY DO NOT use `eval()`, `exec()`, `os`, `subprocess`, `open()`, or restricted built-ins. 6. HTML5 `<input type=\"number\">` behavior: non-numeric text becomes `\"\"` (JavaScript `Number(\"\")` is `0`), NOT `NaN`. Therefore, when calculating expected values for non-numeric inputs on number fields, you MUST treat them as `0`. 7. For JS `throw new Error(...)`, you MUST NOT use `page.click()` to test them because Playwright does not catch internal page JS exceptions. Instead, use `pytest.raises(Error)` AND directly call the JS function via `page.evaluate('() => functionName(...)')`. DO NOT assert on UI error output. 8. DOUBLE CHECK YOUR SYNTAX! Avoid dangling parentheses! 9. ABSOLUTELY DO NOT call `.clear()` on `<select>` dropdown elements. 10. MUST use `pathlib.Path` to construct the local HTML file URI. The target file is ALWAYS exactly named 'source_under_test.html'. Example: `from pathlib import Path; html_path = Path(__file__).with_name('source_under_test.html').as_uri()`. DO NOT hallucinate the file name.",
    "Postman script": "Write Postman test scripts in JavaScript using pm.test commands. IMPORTANT: 1. You MUST generate a valid Postman Collection JSON format (v2.1.0). 2. For EACH test scenario, create an item with the correct `request` (method, url, headers, body) and `event` (test scripts). 3. Your `pm.test` assertions MUST validate the actual API response using `pm.response.json()` or `pm.response.text()`, DO NOT create hardcoded variables to assert against. 4. Include assertions for HTTP status code, response schema, and specific body values. 5. If testing a POST/PUT request, ensure the `body` is properly formatted in the request. 6. DO NOT write dummy tests that don't check the real response. 7. CRITICAL: You MUST output EXACTLY ONE JSON block containing the entire Postman Collection. DO NOT output multiple JSON blocks, environment variables, or any extra conversational text. 8. CRITICAL: If the target API is a dummy API (e.g. JSONPlaceholder), POST/PUT/DELETE requests DO NOT actually mutate server state. They will ALWAYS return a mocked structure (like ID 101). DO NOT write assertions that expect state changes across multiple requests. 9. CRITICAL: Must not generate overly long strings (>50 characters) for test data values, even for boundary tests, to avoid bloating the JSON payload. Use a concise representative string instead. 10. CRITICAL: Your output must be strictly valid JSON. Absolutely DO NOT include JavaScript-style comments (`//` or `/* */`) inside the JSON. Absolutely DO NOT include trailing commas. Ensure all strings are properly escaped.",
}

_FENCED_CODE_BLOCK_PATTERN = re.compile(r"```[^\n]*\n?(.*?)```", re.DOTALL)
_TEST_SECTION_PATTERN = re.compile(r"(?m)^#\s*=+\s*Tests for\s+(.+?)\s*=+\s*$")


def _strip_markdown_code_fences(text: str) -> str:
    cleaned = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if "```" not in cleaned:
        return cleaned

    code_blocks = [
        match.group(1).strip("\n")
        for match in _FENCED_CODE_BLOCK_PATTERN.finditer(cleaned)
        if match.group(1).strip()
    ]
    if code_blocks:
        return "\n\n".join(code_blocks).strip()

    lines = [line for line in cleaned.splitlines() if not line.strip().startswith("```")]
    return "\n".join(lines).strip()


def _ensure_pytest_import(code: str) -> str:
    cleaned = (code or "").strip()
    if not cleaned:
        return cleaned
    if not re.search(r"\bpytest\.", cleaned):
        return cleaned
    if re.search(r"^\s*(import\s+pytest|from\s+pytest\s+import\b)", cleaned, flags=re.MULTILINE):
        return cleaned
    return f"import pytest\n\n{cleaned}"


def _deduplicate_top_level_imports(code: str) -> str:
    lines = (code or "").splitlines()
    seen: set[str] = set()
    deduplicated: list[str] = []
    for line in lines:
        stripped = line.strip()
        if line == stripped and (stripped.startswith("import ") or stripped.startswith("from ")):
            if stripped in seen:
                continue
            seen.add(stripped)
        deduplicated.append(line)
    return "\n".join(deduplicated).strip()


def _ensure_required_import(code: str, import_statement: str) -> str:
    cleaned = (code or "").strip()
    required = (import_statement or "").strip()
    if not cleaned or not required or required in cleaned:
        return cleaned
    return f"{required}\n\n{cleaned}"


def _target_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return slug or "target"


def _prefix_pytest_test_names(code: str, test_name_prefix: str) -> str:
    prefix = _target_slug(test_name_prefix)
    required_prefix = f"test_{prefix}_"
    pattern = re.compile(r"^([ \t]*)(async\s+def|def)\s+(test_[A-Za-z0-9_]+)\s*\(", re.MULTILINE)

    def replace(match: re.Match[str]) -> str:
        indent = match.group(1)
        def_keyword = match.group(2)
        name = match.group(3)
        if name.startswith(required_prefix):
            return match.group(0)
        suffix = name.removeprefix("test_").strip("_") or "case"
        return f"{indent}{def_keyword} {required_prefix}{suffix}("

    return pattern.sub(replace, code or "")


def _namespace_pytest_test_names(code: str, namespace: str) -> str:
    cleaned_namespace = _target_slug(namespace)
    if not cleaned_namespace:
        return code or ""
    required_prefix = f"test_{cleaned_namespace}_"
    pattern = re.compile(r"^([ \t]*)(async\s+def|def)\s+(test_[A-Za-z0-9_]+)\s*\(", re.MULTILINE)

    def replace(match: re.Match[str]) -> str:
        indent = match.group(1)
        def_keyword = match.group(2)
        name = match.group(3)
        if name.startswith(required_prefix):
            return match.group(0)
        suffix = name.removeprefix("test_").strip("_") or "case"
        return f"{indent}{def_keyword} {required_prefix}{suffix}("

    return pattern.sub(replace, code or "")


def _ensure_snapshot_import(code: str) -> str:
    """Nếu code dùng snapshot() mà chưa import, inject import để lỗi rõ ràng hơn khi chạy.
    inline_snapshot không có trong dependencies nên sẽ gây ModuleNotFoundError → trigger heal."""
    cleaned = (code or "").strip()
    if not cleaned:
        return cleaned
    # Kiểm tra có gọi snapshot() không
    if not re.search(r"\bsnapshot\s*\(", cleaned):
        return cleaned
    # Nếu đã có import inline_snapshot rồi thì không cần inject
    if re.search(r"^\s*(from\s+inline_snapshot\s+import|import\s+inline_snapshot)", cleaned, flags=re.MULTILINE):
        return cleaned
    # Inject import để lỗi thành ModuleNotFoundError (import_error) thay vì NameError (collection_error)
    # Cả 2 đều trigger heal, nhưng import_error có message rõ ràng hơn
    logger.warning(
        "Generated pytest code contains snapshot() but inline_snapshot is not installed. "
        "Injecting import to trigger import_error → heal_pytest_code will replace snapshot() with concrete values."
    )
    return "from inline_snapshot import snapshot\n\n" + cleaned


def _remove_snapshot_calls(code: str) -> str:
    """Nếu code dùng snapshot() mà chưa import và không thể resolve, thay bằng None placeholder an toàn.
    Chỉ dùng như last resort fallback sau khi đã cố inject import."""
    # Không xử lý nếu code đã có import inline_snapshot
    if re.search(r"from inline_snapshot import", code or ""):
        return code
    return (code or "")


def _sanitize_generated_test_code(code: str, framework: str) -> str:
    cleaned = _strip_markdown_code_fences(code)
    if framework == "pytest":
        cleaned = _ensure_pytest_import(cleaned)
        cleaned = _ensure_snapshot_import(cleaned)
    return _deduplicate_top_level_imports(cleaned)




def _model_for_backend(backend: str, model: str | None = None) -> str | None:
    if model:
        return model
    if backend == "gemini":
        return GEMINI_CODE_GENERATOR_MODEL
    if backend == "ollama":
        return OLLAMA_CODE_GENERATOR_MODEL
    return None


def _split_marked_test_sections(code: str) -> dict[str, str]:
    matches = list(_TEST_SECTION_PATTERN.finditer(code or ""))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(code)
        section = code[start:end].strip()
        if name and section:
            sections[name] = section
    return sections


def _sanitize_batch_pytest_code(code: str, function_infos: list[_FunctionInfo]) -> str:
    cleaned = _strip_markdown_code_fences(code)
    sections = _split_marked_test_sections(cleaned)
    sanitized_sections: list[str] = []

    if sections:
        for function_info in function_infos:
            section = sections.get(function_info.qualified_name) or sections.get(function_info.name)
            if not section:
                continue
            section = _prefix_pytest_test_names(section, function_info.test_name_prefix)
            section = _ensure_required_import(section, function_info.import_statement)
            sanitized_sections.append(section)
        if sanitized_sections:
            return "\n\n".join(sanitized_sections)

    if len(function_infos) == 1:
        cleaned = _prefix_pytest_test_names(cleaned, function_infos[0].test_name_prefix)

    for function_info in function_infos:
        cleaned = _ensure_required_import(cleaned, function_info.import_statement)
    label = ", ".join(function_info.qualified_name for function_info in function_infos)
    return f"# ===== Tests for {label} =====\n{cleaned}".strip()



def _generate_function_level_pytest(
    *,
    requirement_json: str,
    test_plan_json: str,
    test_technique: str,
    source_code_text: str,
    backend: str,
    api_key: str | None,
    model: str | None,
    system_prompt: str,
) -> str:
    functions = FunctionPromptBuilder.extract_python_functions(source_code_text)
    if not functions:
        return ""

    resolved_model = _model_for_backend(backend, model)
    generated_parts: list[str] = []
    
    def process_batch(function_batch):
        prompt = FunctionPromptBuilder.build_function_batch_prompt(
            requirement_json=requirement_json,
            test_plan_json=test_plan_json,
            function_infos=function_batch,
            test_technique=test_technique,
        )
        code = call_llm_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            backend=backend,
            model=resolved_model,
            api_key=api_key,
            agent_type="code_generator",
        ).strip()
        code = _sanitize_batch_pytest_code(code, function_batch)
        return code

    batches = list(FunctionPromptBuilder.batched(functions, PYTEST_FUNCTION_BATCH_SIZE))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=GENERATOR_MAX_WORKERS) as executor:
        results = list(executor.map(process_batch, batches))
        
    for code in results:
        if code:
            generated_parts.append(code)

    return _sanitize_generated_test_code("\n\n".join(generated_parts), "pytest")


def generate_targeted_pytest_code(
    requirement_json: str,
    test_plan_json: str,
    test_technique: str,
    source_code_text: str,
    missing_lines: list,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
    retry_namespace: str = "retry",
) -> str:
    functions = FunctionPromptBuilder.select_functions_for_lines(source_code_text, missing_lines)
    if not functions:
        return ""

    system_template = CODE_GENERATOR_PROMPT
    system_prompt = system_template.format(
        framework="pytest",
        test_technique=test_technique,
        framework_notes=_FRAMEWORK_NOTES["pytest"],
    )
    system_prompt += (
        "\n\n[MANDATORY RULES FOR PYTEST - EXPECTED VALUE CALCULATION]:\n"
        "1. READ the source code carefully and CALCULATE the expected value directly from the source's logic.\n"
        "   Example: if the source returns 'A' when score >= 90, write `assert letter_grade(95) == 'A'`\n"
        "2. ABSOLUTELY DO NOT use snapshot(). Do not import inline_snapshot. No placeholders.\n"
        "3. If the source raises an exception, use pytest.raises with the correct ExceptionType and matching message.\n"
        "4. If the source DOES NOT raise an exception, ABSOLUTELY DO NOT use pytest.raises.\n\n"
    )
    resolved_model = _model_for_backend(backend, model)
    missing_text = ", ".join(str(item) for item in missing_lines or [])
    generated_parts: list[str] = []

    def process_batch(function_batch):
        prompt = FunctionPromptBuilder.build_function_batch_prompt(
            requirement_json=(
                (requirement_json or "").strip()
                + "\n\nTargeted retry goal: only add tests for targets containing "
                + f"missing_lines=[{missing_text}]. Do not rewrite the entire test file."
            ),
            test_plan_json=test_plan_json,
            function_infos=function_batch,
            test_technique=test_technique,
        )
        code = call_llm_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            backend=backend,
            model=resolved_model,
            api_key=api_key,
            agent_type="code_generator",
        ).strip()
        code = _sanitize_batch_pytest_code(code, function_batch)
        code = _namespace_pytest_test_names(code, retry_namespace)
        return code

    batches = list(FunctionPromptBuilder.batched(functions, PYTEST_FUNCTION_BATCH_SIZE))
    with concurrent.futures.ThreadPoolExecutor(max_workers=GENERATOR_MAX_WORKERS) as executor:
        results = list(executor.map(process_batch, batches))

    for code in results:
        if code:
            generated_parts.append(code)

    return _sanitize_generated_test_code("\n\n".join(generated_parts), "pytest")


def generate_targeted_junit_code(
    requirement_json: str,
    test_plan_json: str,
    test_technique: str,
    source_code_text: str,
    base_generated_code: str,
    missing_lines: list,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
    retry_namespace: str = "retry",
    coverage_gaps: dict | None = None,
) -> str:
    missing_text = ", ".join(str(item) for item in missing_lines or [])
    system_template = CODE_GENERATOR_PROMPT
    system_prompt = system_template.format(
        framework="JUnit",
        test_technique=test_technique,
        framework_notes=_FRAMEWORK_NOTES.get("JUnit", ""),
    )

    # Build method-level coverage hint from JaCoCo coverage_gaps if available
    method_hint = ""
    gaps = coverage_gaps or {}
    missed_methods = gaps.get("missed_methods", [])
    partial_methods = gaps.get("partial_methods", [])
    if missed_methods or partial_methods:
        lines_hint = []
        for m in missed_methods:
            name = m.get("name", "")
            line = m.get("line", 0)
            m_lines = m.get("missed_lines", [])
            lines_hint.append(f"  - {name}() (line {line}): fully uncovered, missing lines {m_lines}")
        for m in partial_methods:
            name = m.get("name", "")
            m_lines = m.get("missed_lines", [])
            br = m.get("missed_branches", 0)
            lines_hint.append(f"  - {name}() (partial): missing lines {m_lines}, missed branches={br}")
        method_hint = (
            "\n\nJaCoCo method-level coverage gaps (prioritize writing tests for these methods):\n"
            + "\n".join(lines_hint)
        )

    prompt = (
        "Objective: Add NEW @Test methods to the existing JUnit 5 test class to increase JaCoCo coverage.\n"
        f"Test technique: {test_technique}\n\n"
        f"Uncovered source lines: [{missing_text}]{method_hint}\n\n"
        "Source Code:\n"
        f"```java\n{source_code_text}\n```\n\n"
        "Current Test Code (DO NOT modify existing tests, only return new @Test methods):\n"
        f"```java\n{base_generated_code}\n```\n\n"
        "Requirements:\n"
        "1. ONLY return NEW @Test methods. DO NOT return the full class.\n"
        "2. Write new @Test methods that exercise the uncovered methods/branches listed above.\n"
        f"3. Name new test methods with prefix `{retry_namespace}_` for easy identification.\n"
        "4. DO NOT reuse existing test method names.\n"
        "5. DO NOT write import statements or class declarations — only write @Test methods.\n"
        "6. DO NOT use @TempDir, java.io, java.nio, java.net, Files.* or any framework extension features.\n"
        "7. Use assertThrows(ExceptionType.class, () -> {...}) for expected exceptions.\n"
        "8. When comparing doubles/floats, use delta: assertEquals(expected, actual, 0.001).\n"
        "9. Return pure Java code only, no explanation."
    )

    resolved_model = _model_for_backend(backend, model)
    code = call_llm_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        backend=backend,
        model=resolved_model,
        api_key=api_key,
        agent_type="code_generator",
    ).strip()
    return _strip_markdown_code_fences(code)



def heal_junit_code(
    test_code: str,
    error_log: str,
    issue_type: str = "",
    source_code_text: str = "",
    coverage_gaps: dict | None = None,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    """Heal JUnit test code based on the issue type.

    - security_block: Remove all unsafe filesystem/network imports and replace with Public API tests.
    - low_coverage: Append new @Test methods targeting missed methods from JaCoCo coverage_gaps.
    - assertion_error / test_compilation_error / runtime_exception: Fix the specific error inline.
    """
    gaps = coverage_gaps or {}
    missed_methods = gaps.get("missed_methods", [])
    partial_methods = gaps.get("partial_methods", [])

    if issue_type == "security_block":
        system_prompt = (
            "You are a senior Java JUnit 5 test repair engineer.\n"
            "Your task is to sanitize a JUnit test file that was blocked by a security sandbox.\n\n"
            "MANDATORY RULES:\n"
            "1. REMOVE all imports and usage of: java.io.*, java.nio.*, java.net.*, @TempDir, "
            "Files.write, Files.delete, Files.copy, Files.move, Files.readAllBytes, "
            "Files.createTempDirectory, Runtime.getRuntime, ProcessBuilder.\n"
            "2. REMOVE all test methods that only test JUnit framework extensions or filesystem behavior "
            "(e.g., TempDirSharedTest, MigrationTest, @TempDir tests, ParameterizedTest with factory).\n"
            "3. REPLACE removed tests with @Test methods that exercise the PUBLIC API of the source class.\n"
            "4. Every @Test must call a public method/constructor of the source class and assert the result.\n"
            "5. Keep all existing tests that are safe and already test the source public API.\n"
            "6. Return the full corrected Java test file. Do not explain."
        )
        prompt = (
            f"Source class under test:\n```java\n{source_code_text}\n```\n\n"
            f"Current JUnit test file (blocked by sandbox):\n```java\n{test_code}\n```\n\n"
            f"Sandbox block reason:\n{error_log}\n\n"
            "Remove all unsafe imports/tests and replace with safe Public API tests.\n"
            "Return only the full corrected Java test file."
        )
    elif issue_type == "low_coverage":
        missed_method_lines = []
        for m in missed_methods:
            name = m.get("name", "")
            line = m.get("line", 0)
            m_lines = m.get("missed_lines", [])
            missed_method_lines.append(f"  - {name}() (line {line}): missing lines {m_lines}")
        for m in partial_methods:
            name = m.get("name", "")
            m_lines = m.get("missed_lines", [])
            br = m.get("missed_branches", 0)
            missed_method_lines.append(f"  - {name}() (partial): missing lines {m_lines}, missed branches={br}")
        coverage_hint = "\n".join(missed_method_lines) if missed_method_lines else "  (see error log for details)"

        system_prompt = (
            "You are a senior Java JUnit 5 test engineer specializing in coverage improvement.\n"
            "Your task is to APPEND new @Test methods to an existing test class to improve JaCoCo coverage.\n\n"
            "MANDATORY RULES:\n"
            "1. DO NOT remove or modify any existing @Test methods.\n"
            "2. ONLY ADD new @Test methods inside the existing test class.\n"
            "3. Each new test must exercise the uncovered methods/branches listed in the prompt.\n"
            "4. Use assertThrows(ExceptionType.class, () -> {...}) for expected exceptions.\n"
            "5. When comparing doubles/floats, always use delta: assertEquals(expected, actual, 0.001).\n"
            "6. DO NOT use @TempDir, java.io, java.nio, java.net, Files.*, or any filesystem/network API.\n"
            "7. DO NOT create extra test classes or inner classes.\n"
            "8. Return the full Java test file with the new @Test methods appended. Do not explain."
        )
        prompt = (
            f"Source class under test:\n```java\n{source_code_text}\n```\n\n"
            f"Current JUnit test file (passing but coverage too low):\n```java\n{test_code}\n```\n\n"
            f"JaCoCo uncovered methods that need new tests:\n{coverage_hint}\n\n"
            "Append new @Test methods for each uncovered method/branch.\n"
            "Return the full Java test file with the new tests added."
        )
    else:
        # assertion_error, test_compilation_error, runtime_exception, null_pointer_error, etc.
        system_prompt = (
            "You are a senior Java JUnit 5 test repair engineer.\n"
            "Your task is to fix compilation or runtime errors in a JUnit test file.\n\n"
            "REPAIR RULES:\n"
            "1. Fix compilation errors: wrong types, missing imports, wrong method signatures.\n"
            "2. Fix assertion errors: update expected values to match source code behavior.\n"
            "3. Fix NullPointerException: ensure objects are properly initialized.\n"
            "4. For expected exceptions, always use assertThrows(ExceptionType.class, () -> {...}).\n"
            "5. When comparing doubles/floats, use delta: assertEquals(expected, actual, 0.001).\n"
            "6. DO NOT use @TempDir, java.io, java.nio, java.net, Files.*, or filesystem APIs.\n"
            "7. DO NOT remove meaningful @Test methods.\n"
            "8. Return the full corrected Java test file. Do not explain."
        )
        prompt = (
            f"Source class under test:\n```java\n{source_code_text}\n```\n\n"
            f"Current JUnit test file with errors:\n```java\n{test_code}\n```\n\n"
            f"Issue type: {issue_type}\n\n"
            f"Error log:\n{error_log}\n\n"
            "Fix the errors according to the repair rules.\n"
            "Return only the full corrected Java test file."
        )

    resolved_model = _model_for_backend(backend, model)
    code = call_llm_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        backend=backend,
        model=resolved_model,
        api_key=api_key,
        agent_type="code_generator",
    ).strip()
    return _strip_markdown_code_fences(code)


def generate_targeted_jest_code(
    requirement_json: str,
    test_plan_json: str,
    test_technique: str,
    source_code_text: str,
    base_generated_code: str,
    missing_lines: list,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
    retry_namespace: str = "retry",
) -> str:
    missing_text = ", ".join(str(item) for item in missing_lines or [])

    system_template = CODE_GENERATOR_PROMPT
    system_prompt = system_template.format(
        framework="Jest",
        test_technique=test_technique,
        framework_notes=_FRAMEWORK_NOTES.get("Jest", ""),
    )
    system_prompt += (
        "\n\n[SUPREME RULES FOR JEST]:\n"
        "1. MUST import the function/class to be tested from the fixed target file named './source_under_test'.\n"
        "   CORRECT Example: `const target = require('./source_under_test');`\n"
        "2. If the test code uses external libraries, you MUST mock them using `jest.mock('library_name');`.\n"
    )
    
    prompt = (
        "Objective: Generate NEW `test(...)` or `it(...)` blocks for Jest to increase coverage for missing source code lines.\n"
        f"Test technique: {test_technique}\n\n"
        f"Uncovered source code lines: [{missing_text}]\n\n"
        "Source Code:\n"
        f"```javascript\n{source_code_text}\n```\n\n"
        "Current Test Code (Please do not modify existing tests, only return new tests):\n"
        f"```javascript\n{base_generated_code}\n```\n\n"
        "Requirements:\n"
        "1. ONLY RETURN NEW `test(...)` BLOCKS, DO NOT return the entire file.\n"
        "2. Write new tests to exercise the paths or exceptions corresponding to the missing_lines.\n"
        f"3. Names of new tests should have the prefix `[{retry_namespace}] ` for easy identification.\n"
        "4. DO NOT reuse existing test names.\n"
        "5. Return pure Javascript code, no explanation."
    )
    
    resolved_model = _model_for_backend(backend, model)
    code = call_llm_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        backend=backend,
        model=resolved_model,
        api_key=api_key,
        agent_type="code_generator",
    ).strip()
    return _strip_markdown_code_fences(code)


def estimate_test_generation_llm_calls(framework: str, source_code_text: str = "") -> int:
    if framework == "pytest" and (source_code_text or "").strip():
        functions = FunctionPromptBuilder.extract_python_functions(source_code_text)
        if functions:
            batch_size = max(int(PYTEST_FUNCTION_BATCH_SIZE or 1), 1)
            return (len(functions) + batch_size - 1) // batch_size
    return 1


def generate_test_code(
    requirement_json: str,
    test_plan_json: str,
    framework: str,
    test_technique: str = "Hybrid",
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
    source_code_text: str = "",
) -> str:
    system_template = CODE_GENERATOR_PROMPT
    system_prompt = system_template.format(
        framework=framework,
        test_technique=test_technique,
        framework_notes=_FRAMEWORK_NOTES.get(framework, "Please use the selected framework correctly."),
    )

    if framework == "pytest":
        system_prompt += (
            "\n\n[MANDATORY RULES FOR PYTEST - EXPECTED VALUE CALCULATION]:\n"
            "1. READ the source code carefully and CALCULATE the expected value directly from the source logic.\n"
            "   CORRECT Example: `assert letter_grade(95) == 'A'` (derived from source: score >= 90 -> 'A')\n"
            "   INCORRECT Example: `assert letter_grade(95) == snapshot()` (snapshot() is strictly prohibited)\n"
            "2. ABSOLUTELY DO NOT use snapshot(), DO NOT import inline_snapshot, DO NOT use placeholders.\n"
            "3. If the source raises an exception, use pytest.raises with the correct ExceptionType.\n"
            "4. If the source DOES NOT raise an exception, ABSOLUTELY DO NOT use pytest.raises.\n"
            "5. Every assert must have a specific value that matches the read source code.\n\n"
        )
    elif framework == "Jest":
        system_prompt += (
            "\n\n[SUPREME RULES FOR JEST]:\n"
            "1. MUST import the function/class to be tested from the fixed target file named './source_under_test'.\n"
            "   CORRECT Example: `const target = require('./source_under_test');`\n"
            "   INCORRECT Example: `const target = require('./my_code');`\n"
            "2. If the test code uses non-existent external dependencies, you MUST mock them using `jest.mock('library_name');`.\n"
        )
    elif framework == "Postman script":
        system_prompt += (
            "\n\n[MANDATORY RULES FOR POSTMAN]:\n"
            "1. Output MUST be a valid Postman Collection JSON (v2.1.0).\n"
            "2. Each test case MUST have a clear request (method, url, headers, body).\n"
            "3. Each test case MUST have 'test' events containing `pm.test(...)` scripts.\n"
            "4. Assertions MUST check the ACTUAL API response using `pm.response.json()` or `pm.response.text()`.\n"
            "5. ABSOLUTELY DO NOT create hardcoded sample variables in your tests just to assert on them. All expects must be asserted on the parsed JSON from pm.response.\n"
            "6. You MUST include assertions for Status Code AND Response Body/Schema.\n"
            "7. CRITICAL: When asserting headers, DO NOT pass regex to `pm.response.to.have.header(key, value)`. It only accepts strict strings. If you want partial matching, use `pm.expect(pm.response.headers.get('Header-Name')).to.include('value');` instead.\n"
            "8. CRITICAL: When checking for missing fields in JSON, DO NOT use `.to.be.oneOf([null, undefined])`. Instead use `pm.expect(json).to.not.have.property('fieldName');`.\n"
            "9. CRITICAL: When generating boundary values or very long strings for test payloads, DO NOT generate strings longer than 50 characters. Use descriptive values like 'LONG_STRING_OVER_255_CHARS' instead of repeating the same character hundreds of times.\n"
        )

    if framework == "pytest" and (source_code_text or "").strip():
        function_level_output = _generate_function_level_pytest(
            requirement_json=requirement_json,
            test_plan_json=test_plan_json,
            test_technique=test_technique,
            source_code_text=source_code_text,
            backend=backend,
            api_key=api_key,
            model=model,
            system_prompt=system_prompt,
        )
        if function_level_output.strip():
            return function_level_output

    source_context = f"Source Code:\n```\n{source_code_text.strip()}\n```\n\n" if (source_code_text or "").strip() else ""
    prompt = (
        f"Selected framework: {framework}\n\n"
        f"Selected test technique: {test_technique}\n\n"
        "Requirement JSON:\n"
        f"{requirement_json.strip() or 'Needs clarification'}\n\n"
        "Test Plan JSON:\n"
        f"{test_plan_json.strip() or 'Needs clarification'}\n\n"
        f"{source_context}"
        "Please generate executable automated test code according to the selected technique. Output only code."
    )
    return _sanitize_generated_test_code(
        call_llm_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            backend=backend,
            model=_model_for_backend(backend, model),
            api_key=api_key,
            agent_type="code_generator",
        ),
        framework,
    )


from testgen.core.config import PYTEST_COVERAGE_THRESHOLD

def heal_pytest_code(
    test_code: str,
    error_log: str,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
    source_code_text: str = "",
    issue_type: str = "",
    coverage_percent: float = 0.0,
    coverage_threshold: float = PYTEST_COVERAGE_THRESHOLD,
    failure_summary: str = "",
) -> str:
    # Special rules for collection errors (NameError, ImportError preventing test collection)
    collection_error_rules = ""
    if issue_type in ("collection_error", "import_error", "syntax_error"):
        collection_error_rules = (
            "\n\nSPECIAL RULES FOR COLLECTION ERROR (HIGHEST PRIORITY):\n"
            "- The test file failed to COLLECT (import/parse phase), NOT during execution.\n"
            "- CRITICAL: If the error is `NameError: name 'snapshot' is not defined`, you MUST:\n"
            "  1. REMOVE `from inline_snapshot import snapshot` if present (it causes issues).\n"
            "  2. Replace ALL `snapshot()` calls with CONCRETE expected values derived from the source code logic.\n"
            "     Example: `assert func(95) == snapshot()` -> `assert func(95) == 'A'` (read source to get 'A').\n"
            "  3. Do NOT use any placeholder, None, or mock value. Calculate the real expected value.\n"
            "- If the error is `ImportError` or `ModuleNotFoundError`, fix the import statement to correctly reference the available module.\n"
            "- If the error is `SyntaxError`, fix the syntax without changing test logic.\n"
            "- After fix, the file MUST be immediately runnable by pytest with NO extra flags.\n"
        )

    low_coverage_rules = ""
    if issue_type == "low_coverage":
        low_coverage_rules = (
            "\n\nSPECIAL RULES FOR LOW COVERAGE:\n"
            "- You MUST add new test cases to cover the missing lines reported in the Failure summary / Pytest output.\n"
            "- Analyze the source code under test to understand what conditions trigger those missing lines, and write specific tests to reach them.\n"
        )

    system_prompt = (
        "You are a senior Python pytest test repair agent.\n"
        "Your task is to fix only the generated pytest test code.\n"
        "Do not modify, rewrite, or suggest changes to the source code under test.\n\n"
        "Repair rules:\n"
        "1. If an assertion expected value is wrong, update the expected value to match the actual behavior shown by the source code and pytest output.\n"
        "2. If pytest.raises is wrong, keep pytest.raises only when the source code really raises that exception.\n"
        "3. If the exception type or message expectation is wrong, update it to match the source code and pytest output.\n"
        "4. Do not add new tests during heal mode UNLESS you are fixing low coverage.\n"
        "5. Do not remove meaningful assertions.\n"
        "6. Do not reduce the current coverage.\n"
        "7. Preserve imports and helper functions unless they are directly causing the failure.\n"
        "8. NEVER use snapshot() from inline_snapshot in the output. All assertions must use concrete values.\n"
        "9. Return the full corrected pytest file only. Do not explain."
        + collection_error_rules
        + low_coverage_rules
    )
    prompt = (
        f"Current generated pytest code:\n```python\n{test_code}\n```\n\n"
        f"Source code under test:\n```python\n{source_code_text}\n```\n\n"
        f"Execution issue type:\n{issue_type}\n\n"
        f"Coverage:\n{coverage_percent}% / threshold {coverage_threshold}%\n\n"
        f"Failure summary:\n{failure_summary}\n\n"
        f"Pytest output:\n```text\n{error_log}\n```\n\n"
        "Fix the pytest file according to the repair rules.\n"
        "Return only the full corrected pytest code."
    )
    return _sanitize_generated_test_code(
        call_llm_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            backend=backend,
            model=_model_for_backend(backend, model),
            api_key=api_key,
            agent_type="code_generator",
        ),
        "pytest",
    )


def heal_jest_code(
    test_code: str,
    error_log: str,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    system_prompt = (
        "You are a Jest test repair expert. Your task is to diagnose and fix errors arising in the test code.\n"
        "MANDATORY RULES:\n"
        "1. Assertion Errors (Expected/Received): MUST preserve the logic, only take the actual `Received` value and replace the incorrect `Expected` value.\n"
        "2. Crash Errors (TypeError, ReferenceError): Allowed to modify logic, including adding `async/await`, correct type casting, or mocking missing environment variables/global functions.\n"
        "3. Module Errors: Add `jest.mock()` for missing dependencies.\n"
    )
    prompt = (
        f"Current test code with errors:\n```javascript\n{test_code}\n```\n\n"
        f"Jest error log:\n{error_log}\n\n"
        "Please analyze the errors and fix them directly in the test code. Return the entire corrected test code. Output pure code only, no explanations."
    )
    return _sanitize_generated_test_code(
        call_llm_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            backend=backend,
            model=_model_for_backend(backend, model),
            api_key=api_key,
            agent_type="code_generator",
        ),
        "Jest",
    )


def heal_postman_code(
    test_code: str,
    error_log: str,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    system_prompt = (
        "You are a Postman test repair expert. Your task is to diagnose and fix errors arising in the test code.\n"
        "MANDATORY RULES:\n"
        "1. Assertion Errors: If the API returns unexpected values, MUST preserve the logic, only take the actual value from the response and replace the incorrect `Expected` value.\n"
        "2. Missing/Extra Properties: If the API echoes an unexpected property, or omits a property, fix the assertion to match the actual API behavior shown in the error log.\n"
        "3. DO NOT change the structure of the JSON collection. DO NOT invent new test cases.\n"
    )
    prompt = (
        f"Current test collection:\n```json\n{test_code}\n```\n\n"
        f"Postman Newman error log:\n{error_log}\n\n"
        "Please analyze the errors and fix them directly in the collection JSON. Return the entire corrected JSON. Output pure JSON only, no explanations."
    )
    raw_generated = call_llm_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        backend=backend,
        model=_model_for_backend(backend, model),
        api_key=api_key,
        agent_type="code_generator",
    )
    extracted = extract_json_payload(raw_generated, silent=True)
    if isinstance(extracted, dict) and "info" in extracted and "item" in extracted:
        return json.dumps(extracted, indent=2, ensure_ascii=False)
    return _sanitize_generated_test_code(raw_generated, "json")
