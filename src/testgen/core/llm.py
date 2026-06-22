from __future__ import annotations

import json
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Literal

import requests
from tenacity import Retrying, retry_if_exception_type, stop_after_attempt, wait_chain, wait_fixed

from testgen.core.config import (
    EMBED_MODEL,
    GEMINI_CHAT_URL,
    GEMINI_CODE_GENERATOR_MODEL,
    GEMINI_EMBED_MODEL,
    GEMINI_EMBED_URL,
    MAIN_MODEL,
    NUM_CTX,
    NUM_PREDICT,
    OLLAMA_CHAT_URL,
    OLLAMA_EMBED_URL,
    OLLAMA_EMBED_BATCH_URL,
    OPENROUTER_CHAT_URL,
    TEMPERATURE,
)


Backend = Literal["ollama", "gemini", "openrouter"]
StreamWriter = Callable[[Iterator[str]], str | None]

_STREAM_WRITER: ContextVar[StreamWriter | None] = ContextVar("llm_stream_writer", default=None)
_OPENROUTER_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

_OLLAMA_UNAVAILABLE_MESSAGE = (
    "Ollama chưa chạy tại http://localhost:11434. "
    "Hãy khởi động Ollama, sau đó kéo các mô hình cần thiết bằng "
    f"`ollama pull {MAIN_MODEL}` và `ollama pull {EMBED_MODEL}`."
)

_GEMINI_UNAVAILABLE_MESSAGE = (
    "Gemini API key chưa hợp lệ hoặc Gemini API không phản hồi. "
    "Hãy kiểm tra API key và mô hình được chọn."
)


class _RetryableHTTPError(RuntimeError):
    pass


@contextmanager
def use_stream_writer(writer: StreamWriter | None) -> Iterator[None]:
    token = _STREAM_WRITER.set(writer)
    try:
        yield
    finally:
        _STREAM_WRITER.reset(token)


def _retry_sleep(seconds: float) -> None:
    time.sleep(seconds)


def _retry_wait_strategy():
    return wait_chain(wait_fixed(3), wait_fixed(5), wait_fixed(10))


def _with_retry(operation):
    for attempt in Retrying(
        stop=stop_after_attempt(4),
        wait=_retry_wait_strategy(),
        retry=retry_if_exception_type(_RetryableHTTPError),
        reraise=True,
        sleep=_retry_sleep,
    ):
        with attempt:
            return operation()
    raise RuntimeError("Không thể thực hiện yêu cầu AI.")


def _usable_api_key(value: str | None) -> str:
    key = (value or "").strip()
    if not key or key == "your-gemini-api-key":
        return ""
    if not key.isascii():
        raise RuntimeError("API Key đang chứa ký tự tiếng Việt hoặc ký tự lạ (như chữ 'ầ'). Vui lòng xóa API Key đi và nhập lại chuẩn từ đầu!")
    return key


def _require_gemini_key(api_key: str | None) -> str:
    key = _usable_api_key(api_key)
    if not key:
        raise RuntimeError("Gemini API key bị thiếu.")
    return key


def _gemini_headers(api_key: str) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }


def _to_float_list(values: list[Any], error_message: str) -> list[float]:
    try:
        return [float(value) for value in values]
    except (TypeError, ValueError) as exc:
        raise RuntimeError(error_message) from exc


def _response_error_text(response: requests.Response) -> str:
    error_text = response.text.strip()
    try:
        body = response.json()
    except ValueError:
        body = None
    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            error_text = str(error.get("message") or error.get("status") or error_text)
        else:
            error_text = str(body.get("message") or error or error_text)
    return error_text


def _raise_for_bad_response(response: requests.Response, url: str) -> None:
    if response.status_code < 400:
        return
    message = f"Yêu cầu thất bại ({response.status_code}): {_response_error_text(response)}"
    if url == OPENROUTER_CHAT_URL and response.status_code in _OPENROUTER_RETRYABLE_STATUS_CODES:
        raise _RetryableHTTPError(message)
    raise RuntimeError(message)


def _post_json_once(
    url: str,
    payload: dict[str, Any],
    timeout: int,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    try:
        response = requests.post(url, json=payload, timeout=timeout, headers=headers)
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(_OLLAMA_UNAVAILABLE_MESSAGE if "11434" in url else _GEMINI_UNAVAILABLE_MESSAGE) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError("Yêu cầu đã hết thời gian chờ. Hãy kiểm tra mô hình rồi thử lại.") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Không thể kết nối tới dịch vụ AI: {exc}") from exc

    _raise_for_bad_response(response, url)

    try:
        body = response.json()
    except ValueError as exc:
        raise RuntimeError(f"Phản hồi JSON không hợp lệ: {response.text[:200]}") from exc

    if not isinstance(body, dict):
        raise RuntimeError("Phản hồi không mang cấu trúc mong đợi.")
    return body


def _post_json(
    url: str,
    payload: dict[str, Any],
    timeout: int,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    return _with_retry(lambda: _post_json_once(url, payload, timeout, headers))


def _post_stream_response(
    url: str,
    payload: dict[str, Any],
    timeout: int,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    def send() -> requests.Response:
        try:
            response = requests.post(url, json=payload, timeout=timeout, headers=headers, stream=True)
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(_OLLAMA_UNAVAILABLE_MESSAGE if "11434" in url else _GEMINI_UNAVAILABLE_MESSAGE) from exc
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("Yêu cầu đã hết thời gian chờ. Hãy kiểm tra mô hình rồi thử lại.") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Không thể kết nối tới dịch vụ AI: {exc}") from exc

        _raise_for_bad_response(response, url)
        return response

    return _with_retry(send)


def _iter_openrouter_sse_chunks(response: requests.Response) -> Iterator[str]:
    try:
        for raw_line in response.iter_lines(decode_unicode=False):
            if not raw_line:
                continue
            line = raw_line.decode("utf-8", errors="replace") if isinstance(raw_line, bytes) else str(raw_line)
            if not line.startswith("data:"):
                continue
            data = line.removeprefix("data:").strip()
            if data == "[DONE]":
                break
            try:
                event = json.loads(data)
            except ValueError:
                continue
            choices = event.get("choices")
            if not isinstance(choices, list) or not choices:
                continue
            choice = choices[0]
            if not isinstance(choice, dict):
                continue
            delta = choice.get("delta")
            message = choice.get("message")
            content = None
            if isinstance(delta, dict):
                content = delta.get("content")
            if content is None and isinstance(message, dict):
                content = message.get("content")
            if isinstance(content, str) and content:
                yield content
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


def _collect_stream(chunks: Iterator[str]) -> str:
    collected: list[str] = []

    def tapped() -> Iterator[str]:
        for chunk in chunks:
            collected.append(chunk)
            yield chunk

    writer = _STREAM_WRITER.get()
    if writer is not None:
        rendered = writer(tapped())
        if isinstance(rendered, str) and rendered.strip():
            return rendered.strip()
    else:
        for _chunk in tapped():
            pass
    return "".join(collected).strip()


def _ollama_messages(prompt: str, system_prompt: str | None) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return messages


def call_ollama_chat(prompt: str, system_prompt: str | None = None, model: str | None = None) -> str:
    payload = {
        "model": model or MAIN_MODEL,
        "messages": _ollama_messages(prompt, system_prompt),
        "stream": False,
        "options": {
            "num_ctx": NUM_CTX,
            "temperature": TEMPERATURE,
            "num_predict": NUM_PREDICT,
        },
    }
    body = _post_json(OLLAMA_CHAT_URL, payload, timeout=1200)
    message = body.get("message")
    if not isinstance(message, dict):
        raise RuntimeError("Phản hồi chat của Ollama thiếu nội dung trợ lý.")

    content = message.get("content")
    if not isinstance(content, str):
        raise RuntimeError("Phản hồi chat của Ollama thiếu phần văn bản.")
    return content.strip()


def call_gemini_chat(
    prompt: str,
    system_prompt: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> str:
    key = _require_gemini_key(api_key)
    model_name = model or GEMINI_CODE_GENERATOR_MODEL
    full_prompt = prompt if not system_prompt else f"{system_prompt}\n\n{prompt}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": full_prompt}],
            }
        ],
        "generationConfig": {
            "temperature": TEMPERATURE,
            "maxOutputTokens": NUM_PREDICT,
        },
    }
    body = _post_json(
        GEMINI_CHAT_URL.format(model=model_name),
        payload,
        timeout=1200,
        headers=_gemini_headers(key),
    )
    return _extract_gemini_text(body)


def _call_openrouter_chat_non_stream(
    prompt: str,
    system_prompt: str | None = None,
    api_key: str | None = None,
    models: list[str] | None = None,
) -> str:
    """Gọi OpenRouter API, thử lần lượt từng model trong danh sách fallback."""
    key = (api_key or "").strip()
    if not key:
        raise RuntimeError("OpenRouter API key bị thiếu.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }
    messages = _ollama_messages(prompt, system_prompt)

    models_to_try = models or ["openai/gpt-oss-120b:free"]
    last_error = None
    failed_models: list[str] = []

    for model_id in models_to_try:
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": TEMPERATURE,
            "max_tokens": NUM_PREDICT,
        }
        try:
            body = _post_json(OPENROUTER_CHAT_URL, payload, timeout=1200, headers=headers)
            choices = body.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                if isinstance(content, str) and content.strip():
                    return content.strip()
            raise RuntimeError("OpenRouter trả về rỗng.")
        except RuntimeError as exc:
            last_error = exc
            failed_models.append(model_id)
            continue

    tried = ", ".join(failed_models or models_to_try)
    raise RuntimeError(
        "Tất cả model OpenRouter đều thất bại. "
        f"Models tried: {tried}. Lỗi cuối: {last_error}"
    )


def call_openrouter_chat_stream(
    prompt: str,
    system_prompt: str | None = None,
    api_key: str | None = None,
    models: list[str] | None = None,
) -> Iterator[str]:
    key = (api_key or "").strip()
    if not key:
        raise RuntimeError("OpenRouter API key bị thiếu.")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    }
    messages = _ollama_messages(prompt, system_prompt)
    models_to_try = models or ["openai/gpt-oss-120b:free"]
    last_error = None
    failed_models: list[str] = []

    for model_id in models_to_try:
        payload = {
            "model": model_id,
            "messages": messages,
            "temperature": TEMPERATURE,
            "max_tokens": NUM_PREDICT,
            "stream": True,
        }
        emitted = False
        try:
            response = _post_stream_response(OPENROUTER_CHAT_URL, payload, timeout=1200, headers=headers)
            for chunk in _iter_openrouter_sse_chunks(response):
                emitted = True
                yield chunk
            if emitted:
                return
            raise RuntimeError("OpenRouter trả về rỗng.")
        except RuntimeError as exc:
            last_error = exc
            failed_models.append(model_id)
            continue

    tried = ", ".join(failed_models or models_to_try)
    raise RuntimeError(
        "Tất cả model OpenRouter đều thất bại. "
        f"Models tried: {tried}. Lỗi cuối: {last_error}"
    )


def call_openrouter_chat(
    prompt: str,
    system_prompt: str | None = None,
    api_key: str | None = None,
    models: list[str] | None = None,
    *,
    stream: bool = True,
) -> str:
    if not stream:
        return _call_openrouter_chat_non_stream(prompt, system_prompt, api_key=api_key, models=models)
    return _collect_stream(call_openrouter_chat_stream(prompt, system_prompt, api_key=api_key, models=models))


def call_llm_chat(
    prompt: str,
    system_prompt: str | None = None,
    backend: Backend = "ollama",
    model: str | None = None,
    api_key: str | None = None,
    agent_type: str = "",
) -> str:
    if backend == "openrouter":
        from testgen.core.config import FALLBACK_MODELS
        fallback_models = FALLBACK_MODELS.get(agent_type, ["openai/gpt-oss-120b:free"])
        selected_model = (model or "").strip()
        models = (
            [selected_model, *[item for item in fallback_models if item != selected_model]]
            if selected_model
            else fallback_models
        )
        return call_openrouter_chat(prompt, system_prompt, api_key=api_key, models=models)
    if backend == "gemini":
        return call_gemini_chat(prompt, system_prompt=system_prompt, model=model, api_key=api_key)
    return call_ollama_chat(prompt, system_prompt=system_prompt, model=model)


def get_ollama_embedding(text: str) -> list[float]:
    payload = {
        "model": EMBED_MODEL,
        "prompt": text,
    }
    body = _post_json(OLLAMA_EMBED_URL, payload, timeout=60)
    embedding = body.get("embedding")
    if not isinstance(embedding, list):
        raise RuntimeError("Phản hồi embedding của Ollama thiếu vector embedding.")
    return _to_float_list(
        embedding,
        "Phản hồi embedding của Ollama chứa giá trị không phải số.",
    )


def get_ollama_embeddings_batch(texts: list[str]) -> list[list[float]]:
    payload = {
        "model": EMBED_MODEL,
        "input": texts,
    }
    body = _post_json(OLLAMA_EMBED_BATCH_URL, payload, timeout=120)
    embeddings = body.get("embeddings")
    if not isinstance(embeddings, list):
        raise RuntimeError("Phản hồi batch embedding của Ollama thiếu danh sách vector.")
    
    result = []
    for emb in embeddings:
        if not isinstance(emb, list):
             raise RuntimeError("Phản hồi batch embedding của Ollama chứa giá trị không hợp lệ.")
        result.append(_to_float_list(emb, "Phản hồi batch embedding chứa giá trị không phải số."))
    return result


def _extract_gemini_embedding_values(body: dict[str, Any]) -> list[Any] | None:
    embedding = body.get("embedding")
    if isinstance(embedding, dict) and isinstance(embedding.get("values"), list):
        return embedding["values"]

    embeddings = body.get("embeddings")
    if isinstance(embeddings, list) and embeddings:
        first = embeddings[0]
        if isinstance(first, dict) and isinstance(first.get("values"), list):
            return first["values"]
    return None


def get_gemini_embedding(
    text: str,
    api_key: str | None = None,
    model: str | None = None,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[float]:
    key = _require_gemini_key(api_key)
    model_name = model or GEMINI_EMBED_MODEL
    payload: dict[str, Any] = {
        "content": {"parts": [{"text": text}]},
    }
    if task_type:
        payload["task_type"] = task_type

    body = _post_json(
        GEMINI_EMBED_URL.format(model=model_name),
        payload,
        timeout=60,
        headers=_gemini_headers(key),
    )
    values = _extract_gemini_embedding_values(body)
    if values is None:
        raise RuntimeError("Phản hồi embedding của Gemini thiếu vector embedding.")
    return _to_float_list(
        values,
        "Phản hồi embedding của Gemini chứa giá trị không phải số.",
    )


def get_embedding(text: str, backend: Backend = "ollama", api_key: str | None = None) -> list[float]:
    if backend == "gemini":
        return get_gemini_embedding(text, api_key=api_key)
    return get_ollama_embedding(text)


def get_embedding_batch(texts: list[str], backend: Backend = "ollama", api_key: str | None = None) -> list[list[float]]:
    if backend == "gemini":
        # Fallback to sequential for Gemini until we implement batching for it
        return [get_gemini_embedding(text, api_key=api_key) for text in texts]
    return get_ollama_embeddings_batch(texts)


def _extract_gemini_text(body: dict[str, Any]) -> str:
    candidates = body.get("candidates")
    if isinstance(candidates, list):
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            content = candidate.get("content")
            if not isinstance(content, dict):
                continue
            parts = content.get("parts")
            if not isinstance(parts, list):
                continue
            texts = [
                str(text).strip()
                for part in parts
                if isinstance(part, dict)
                for text in [part.get("text")]
                if isinstance(text, str) and text.strip()
            ]
            if texts:
                return "\n".join(texts).strip()

    text = body.get("text")
    if isinstance(text, str) and text.strip():
        return text.strip()
    raise RuntimeError("Phản hồi Gemini thiếu văn bản.")
