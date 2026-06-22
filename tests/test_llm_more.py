import pytest
import requests
from unittest.mock import patch, MagicMock

from testgen.core import llm

def test_raise_for_bad_response_retryable(monkeypatch):
    resp = MagicMock()
    resp.status_code = 502
    resp.text = "Bad Gateway"
    resp.json.side_effect = ValueError
    
    with pytest.raises(llm._RetryableHTTPError):
        llm._raise_for_bad_response(resp, llm.OPENROUTER_CHAT_URL)

def test_post_stream_response_connection_error(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("refused")
    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="Ollama"):
        # Not exported so need to use it inside a lambda that is retried or directly
        llm._post_stream_response("http://localhost:11434/api/chat", {}, timeout=5)

def test_post_stream_response_timeout(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.Timeout("timed out")
    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="hết thời gian"):
        llm._post_stream_response("http://localhost:11434/api/chat", {}, timeout=5)

def test_post_stream_response_request_exception(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.RequestException("error")
    monkeypatch.setattr(requests, "post", fake_post)
    with pytest.raises(RuntimeError, match="kết nối"):
        llm._post_stream_response("http://localhost:11434/api/chat", {}, timeout=5)

def test_iter_openrouter_sse_chunks_variations():
    class FakeResponse:
        def iter_lines(self, decode_unicode=False):
            yield b""  # Empty line
            yield b"data: not json"  # ValueError
            yield b'data: {"choices": []}'  # Empty choices
            yield b'data: {"choices": ["not_dict"]}'  # non-dict choice
            yield b'data: {"choices": [{"message": {"content": "hello "}}]}'  # Using message content
            yield b"data: [DONE]"
            yield b'data: {"choices": [{"delta": {"content": "skipped"}}]}'  # Skipped due to DONE
    
    res = list(llm._iter_openrouter_sse_chunks(FakeResponse()))
    assert res == ["hello "]

def test_collect_stream_no_writer():
    assert llm._collect_stream(iter(["a", "b"])) == "ab"

def test_collect_stream_with_writer_returning_none():
    def dummy_writer(chunks):
        for _ in chunks: pass
        return None
    with llm.use_stream_writer(dummy_writer):
        assert llm._collect_stream(iter(["a", "b"])) == "ab"

def test_get_ollama_embedding_bad_response(monkeypatch):
    monkeypatch.setattr(llm, "_post_json", lambda *a, **k: {"embedding": "not_a_list"})
    with pytest.raises(RuntimeError, match="thiếu vector embedding"):
        llm.get_ollama_embedding("test")

def test_get_gemini_embedding_bad_response(monkeypatch):
    monkeypatch.setattr(llm, "_post_json", lambda *a, **k: {"embedding": "not_a_list"})
    with pytest.raises(RuntimeError, match="thiếu vector embedding"):
        llm.get_gemini_embedding("test", api_key="key")

def test_get_gemini_embedding_with_task_type(monkeypatch):
    captured_payload = {}
    def fake_post_json(url, payload, timeout, headers=None):
        captured_payload.update(payload)
        return {"embedding": {"values": [0.1, 0.2]}}
    
    monkeypatch.setattr(llm, "_post_json", fake_post_json)
    llm.get_gemini_embedding("test", api_key="key", task_type="CUSTOM")
    assert captured_payload["task_type"] == "CUSTOM"
