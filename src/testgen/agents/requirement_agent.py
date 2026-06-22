from __future__ import annotations

from functools import lru_cache

from pydantic import BaseModel, Field, field_validator

from testgen.core.config import GEMINI_REQUIREMENT_MODEL, OLLAMA_REQUIREMENT_MODEL, PROMPTS_PATH
from testgen.core.llm import call_llm_chat
from testgen.core.utils import extract_and_validate_json_payload, extract_json_payload
import json
from testgen.prompts.templates import REQUIREMENT_PROMPT

from typing import Any

class RequirementSchema(BaseModel):
    module: str = ""
    features: list[Any] = Field(default_factory=list)
    inputs: list[Any] = Field(default_factory=list)
    outputs: list[Any] = Field(default_factory=list)
    business_rules: list[Any] = Field(default_factory=list)
    validations: list[Any] = Field(default_factory=list)
    assumptions: list[Any] = Field(default_factory=list)
    missing_information: list[Any] = Field(default_factory=list)

    @field_validator(
        "features", "inputs", "outputs", "business_rules", "validations", "assumptions", "missing_information",
        mode="before"
    )
    @classmethod
    def coerce_to_list(cls, v: Any) -> list[Any]:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return [v] if v.strip() else []
        if v is None:
            return []
        return [str(v)]



def _model_for_backend(backend: str, model: str | None = None) -> str | None:
    if model:
        return model
    if backend == "gemini":
        return GEMINI_REQUIREMENT_MODEL
    if backend == "ollama":
        return OLLAMA_REQUIREMENT_MODEL
    return None


def _normalize_requirement_payload(payload: str) -> str | None:
    data = extract_json_payload(payload, silent=True)
    if data is None:
        return None
    
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    
    if not isinstance(data, dict):
        return None

    def coerce_list(val: Any) -> list[Any]:
        if isinstance(val, list):
            return val
        if isinstance(val, str):
            return [val] if val.strip() else []
        if val is None:
            return []
        return [str(val)]

    normalized_data = {
        "module": str(data.get("module", "")),
        "features": coerce_list(data.get("features", data.get("feature"))),
        "inputs": coerce_list(data.get("inputs", data.get("input"))),
        "outputs": coerce_list(data.get("outputs", data.get("output"))),
        "business_rules": coerce_list(data.get("business_rules", data.get("rules"))),
        "validations": coerce_list(data.get("validations", data.get("validation"))),
        "assumptions": coerce_list(data.get("assumptions", data.get("assumption"))),
        "missing_information": coerce_list(data.get("missing_information", data.get("missing"))),
    }

    normalized = json.dumps(normalized_data, ensure_ascii=False)
    if extract_and_validate_json_payload(normalized, RequirementSchema, silent=True) is None:
        return None
    return normalized


def _ensure_valid_requirement_json(payload: str) -> str:
    if extract_and_validate_json_payload(payload, RequirementSchema, silent=True) is not None:
        return payload

    normalized = _normalize_requirement_payload(payload)
    if normalized is None:
        raise ValueError("Requirement Agent trả về JSON không đúng schema.")
    return normalized


def analyze_requirements(
    user_query: str,
    context: str,
    framework: str,
    backend: str = "ollama",
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    system_prompt = REQUIREMENT_PROMPT.format(framework=framework)
    prompt = (
        "Văn bản yêu cầu của người dùng:\n"
        f"{user_query.strip() or 'Cần làm rõ'}\n\n"
        "Ngữ cảnh truy xuất:\n"
        f"{context.strip() or 'Cần làm rõ'}\n\n"
        "Hãy trả về JSON có cấu trúc, chỉ gồm JSON."
    )
    result = call_llm_chat(
        prompt=prompt,
        system_prompt=system_prompt,
        backend=backend,
        model=_model_for_backend(backend, model),
        api_key=api_key,
        agent_type="requirement",
    )
    return _ensure_valid_requirement_json(result)
