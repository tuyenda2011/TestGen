from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

OLLAMA_CHAT_URL = os.environ.get("OLLAMA_CHAT_URL", "http://localhost:11434/api/chat")
OLLAMA_EMBED_URL = os.environ.get("OLLAMA_EMBED_URL", "http://localhost:11434/api/embeddings")
OLLAMA_EMBED_BATCH_URL = os.environ.get("OLLAMA_EMBED_BATCH_URL", "http://localhost:11434/api/embed")
GEMINI_CHAT_URL = os.environ.get("GEMINI_CHAT_URL", "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent")
GEMINI_EMBED_URL = os.environ.get("GEMINI_EMBED_URL", "https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent")
OPENROUTER_CHAT_URL = os.environ.get("OPENROUTER_CHAT_URL", "https://openrouter.ai/api/v1/chat/completions")

FALLBACK_MODELS = {
    "requirement": [
        "nex-agi/nex-n2-pro:free",
        "openai/gpt-oss-120b:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ],
    "test_planner": [
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "openai/gpt-oss-120b:free",
        "qwen/qwen3-coder:free",
    ],
    "code_generator": [
        "poolside/laguna-m.1:free",
        "openai/gpt-oss-120b:free",
        "poolside/laguna-xs.2:free",
        "qwen/qwen3-coder:free",
    ],
    "code_reviewer": [
        "openai/gpt-oss-120b:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "qwen/qwen3-coder:free",
    ],
    "failure_analyzer": [
        "openai/gpt-oss-120b:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
    ],
}

_OPENROUTER_EXTRA_MODELS = [
    model.strip()
    for model in os.environ.get("OPENROUTER_MODEL_OPTIONS", "").split(",")
    if model.strip()
]
OPENROUTER_MODEL_OPTIONS = list(
    dict.fromkeys(
        [
            *_OPENROUTER_EXTRA_MODELS,
            *[model for models in FALLBACK_MODELS.values() for model in models],
        ]
    )
)

OLLAMA_REQUIREMENT_MODEL = os.environ.get("OLLAMA_REQUIREMENT_MODEL", "qwen2.5:7b")
OLLAMA_TEST_PLANNING_MODEL = os.environ.get("OLLAMA_TEST_PLANNING_MODEL", "llama3.1:8b")
OLLAMA_CODE_GENERATOR_MODEL = os.environ.get("OLLAMA_CODE_GENERATOR_MODEL", "qwen2.5-coder:7b")
OLLAMA_CODE_REVIEW_MODEL = os.environ.get("OLLAMA_CODE_REVIEW_MODEL", "deepseek-coder:6.7b")
_OLLAMA_EXTRA_MODELS = [
    model.strip()
    for model in os.environ.get("OLLAMA_MODEL_OPTIONS", "").split(",")
    if model.strip()
]
OLLAMA_MODEL_OPTIONS = list(
    dict.fromkeys(
        [
            *_OLLAMA_EXTRA_MODELS,
            OLLAMA_REQUIREMENT_MODEL,
            OLLAMA_TEST_PLANNING_MODEL,
            OLLAMA_CODE_GENERATOR_MODEL,
            OLLAMA_CODE_REVIEW_MODEL,
            "qwen2.5:7b",
            "llama3.1:8b",
            "qwen2.5-coder:7b",
            "deepseek-coder:6.7b",
            "mistral:7b",
        ]
    )
)

GEMINI_REQUIREMENT_MODEL = os.environ.get("GEMINI_REQUIREMENT_MODEL", "gemini-2.0-flash")
GEMINI_TEST_PLANNING_MODEL = os.environ.get("GEMINI_TEST_PLANNING_MODEL", "gemini-2.0-flash")
GEMINI_CODE_GENERATOR_MODEL = os.environ.get("GEMINI_CODE_GENERATOR_MODEL", "gemini-2.0-flash")
GEMINI_CODE_REVIEW_MODEL = os.environ.get("GEMINI_CODE_REVIEW_MODEL", "gemini-2.0-flash")
GEMINI_EMBED_MODEL = os.environ.get("GEMINI_EMBED_MODEL", "gemini-embedding-001")

REQUIREMENT_MODEL = os.environ.get("REQUIREMENT_MODEL", OLLAMA_REQUIREMENT_MODEL)
TEST_PLANNING_MODEL = os.environ.get("TEST_PLANNING_MODEL", OLLAMA_TEST_PLANNING_MODEL)
CODE_GENERATOR_MODEL = os.environ.get("CODE_GENERATOR_MODEL", OLLAMA_CODE_GENERATOR_MODEL)
CODE_REVIEW_MODEL = os.environ.get("CODE_REVIEW_MODEL", OLLAMA_CODE_REVIEW_MODEL)
MAIN_MODEL = os.environ.get("MAIN_MODEL", OLLAMA_CODE_GENERATOR_MODEL)
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text")
NUM_CTX = int(os.environ.get("NUM_CTX", 32768))
TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.1))
NUM_PREDICT = int(os.environ.get("NUM_PREDICT", 8192))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 1200))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 150))
TOP_K = int(os.environ.get("TOP_K", 8))
REQUIREMENT_CONTEXT_BUDGET = int(os.environ.get("REQUIREMENT_CONTEXT_BUDGET", 9000))
PLANNING_CONTEXT_BUDGET = int(os.environ.get("PLANNING_CONTEXT_BUDGET", 8000))
GENERATION_CONTEXT_BUDGET = int(os.environ.get("GENERATION_CONTEXT_BUDGET", 8000))
REVIEW_CONTEXT_BUDGET = int(os.environ.get("REVIEW_CONTEXT_BUDGET", 8000))
PYTEST_COVERAGE_THRESHOLD = float(os.environ.get("PYTEST_COVERAGE_THRESHOLD", 100.0))
PYTEST_MAX_ATTEMPTS = int(os.environ.get("PYTEST_MAX_ATTEMPTS", 3))
PYTEST_FUNCTION_BATCH_SIZE = int(os.environ.get("PYTEST_FUNCTION_BATCH_SIZE", 4))
PIPELINE_MAX_WORKERS = int(os.environ.get("PIPELINE_MAX_WORKERS", 2))
GENERATOR_MAX_WORKERS = int(os.environ.get("GENERATOR_MAX_WORKERS", 5))

OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "outputs")
RUNTIME_DIR = os.environ.get("RUNTIME_DIR", ".runtime")

OUTPUT_PATH = BASE_DIR / OUTPUT_DIR
OUTPUT_RUNS_PATH = OUTPUT_PATH / "runs"
PROMPTS_PATH = Path(__file__).resolve().parents[1] / "prompts"
RUNTIME_PATH = BASE_DIR / RUNTIME_DIR
CHROMA_PATH = RUNTIME_PATH / "chroma"
DOC_UPLOAD_PATH = RUNTIME_PATH / "uploaded_docs"
DOC_COLLECTION_NAME = os.environ.get("DOC_COLLECTION_NAME", "testgen_chatbot_documents")
SOURCE_COLLECTION_NAME = os.environ.get("SOURCE_COLLECTION_NAME", "testgen_chatbot_source_code")
COLLECTION_NAME = DOC_COLLECTION_NAME
