from __future__ import annotations

from testgen.core.config import (
    EMBED_MODEL,
    OLLAMA_CODE_GENERATOR_MODEL,
    OLLAMA_CODE_REVIEW_MODEL,
    OLLAMA_REQUIREMENT_MODEL,
    OLLAMA_TEST_PLANNING_MODEL,
)


def _unique_ordered(values: list[str]) -> list[str]:
    unique: list[str] = []
    for value in values:
        cleaned = (value or "").strip()
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
    return unique


def ollama_model_names(models: list[str] | None = None) -> list[str]:
    if models is not None:
        return _unique_ordered(models)
    return _unique_ordered(
        [
            OLLAMA_REQUIREMENT_MODEL,
            OLLAMA_TEST_PLANNING_MODEL,
            OLLAMA_CODE_GENERATOR_MODEL,
            OLLAMA_CODE_REVIEW_MODEL,
            EMBED_MODEL,
        ]
    )


def ollama_pull_commands(models: list[str] | None = None) -> list[str]:
    return [f"ollama pull {model_name}" for model_name in ollama_model_names(models)]
