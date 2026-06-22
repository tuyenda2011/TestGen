from __future__ import annotations

import json

import pytest

from testgen.agents import requirement_agent, test_planning_agent


# ── requirement_agent ──

def test_requirement_model_for_gemini():
    assert requirement_agent._model_for_backend("gemini") == requirement_agent.GEMINI_REQUIREMENT_MODEL


def test_requirement_model_for_ollama():
    assert requirement_agent._model_for_backend("ollama") == requirement_agent.OLLAMA_REQUIREMENT_MODEL



def test_analyze_requirements_calls_llm(monkeypatch):
    calls = []

    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        calls.append({"prompt": prompt, "backend": backend, "model": model, "agent_type": agent_type})
        return '{"module": "test"}'

    monkeypatch.setattr(requirement_agent, "call_llm_chat", fake_llm_chat)
    result = requirement_agent.analyze_requirements("user query", "context", backend="ollama")
    assert result == '{"module": "test"}'
    assert len(calls) == 1
    assert "user query" in calls[0]["prompt"]
    assert calls[0]["backend"] == "ollama"
    assert calls[0]["agent_type"] == "requirement"


def test_analyze_requirements_handles_empty_inputs(monkeypatch):
    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        assert agent_type == "requirement"
        return '{"missing_information": ["all"]}'

    monkeypatch.setattr(requirement_agent, "call_llm_chat", fake_llm_chat)
    result = requirement_agent.analyze_requirements("", "", backend="gemini", api_key="key")
    assert "missing_information" in result


# ── test_planning_agent ──

def test_analyze_requirements_rejects_invalid_json(monkeypatch):
    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        return "not json"

    monkeypatch.setattr(requirement_agent, "call_llm_chat", fake_llm_chat)
    with pytest.raises(ValueError, match="Requirement Agent"):
        requirement_agent.analyze_requirements("query", "context")


def test_planning_model_for_gemini():
    assert test_planning_agent._model_for_backend("gemini") == test_planning_agent.GEMINI_TEST_PLANNING_MODEL


def test_planning_model_for_ollama():
    assert test_planning_agent._model_for_backend("ollama") == test_planning_agent.OLLAMA_TEST_PLANNING_MODEL



def test_generate_test_plan_calls_llm(monkeypatch):
    calls = []

    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        calls.append({"prompt": prompt, "backend": backend, "agent_type": agent_type})
        return '{"test_scenarios": []}'

    monkeypatch.setattr(test_planning_agent, "call_llm_chat", fake_llm_chat)
    result = test_planning_agent.generate_test_plan('{"module": "auth"}', "Hybrid", backend="ollama")
    assert result == '{"test_scenarios": []}'
    assert len(calls) == 1
    assert "Hybrid" in calls[0]["prompt"]
    assert calls[0]["agent_type"] == "test_planner"


def test_generate_test_plan_includes_ast_context(monkeypatch):
    captured = {}

    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        assert agent_type == "test_planner"
        captured["prompt"] = prompt
        return "{}"

    monkeypatch.setattr(test_planning_agent, "call_llm_chat", fake_llm_chat)
    test_planning_agent.generate_test_plan("{}", "Hybrid", ast_context="AST info here")
    assert "AST info here" in captured["prompt"]


def test_generate_test_plan_omits_ast_when_empty(monkeypatch):
    captured = {}

    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        assert agent_type == "test_planner"
        captured["prompt"] = prompt
        return "{}"

    monkeypatch.setattr(test_planning_agent, "call_llm_chat", fake_llm_chat)
    test_planning_agent.generate_test_plan("{}", "Black-box", ast_context="")
    assert "Black-box" in captured["prompt"]


def test_generate_test_plan_rejects_invalid_json(monkeypatch):
    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        return "not json"

    monkeypatch.setattr(test_planning_agent, "call_llm_chat", fake_llm_chat)
    with pytest.raises(ValueError, match="Test Planning Agent"):
        test_planning_agent.generate_test_plan("{}", "Hybrid")


def test_generate_test_plan_normalizes_ollama_array_object_fields(monkeypatch):
    def fake_llm_chat(prompt, system_prompt, backend, model, api_key, agent_type=None):
        return json.dumps(
            {
                "test_scenarios": [
                    {
                        "id": "TC-001",
                        "type": "positive",
                        "title": "valid data",
                        "preconditions": ["user exists", "account active"],
                        "test_data": {"amount": 100, "currency": "VND"},
                        "expected_result": ["balance updated", "transaction saved"],
                        "priority": "High",
                    }
                ]
            }
        )

    monkeypatch.setattr(test_planning_agent, "call_llm_chat", fake_llm_chat)

    result = test_planning_agent.generate_test_plan("{}", "Hybrid", backend="ollama")
    payload = json.loads(result)
    scenario = payload["test_scenarios"][0]

    assert scenario["preconditions"] == "user exists; account active"
    assert scenario["test_data"] == '{"amount": 100, "currency": "VND"}'
    assert scenario["expected_result"] == "balance updated; transaction saved"
