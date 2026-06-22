from testgen.core.config import (
    GEMINI_CODE_GENERATOR_MODEL,
    GEMINI_CODE_REVIEW_MODEL,
    GEMINI_EMBED_MODEL,
    GEMINI_REQUIREMENT_MODEL,
    GEMINI_TEST_PLANNING_MODEL,
    OLLAMA_CODE_GENERATOR_MODEL,
    OLLAMA_CODE_REVIEW_MODEL,
    OLLAMA_REQUIREMENT_MODEL,
    OLLAMA_TEST_PLANNING_MODEL,
    OLLAMA_MODEL_OPTIONS,
    EMBED_MODEL,
    FALLBACK_MODELS,
    OPENROUTER_MODEL_OPTIONS,
)

FRAMEWORK_OPTIONS = [
    ("Pytest", "pytest"),
    ("JUnit", "JUnit"),
    ("Selenium", "Selenium"),
    ("Playwright", "Playwright"),
    ("Jest", "Jest"),
    ("Postman / Newman", "Postman script"),
]
FRAMEWORK_LOOKUP = {label: value for label, value in FRAMEWORK_OPTIONS}

MODE_OPTIONS = ["API key", "Local AI", "OpenRouter API Key"]
RAG_WORKFLOW = "rag_docs"
GENERATE_WORKFLOW = "generate_tests"
REVIEW_WORKFLOW = "review_tests"
HISTORY_WORKFLOW = "run_history"
PRIVACY_WORKFLOW = "privacy_cleanup"
WORKFLOW_OPTIONS = [RAG_WORKFLOW, GENERATE_WORKFLOW, REVIEW_WORKFLOW, HISTORY_WORKFLOW, PRIVACY_WORKFLOW]
WORKFLOW_LABELS = {
    RAG_WORKFLOW: "Quản lý tài liệu",
    GENERATE_WORKFLOW: "Sinh mã kiểm thử",
    REVIEW_WORKFLOW: "Rà soát test code",
    HISTORY_WORKFLOW: "Lịch sử chạy",
    PRIVACY_WORKFLOW: "Quản lý dữ liệu",
}
LEGACY_WORKFLOW_LOOKUP = {label: value for value, label in WORKFLOW_LABELS.items()}
WORKFLOW_LABEL_OPTIONS = list(WORKFLOW_LABELS.values())
WORKFLOW_WIDGET_KEY = "workflow_choice_label_v3"
TEST_TECHNIQUE_OPTIONS = ["Hybrid", "Black-box", "White-box"]
CODE_FILE_TYPES = [
    "txt", "py", "js", "ts", "jsx", "tsx", "java", "kt", "cs", "go",
    "rb", "php", "html", "css", "json", "xml", "yaml", "yml", "md",
]

def _openrouter_default_model(agent_type: str) -> str:
    models = FALLBACK_MODELS.get(agent_type, [])
    return models[0] if models else "openai/gpt-oss-120b:free"

def profile_for_mode(mode: str) -> dict[str, str]:
    if mode == "OpenRouter API Key":
        return {
            "backend": "openrouter",
            "mode_label": "OpenRouter / Multi-model",
            "requirement_model": _openrouter_default_model("requirement"),
            "planning_model": _openrouter_default_model("test_planner"),
            "generator_model": _openrouter_default_model("code_generator"),
            "review_model": _openrouter_default_model("code_reviewer"),
            "embed_model": EMBED_MODEL,
            "embedding_backend": "ollama",
        }
    if mode == "API key":
        return {
            "backend": "gemini",
            "mode_label": "API key / Gemini",
            "requirement_model": GEMINI_REQUIREMENT_MODEL,
            "planning_model": GEMINI_TEST_PLANNING_MODEL,
            "generator_model": GEMINI_CODE_GENERATOR_MODEL,
            "review_model": GEMINI_CODE_REVIEW_MODEL,
            "embed_model": GEMINI_EMBED_MODEL,
            "embedding_backend": "gemini",
        }
    return {
        "backend": "ollama",
        "mode_label": "Local AI / Ollama",
        "requirement_model": OLLAMA_REQUIREMENT_MODEL,
        "planning_model": OLLAMA_TEST_PLANNING_MODEL,
        "generator_model": OLLAMA_CODE_GENERATOR_MODEL,
        "review_model": OLLAMA_CODE_REVIEW_MODEL,
        "embed_model": EMBED_MODEL,
        "embedding_backend": "ollama",
    }

def workflow_label(workflow: str) -> str:
    return WORKFLOW_LABELS.get(workflow, workflow)
