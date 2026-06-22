from __future__ import annotations

from types import SimpleNamespace

from testgen.agents import code_reviewer_agent
from testgen.core import llm


def test_call_llm_chat_routes_to_gemini_backend(monkeypatch):
    captured = {}

    def fake_post(url, json, timeout, headers=None):
        captured["url"] = url
        captured["json"] = json
        captured["timeout"] = timeout
        captured["headers"] = headers
        return SimpleNamespace(
            status_code=200,
            json=lambda: {
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": "gemini-response"}],
                        }
                    }
                ]
            },
            text="{}",
        )

    monkeypatch.setattr(llm.requests, "post", fake_post)

    result = llm.call_llm_chat(
        "Hello",
        system_prompt="System",
        backend="gemini",
        model="gemini-2.0-flash",
        api_key="test-key",
    )

    assert result == "gemini-response"
    assert captured["url"].endswith("/models/gemini-2.0-flash:generateContent")
    assert captured["headers"]["x-goog-api-key"] == "test-key"
    assert "System" in captured["json"]["contents"][0]["parts"][0]["text"]


def test_get_gemini_embedding_parses_vector(monkeypatch):
    def fake_post(url, json, timeout, headers=None):
        return SimpleNamespace(
            status_code=200,
            json=lambda: {"embedding": {"values": [1, 2.5, 3]}},
            text="{}",
        )

    monkeypatch.setattr(llm.requests, "post", fake_post)

    embedding = llm.get_gemini_embedding("hello", api_key="test-key")

    assert embedding == [1.0, 2.5, 3.0]


def test_review_test_code_uses_custom_target_label(monkeypatch):
    captured = {}

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        captured["prompt"] = prompt
        captured["system_prompt"] = system_prompt
        captured["backend"] = backend
        captured["model"] = model
        captured["api_key"] = api_key
        captured["agent_type"] = agent_type
        return "review-report"

    monkeypatch.setattr(code_reviewer_agent, "call_llm_chat", fake_call_llm_chat)

    result = code_reviewer_agent.review_test_code(
        requirement_json='{"module": "auth"}',
        test_plan_json='{"test_scenarios": []}',
        code_to_review="assert True",
        framework="pytest",
        test_technique="White-box",
        backend="gemini",
        api_key="test-key",
        review_target_label="Test code người dùng cung cấp",
        source_code_text="def login(username, password): return True",
    )

    assert result == "review-report"
    assert "Test code người dùng cung cấp" in captured["prompt"]
    assert "[MÃ NGUỒN GỐC]" in captured["prompt"]
    assert "def login(username, password): return True" in captured["prompt"]
    assert "Kỹ thuật kiểm thử đã chọn: White-box" in captured["prompt"]
    assert "assert True" in captured["prompt"]
    assert captured["backend"] == "gemini"
    assert captured["model"] == "gemini-2.0-flash"
    assert captured["api_key"] == "test-key"
    assert captured["agent_type"] == "code_reviewer"

