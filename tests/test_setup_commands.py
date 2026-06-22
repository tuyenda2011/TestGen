from __future__ import annotations

from testgen.core import config
from testgen.core.setup_commands import ollama_model_names, ollama_pull_commands


def test_ollama_pull_commands_follow_config_models():
    commands = ollama_pull_commands()

    assert f"ollama pull {config.OLLAMA_CODE_GENERATOR_MODEL}" in commands
    assert f"ollama pull {config.EMBED_MODEL}" in commands
    assert len(commands) == len(set(commands))


def test_ollama_pull_commands_can_follow_selected_profile_models():
    models = ["qwen2.5:7b", "qwen2.5:7b", "nomic-embed-text"]

    assert ollama_model_names(models) == ["qwen2.5:7b", "nomic-embed-text"]
    assert ollama_pull_commands(models) == [
        "ollama pull qwen2.5:7b",
        "ollama pull nomic-embed-text",
    ]
