from __future__ import annotations

from functools import lru_cache

from testgen.core.config import GEMINI_CODE_REVIEW_MODEL, OLLAMA_CODE_REVIEW_MODEL, PROMPTS_PATH
from testgen.core.llm import call_llm_chat
from testgen.prompts.templates import REVIEWER_PROMPT

def _model_for_backend(backend: str, model: str | None = None) -> str | None:
    if model:
        return model
    if backend == "gemini":
        return GEMINI_CODE_REVIEW_MODEL
    if backend == "ollama":
        return OLLAMA_CODE_REVIEW_MODEL
    return None


def review_test_code(
    requirement_json: str,
    test_plan_json: str,
    code_to_review: str,
    framework: str,
    test_technique: str = "Hybrid",
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
    review_target_label: str = "Test code to review",
    source_code_text: str = "",
) -> str:
    system_prompt = REVIEWER_PROMPT
    if framework in ("pytest", "Selenium", "Playwright"):
        system_prompt += (
            "\n\n[PYTEST ERROR LOG GUIDANCE]:\n"
            "Do not change the original source code logic. If your test fails due to value hallucination (E assert X == Y), "
            "find the actual value X in the error log and automatically adjust your assert to match it. "
            "You must strictly adhere to the truth from the execution environment."
        )
    if framework in ("Selenium", "Playwright"):
        system_prompt += (
            "\n\n[E2E FRAMEWORK GUIDANCE]:\n"
            "1. For JavaScript errors (throw new Error), the provided HTML does NOT catch them to display on the UI. "
            "Do NOT recommend asserting on the '#error' element for these cases. Recommend using execute_script/evaluate to catch the JS exception directly.\n"
            "2. Ensure all test cases are strictly implemented and tagged with their exact TC-XXX IDs. Do not recommend hardcoded math.\n"
            "3. DO NOT penalize maintainability for hardcoding the local HTML file path or using Edge driver (webdriver.Edge), as these are required in the execution environment.\n"
            "4. Do NOT penalize test cases for 'Missing meaningful assertions' if they rely on implicit UI interactions (e.g. `find_element`, `click`, `fill`, `expect`) to verify the page state or flow."
        )
    if framework == "Postman script":
        system_prompt += (
            "\n\n[POSTMAN GUIDANCE]:\n"
            "1. Using Regex in `pm.response.to.have.header()` or using `.to.be.oneOf([null, undefined])` to check missing fields are strict syntax errors and MUST be flagged as 'Lỗi nghiêm trọng'.\n"
            "2. Generating excessively long strings (e.g. hundreds of characters) for payloads is strictly prohibited. Flag it as 'Lỗi nghiêm trọng' if a generated string exceeds 50 characters.\n"
            "3. If the test asserts state changes across multiple requests against a dummy API like JSONPlaceholder (e.g., expecting consecutive POSTs to return different IDs), flag it as 'Lỗi nghiêm trọng' because dummy APIs do not persist state.\n"
            "4. Using `pm.expect(pm.response.text()).to.be.empty` to assert an empty JSON object is logically wrong and fails at runtime (because `{}` is not empty). Flag this as 'Lỗi nghiêm trọng' and instruct the generator to use `pm.expect(Object.keys(pm.response.json())).to.be.empty` instead.\n"
            "5. Dummy APIs (like JSONPlaceholder) always return 200 or 201 for POST/PUT requests even if the payload is invalid/missing. If a generated test correctly asserts 200/201 (because that's what the mock API actually returns), DO NOT penalize the test as a 'Lỗi nghiêm trọng' just because the original Test Plan expected a 400 or 500 error. The test is reflecting reality."
        )
    source_block = source_code_text.strip() or "No source code provided."
    prompt = (
        f"Selected framework: {framework}\n\n"
        f"Selected test technique: {test_technique}\n\n"
        "Requirement JSON:\n"
        f"{requirement_json.strip() or 'Needs clarification'}\n\n"
        "Test Plan JSON:\n"
        f"{test_plan_json.strip() or 'Needs clarification'}\n\n"
        "[ORIGINAL SOURCE CODE]\n"
        f"{source_block}\n\n"
        f"{review_target_label}:\n"
        f"{code_to_review.strip() or 'Needs clarification'}\n\n"
        "Please return a concise and clear review report based on the selected technique."
    )
    return call_llm_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        backend=backend,
        model=_model_for_backend(backend, model),
        api_key=api_key,
        agent_type="code_reviewer",
    )
