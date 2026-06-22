from __future__ import annotations

from testgen.core import constants


def test_openrouter_profile_uses_local_embedding_backend():
    profile = constants.profile_for_mode("OpenRouter")

    assert profile["backend"] == "openrouter"
    assert profile["embedding_backend"] == "ollama"
    assert profile["embed_model"] == constants.EMBED_MODEL


def test_ollama_profile_uses_multi_model_defaults():
    profile = constants.profile_for_mode("Multi-agent")
    agent_models = {
        profile["requirement_model"],
        profile["planning_model"],
        profile["generator_model"],
        profile["review_model"],
    }

    assert profile["backend"] == "ollama"
    assert len(agent_models) >= 3
    assert profile["generator_model"] == constants.OLLAMA_CODE_GENERATOR_MODEL
