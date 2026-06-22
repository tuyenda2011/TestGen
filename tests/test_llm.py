from __future__ import annotations

import pytest
import requests
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

from testgen.core import llm


# ── _usable_api_key ──

def test_usable_api_key_returns_key():
    assert llm._usable_api_key("my-key") == "my-key"


def test_usable_api_key_strips_whitespace():
    assert llm._usable_api_key("  key  ") == "key"


def test_usable_api_key_returns_empty_for_none():
    assert llm._usable_api_key(None) == ""


def test_usable_api_key_returns_empty_for_placeholder():
    assert llm._usable_api_key("your-gemini-api-key") == ""


def test_usable_api_key_returns_empty_for_blank():
    assert llm._usable_api_key("   ") == ""


# ── _require_gemini_key ──

def test_require_gemini_key_returns_valid_key():
    assert llm._require_gemini_key("valid-key") == "valid-key"


def test_require_gemini_key_raises_for_missing():
    with pytest.raises(RuntimeError, match="API key"):
        llm._require_gemini_key(None)


def test_require_gemini_key_raises_for_placeholder():
    with pytest.raises(RuntimeError, match="API key"):
        llm._require_gemini_key("your-gemini-api-key")


# ── _gemini_headers ──

def test_gemini_headers_contains_api_key():
    headers = llm._gemini_headers("test-key")
    assert headers["x-goog-api-key"] == "test-key"
    assert "application/json" in headers["Content-Type"]


# ── _to_float_list ──

def test_to_float_list_converts_ints():
    assert llm._to_float_list([1, 2, 3], "err") == [1.0, 2.0, 3.0]


def test_to_float_list_converts_strings():
    assert llm._to_float_list(["1.5", "2.5"], "err") == [1.5, 2.5]


def test_to_float_list_raises_on_bad_values():
    with pytest.raises(RuntimeError, match="custom error"):
        llm._to_float_list(["not_a_number"], "custom error")


# ── _ollama_messages ──

def test_ollama_messages_without_system():
    msgs = llm._ollama_messages("hello", None)
    assert len(msgs) == 1
    assert msgs[0] == {"role": "user", "content": "hello"}


def test_ollama_messages_with_system():
    msgs = llm._ollama_messages("hello", "system prompt")
    assert len(msgs) == 2
    assert msgs[0] == {"role": "system", "content": "system prompt"}
    assert msgs[1] == {"role": "user", "content": "hello"}


# ── _post_json ──

def test_post_json_connection_error_ollama(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("refused")

    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="Ollama"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_connection_error_gemini(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("refused")

    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="Gemini"):
        llm._post_json("https://generativelanguage.googleapis.com/v1", {}, timeout=5)


def test_post_json_timeout_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.Timeout("timed out")

    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="hết thời gian"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_generic_request_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.RequestException("network error")

    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="kết nối"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_http_error_with_json_body(monkeypatch):
    resp = MagicMock()
    resp.status_code = 400
    resp.text = "Bad Request"
    resp.json.return_value = {"error": {"message": "invalid model"}}

    monkeypatch.setattr(requests, "post", lambda *a, **kw: resp)
    with pytest.raises(RuntimeError, match="invalid model"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_http_error_with_plain_error(monkeypatch):
    resp = MagicMock()
    resp.status_code = 401
    resp.text = "Unauthorized"
    resp.json.return_value = {"error": "unauthorized access"}

    monkeypatch.setattr(requests, "post", lambda *a, **kw: resp)
    with pytest.raises(RuntimeError, match="unauthorized"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_http_error_non_json(monkeypatch):
    resp = MagicMock()
    resp.status_code = 500
    resp.text = "Internal Server Error"
    resp.json.side_effect = ValueError("no json")

    monkeypatch.setattr(requests, "post", lambda *a, **kw: resp)
    with pytest.raises(RuntimeError, match="500"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_invalid_json_response(monkeypatch):
    resp = MagicMock()
    resp.status_code = 200
    resp.text = "not json"
    resp.json.side_effect = ValueError("bad json")

    monkeypatch.setattr(requests, "post", lambda *a, **kw: resp)
    with pytest.raises(RuntimeError, match="JSON không hợp lệ"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_non_dict_response(monkeypatch):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = [1, 2, 3]  # list, not dict

    monkeypatch.setattr(requests, "post", lambda *a, **kw: resp)
    with pytest.raises(RuntimeError, match="cấu trúc"):
        llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)


def test_post_json_success(monkeypatch):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"result": "ok"}

    monkeypatch.setattr(requests, "post", lambda *a, **kw: resp)
    result = llm._post_json("http://localhost:11434/api/chat", {}, timeout=5)
    assert result == {"result": "ok"}


def test_post_json_retries_openrouter_overload(monkeypatch):
    calls = []
    sleeps = []

    retry_response = MagicMock()
    retry_response.status_code = 429
    retry_response.text = "Too Many Requests"
    retry_response.json.return_value = {"error": {"message": "rate limited"}}

    ok_response = MagicMock()
    ok_response.status_code = 200
    ok_response.json.return_value = {"result": "ok"}

    responses = [retry_response, ok_response]

    def fake_post(*args, **kwargs):
        calls.append(kwargs)
        return responses.pop(0)

    monkeypatch.setattr(requests, "post", fake_post)
    monkeypatch.setattr(llm, "_retry_sleep", lambda seconds: sleeps.append(seconds))

    result = llm._post_json(llm.OPENROUTER_CHAT_URL, {"prompt": "x"}, timeout=5)

    assert result == {"result": "ok"}
    assert len(calls) == 2
    assert sleeps == [3.0]


def test_call_openrouter_chat_streams_sse_response(monkeypatch):
    captured: dict[str, object] = {}
    streamed_chunks: list[str] = []

    class FakeResponse:
        status_code = 200
        text = ""

        def iter_lines(self, decode_unicode=True):
            yield 'data: {"choices":[{"delta":{"content":"hello "}}]}'
            yield 'data: {"choices":[{"delta":{"content":"world"}}]}'
            yield "data: [DONE]"

        def close(self):
            captured["closed"] = True

    def fake_post(url, json, timeout, headers=None, stream=False):
        captured["stream"] = stream
        captured["payload_stream"] = json.get("stream")
        return FakeResponse()

    def stream_writer(chunks):
        for chunk in chunks:
            streamed_chunks.append(chunk)
        return "".join(streamed_chunks)

    monkeypatch.setattr(requests, "post", fake_post)

    with llm.use_stream_writer(stream_writer):
        result = llm.call_openrouter_chat("prompt", api_key="key", models=["model-a"])

    assert result == "hello world"
    assert streamed_chunks == ["hello ", "world"]
    assert captured["stream"] is True
    assert captured["payload_stream"] is True
    assert captured["closed"] is True


# ── _extract_gemini_text ──

def test_extract_gemini_text_from_candidates():
    body = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "  hello world  "}]
                }
            }
        ]
    }
    assert llm._extract_gemini_text(body) == "hello world"


def test_extract_gemini_text_from_top_level():
    body = {"text": "  direct text  "}
    assert llm._extract_gemini_text(body) == "direct text"


def test_extract_gemini_text_raises_when_missing():
    with pytest.raises(RuntimeError, match="Gemini"):
        llm._extract_gemini_text({})


def test_extract_gemini_text_skips_non_dict_candidates():
    body = {"candidates": ["not a dict"]}
    with pytest.raises(RuntimeError):
        llm._extract_gemini_text(body)


# ── _extract_gemini_embedding_values ──

def test_extract_embedding_from_embedding_key():
    body = {"embedding": {"values": [0.1, 0.2]}}
    assert llm._extract_gemini_embedding_values(body) == [0.1, 0.2]


def test_extract_embedding_from_embeddings_list():
    body = {"embeddings": [{"values": [0.3, 0.4]}]}
    assert llm._extract_gemini_embedding_values(body) == [0.3, 0.4]


def test_extract_embedding_returns_none_when_missing():
    assert llm._extract_gemini_embedding_values({}) is None


# ── call_llm_chat ──

def test_call_llm_chat_routes_to_ollama(monkeypatch):
    monkeypatch.setattr(llm, "call_ollama_chat", lambda prompt, system_prompt, model: "ollama response")
    result = llm.call_llm_chat("test", backend="ollama")
    assert result == "ollama response"


def test_call_llm_chat_routes_to_gemini(monkeypatch):
    monkeypatch.setattr(llm, "call_gemini_chat", lambda prompt, system_prompt, model, api_key: "gemini response")
    result = llm.call_llm_chat("test", backend="gemini", api_key="key")
    assert result == "gemini response"


# ── get_embedding ──

def test_call_llm_chat_openrouter_uses_selected_model_first(monkeypatch):
    captured = {}

    def fake_openrouter_chat(prompt, system_prompt, api_key, models):
        captured["models"] = models
        return "openrouter response"

    monkeypatch.setattr(llm, "call_openrouter_chat", fake_openrouter_chat)

    result = llm.call_llm_chat(
        "test",
        backend="openrouter",
        model="custom/provider-model:free",
        api_key="key",
        agent_type="requirement",
    )

    assert result == "openrouter response"
    assert captured["models"][0] == "custom/provider-model:free"
    assert "z-ai/glm-4.5-air:free" in captured["models"]


def test_call_openrouter_chat_reports_all_failed_models(monkeypatch):
    calls = []

    def fake_post_json(url, payload, timeout, headers=None):
        calls.append(payload["model"])
        raise RuntimeError(f"{payload['model']} failed")

    monkeypatch.setattr(llm, "_post_json", fake_post_json)

    with pytest.raises(RuntimeError) as exc_info:
        llm.call_openrouter_chat("prompt", api_key="key", models=["model-a", "model-b"], stream=False)

    message = str(exc_info.value)
    assert calls == ["model-a", "model-b"]
    assert "model-a, model-b" in message
    assert "model-b failed" in message


def test_get_embedding_routes_to_ollama(monkeypatch):
    monkeypatch.setattr(llm, "get_ollama_embedding", lambda text: [1.0, 2.0])
    result = llm.get_embedding("text", backend="ollama")
    assert result == [1.0, 2.0]


def test_get_embedding_routes_to_gemini(monkeypatch):
    monkeypatch.setattr(llm, "get_gemini_embedding", lambda text, api_key: [3.0, 4.0])
    result = llm.get_embedding("text", backend="gemini", api_key="key")
    assert result == [3.0, 4.0]


# ── call_ollama_chat ──

def test_call_ollama_chat_parses_response(monkeypatch):
    def fake_post_json(url, payload, timeout, headers=None):
        return {"message": {"content": "  test response  "}}

    monkeypatch.setattr(llm, "_post_json", fake_post_json)
    result = llm.call_ollama_chat("prompt")
    assert result == "test response"


def test_call_ollama_chat_raises_on_missing_message(monkeypatch):
    monkeypatch.setattr(llm, "_post_json", lambda *a, **kw: {"result": "no message"})
    with pytest.raises(RuntimeError, match="Ollama"):
        llm.call_ollama_chat("prompt")


def test_call_ollama_chat_raises_on_non_string_content(monkeypatch):
    monkeypatch.setattr(llm, "_post_json", lambda *a, **kw: {"message": {"content": 123}})
    with pytest.raises(RuntimeError, match="văn bản"):
        llm.call_ollama_chat("prompt")


# ── call_gemini_chat ──

def test_call_gemini_chat_parses_response(monkeypatch):
    def fake_post_json(url, payload, timeout, headers=None):
        return {
            "candidates": [{"content": {"parts": [{"text": "gemini result"}]}}]
        }

    monkeypatch.setattr(llm, "_post_json", fake_post_json)
    result = llm.call_gemini_chat("prompt", api_key="key")
    assert result == "gemini result"


def test_call_gemini_chat_raises_without_key():
    with pytest.raises(RuntimeError, match="API key"):
        llm.call_gemini_chat("prompt", api_key=None)
