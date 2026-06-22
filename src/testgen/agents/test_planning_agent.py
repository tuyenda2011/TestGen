from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import BaseModel, Field, field_validator

from testgen.core.config import GEMINI_TEST_PLANNING_MODEL, OLLAMA_TEST_PLANNING_MODEL, PROMPTS_PATH
from testgen.core.llm import call_llm_chat
from testgen.core.logger import get_logger
from testgen.core.utils import extract_and_validate_json_payload, extract_json_payload

logger = get_logger(__name__)
from testgen.prompts.templates import TEST_PLANNING_PROMPT


class TestCaseSchema(BaseModel):
    id: str = ""
    type: str = ""
    title: str = ""
    preconditions: str = ""
    test_data: str = ""
    expected_result: str = ""
    priority: str = ""

    @field_validator("preconditions", "test_data", "expected_result", mode="before")
    @classmethod
    def coerce_to_string(cls, v: Any) -> str:
        if isinstance(v, (dict, list)):
            return json.dumps(v, ensure_ascii=False)
        return str(v)


class TestPlanSchema(BaseModel):
    test_scenarios: list[TestCaseSchema] = Field(default_factory=list)


def _model_for_backend(backend: str, model: str | None = None) -> str | None:
    if model:
        return model
    if backend == "gemini":
        return GEMINI_TEST_PLANNING_MODEL
    if backend == "ollama":
        return OLLAMA_TEST_PLANNING_MODEL
    return None


def _coerce_plan_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        parts = [_coerce_plan_text(item) for item in value]
        return "; ".join(part for part in parts if part)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value).strip()


def _scenario_value(scenario: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in scenario:
            return scenario.get(key)
    return ""


def _normalize_test_plan_payload(payload: str) -> str | None:
    data = extract_json_payload(payload, silent=True)
    if data is None:
        return None

    if isinstance(data, list):
        scenarios = data
    elif isinstance(data, dict):
        scenarios = (
            data.get("test_scenarios")
            or data.get("test_cases")
            or data.get("scenarios")
            or data.get("tests")
            or []
        )
        if isinstance(scenarios, dict):
            scenarios = [scenarios]
    else:
        return None

    if not isinstance(scenarios, list):
        scenarios = []

    normalized_scenarios: list[dict[str, str]] = []
    for index, raw_scenario in enumerate(scenarios, start=1):
        scenario = raw_scenario if isinstance(raw_scenario, dict) else {"title": raw_scenario}
        normalized_scenarios.append(
            {
                "id": _coerce_plan_text(
                    _scenario_value(scenario, "id", "test_id", "case_id")
                    or f"TC-{index:03d}"
                ),
                "type": _coerce_plan_text(
                    _scenario_value(scenario, "type", "category", "test_type")
                    or "clarification"
                ),
                "title": _coerce_plan_text(
                    _scenario_value(scenario, "title", "name", "scenario")
                ),
                "preconditions": _coerce_plan_text(
                    _scenario_value(scenario, "preconditions", "precondition", "setup")
                ),
                "test_data": _coerce_plan_text(
                    _scenario_value(scenario, "test_data", "data", "input", "inputs")
                ),
                "expected_result": _coerce_plan_text(
                    _scenario_value(
                        scenario,
                        "expected_result",
                        "expected",
                        "expected_output",
                        "expected_behavior",
                    )
                ),
                "priority": _coerce_plan_text(
                    _scenario_value(scenario, "priority", "severity") or "Medium"
                ),
            }
        )

    normalized = json.dumps({"test_scenarios": normalized_scenarios}, ensure_ascii=False)
    if extract_and_validate_json_payload(normalized, TestPlanSchema, silent=True) is None:
        return None
    return normalized


def _ensure_valid_test_plan_json(payload: str) -> str:
    if extract_and_validate_json_payload(payload, TestPlanSchema) is not None:
        return payload

    normalized_payload = _normalize_test_plan_payload(payload)
    if normalized_payload is None:
        with open(r"d:\Chatbot\scratch\planning_error_payload.txt", "w", encoding="utf-8") as f:
            f.write(payload)
        raise ValueError("Test Planning Agent trả về JSON không đúng schema. Đã lưu raw payload vào d:/Chatbot/scratch/planning_error_payload.txt để debug.")
    return normalized_payload


def generate_test_plan(
    requirement_json: str,
    test_technique: str = "Hybrid",
    backend: str = "ollama",
    api_key: str | None = None,
    ast_context: str = "",
    model: str | None = None,
) -> str:
    system_prompt = TEST_PLANNING_PROMPT
    ast_prompt = f"\n\n{ast_context}\n" if ast_context else ""
    base_prompt = (
        f"Kỹ thuật kiểm thử đã chọn: {test_technique}\n\n"
        "JSON yêu cầu:\n"
        f"{requirement_json.strip() or 'Cần làm rõ'}\n"
        f"{ast_prompt}\n"
        "Hãy tạo ngay JSON kế hoạch kiểm thử theo kỹ thuật đã chọn. "
        "Tất cả field trong mỗi scenario phải là chuỗi, không dùng array/object cho preconditions, test_data hoặc expected_result."
    )
    
    max_retries = 3
    last_payload = ""
    for attempt in range(max_retries):
        if attempt == 0:
            prompt = base_prompt
        else:
            logger.warning(f"Test Planner retry {attempt}/{max_retries - 1} due to JSON schema error.")
            prompt = (
                f"{base_prompt}\n\n"
                "LẦN THỬ TRƯỚC BỊ LỖI JSON SCHEMA:\n"
                f"Payload đã sinh:\n{last_payload}\n"
                "Lỗi: Payload bạn trả về không phải là JSON hợp lệ (có thể bạn đã dùng biểu thức JavaScript như .repeat() hoặc nối chuỗi + bên trong chuỗi JSON). "
                "HÃY CHỈ TRẢ VỀ JSON HỢP LỆ THEO ĐÚNG SCHEMA. TUYỆT ĐỐI KHÔNG SỬ DỤNG JAVASCRIPT BÊN TRONG JSON!"
            )
            
        result = call_llm_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            backend=backend,
            model=_model_for_backend(backend, model),
            api_key=api_key,
            agent_type="test_planner",
        )
        last_payload = result
        
        try:
            return _ensure_valid_test_plan_json(result)
        except ValueError as e:
            if attempt == max_retries - 1:
                logger.error(f"Test Planner failed to generate valid JSON after {max_retries} attempts.")
                raise e
    
    raise ValueError("Unexpected error in generate_test_plan retry loop")
