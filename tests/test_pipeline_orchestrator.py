from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from testgen import pipeline_orchestrator
from testgen.pipeline import stages as pipeline_stages
from testgen.pipeline_orchestrator import _emit_progress, run_pipeline


# ── Helper profile & helpers fixtures ──

def _make_profile(backend="ollama"):
    return {
        "backend": backend,
        "mode_label": f"Test / {backend}",
        "requirement_model": "test-req",
        "planning_model": "test-plan",
        "generator_model": "test-gen",
        "review_model": "test-review",
        "embed_model": "test-embed",
        "embedding_backend": "ollama" if backend == "openrouter" else backend,
    }


def _make_helpers():
    return {
        "_normalize_text": lambda x: (x or "").strip(),
        "_clip_text": lambda x, n: (x or "")[:n],
        "_combine_sections": lambda loaded, pasted, label: loaded + ([(label, pasted)] if (pasted or "").strip() else []),
        "_build_rag_context": lambda *a, **kw: ("rag context", 5, False),
        "_retrieve_preindexed_rag_context": lambda *a, **kw: ("preindexed context", True),
        "_collection_count": lambda name: 10,
        "_merge_contexts": lambda a, b: f"{a}\n\n{b}".strip(),
        "_workflow_label": lambda w: f"Label({w})",
        "_python_source_for_generation": lambda sections: "\n\n".join(text for _, text in sections),
        "DOC_COLLECTION_NAME": "test_docs",
        "SOURCE_COLLECTION_NAME": "test_source",
    }


# ── _emit_progress ──

def test_emit_progress_appends_item():
    progress = []
    _emit_progress(progress, None, "1", "Agent", "model", "OK", "Done")
    assert len(progress) == 1
    assert progress[0]["step"] == "1"
    assert progress[0]["agent"] == "Agent"


def test_emit_progress_calls_callback():
    progress = []
    callback_calls = []
    _emit_progress(progress, lambda item: callback_calls.append(item), "2", "A", "M", "S", "R")
    assert len(callback_calls) == 1
    assert callback_calls[0]["step"] == "2"


def test_emit_progress_no_callback_is_safe():
    progress = []
    _emit_progress(progress, None, "1", "A", "M", "S", "R")
    assert len(progress) == 1


# ── run_pipeline validation errors ──

def test_pipeline_raises_without_gemini_key():
    profile = _make_profile("gemini")
    helpers = _make_helpers()
    with pytest.raises(ValueError, match="API key"):
        run_pipeline(
            requirement_text="", docs_files=[], source_code_text="", source_files=[],
            test_code_text="", test_files=[], retrieval_query="",
            framework="pytest", test_technique="Hybrid",
            workflow_mode="generate_tests", profile=profile, api_key="",
            use_preindexed_docs=False, helpers=helpers,
        )


def test_pipeline_raises_when_nothing_provided():
    profile = _make_profile("ollama")
    helpers = _make_helpers()
    with pytest.raises(ValueError, match="nhập"):
        run_pipeline(
            requirement_text="", docs_files=[], source_code_text="", source_files=[],
            test_code_text="", test_files=[], retrieval_query="",
            framework="pytest", test_technique="Hybrid",
            workflow_mode="generate_tests", profile=profile, api_key="",
            use_preindexed_docs=False, helpers=helpers,
        )


def test_pipeline_review_raises_without_test_code():
    profile = _make_profile("ollama")
    helpers = _make_helpers()
    with pytest.raises(ValueError, match="test code"):
        run_pipeline(
            requirement_text="", docs_files=[], source_code_text="", source_files=[],
            test_code_text="", test_files=[], retrieval_query="",
            framework="pytest", test_technique="Hybrid",
            workflow_mode="review_tests", profile=profile, api_key="",
            use_preindexed_docs=False, helpers=helpers,
        )


# ── run_pipeline review-only mode ──

def test_pipeline_review_only_returns_review_report(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()

    monkeypatch.setattr(pipeline_orchestrator, "review_test_code", lambda *a, **kw: "Review OK")
    monkeypatch.setattr(pipeline_orchestrator, "create_run_id", lambda: "run-001")
    monkeypatch.setattr(pipeline_orchestrator, "save_review_report", lambda report, run_id: "/path/review.pdf")
    monkeypatch.setattr(pipeline_orchestrator, "persist_run_history", lambda **kw: None)
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: None)

    result = run_pipeline(
        requirement_text="", docs_files=[], source_code_text="", source_files=[],
        test_code_text="def test_foo(): pass", test_files=[], retrieval_query="",
        framework="pytest", test_technique="Hybrid",
        workflow_mode="review_tests", profile=profile, api_key="",
        use_preindexed_docs=False, helpers=helpers,
    )

    assert result["review_report"] == "Review OK"
    assert result["workflow"] == "review_tests"
    assert result["generated_code"] == ""
    assert len(result["progress"]) >= 2
    assert {"input", "review", "artifacts"}.issubset(result["diagnostics"]["stage_timings_ms"])


# ── run_pipeline review-only language mismatch ──

def test_pipeline_review_rejects_mismatched_framework(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()

    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: "Mismatch error")

    with pytest.raises(ValueError, match="Mismatch"):
        run_pipeline(
            requirement_text="", docs_files=[], source_code_text="", source_files=[],
            test_code_text="public class Test {}", test_files=[], retrieval_query="",
            framework="pytest", test_technique="Hybrid",
            workflow_mode="review_tests", profile=profile, api_key="",
            use_preindexed_docs=False, helpers=helpers,
        )


# ── run_pipeline generate mode (no pytest execution) ──

def test_pipeline_generate_non_pytest_returns_code(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()
    captured_models = {}

    def fake_analyze_requirements(*args, **kwargs):
        captured_models["requirement"] = kwargs.get("model")
        return '{"module": "test"}'

    def fake_generate_test_plan(*args, **kwargs):
        captured_models["planning"] = kwargs.get("model")
        return '{"test_scenarios": []}'

    def fake_generate_test_code(*args, **kwargs):
        captured_models["generator"] = kwargs.get("model")
        return "test('ok', () => {});"

    def fake_review_test_code(*args, **kwargs):
        captured_models["review"] = kwargs.get("model")
        return "Review report"

    monkeypatch.setattr(pipeline_orchestrator, "create_run_id", lambda: "run-002")
    monkeypatch.setattr(pipeline_orchestrator, "load_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: None)
    monkeypatch.setattr(pipeline_orchestrator, "retrieve_context", lambda *a, **kw: "")
    monkeypatch.setattr(pipeline_orchestrator, "analyze_requirements", fake_analyze_requirements)
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_plan", fake_generate_test_plan)
    monkeypatch.setattr(pipeline_orchestrator, "parse_test_plan_rows", lambda x: [])
    monkeypatch.setattr(pipeline_orchestrator, "estimate_test_generation_llm_calls", lambda fw, src: 1)
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_code", fake_generate_test_code)
    monkeypatch.setattr(pipeline_orchestrator, "review_test_code", fake_review_test_code)
    monkeypatch.setattr(pipeline_orchestrator, "save_generated_code", lambda code, fw, run_id: "/code.js")
    monkeypatch.setattr(pipeline_orchestrator, "save_test_plan_excel", lambda plan, run_id: "/plan.xlsx")
    monkeypatch.setattr(pipeline_orchestrator, "save_review_report", lambda report, run_id: "/review.pdf")
    monkeypatch.setattr(pipeline_orchestrator, "persist_run_history", lambda **kw: None)
    monkeypatch.setattr(pipeline_stages, "get_test_executor", lambda framework, **kwargs: None)

    result = run_pipeline(
        requirement_text="Test authentication",
        docs_files=[], source_code_text="", source_files=[],
        test_code_text="", test_files=[], retrieval_query="auth tests",
        framework="Jest", test_technique="Black-box",
        workflow_mode="generate_tests", profile=profile, api_key="",
        use_preindexed_docs=False, helpers=helpers,
    )

    assert result["generated_code"] == "test('ok', () => {});"
    assert result["review_report"] == "Review report"
    assert result["framework"] == "Jest"
    assert result["run_id"] == "run-002"
    assert len(result["progress"]) >= 4
    assert {
        "input",
        "rag",
        "requirement",
        "planning",
        "generation",
        "execution",
        "review",
        "artifacts",
    }.issubset(result["diagnostics"]["stage_timings_ms"])
    assert captured_models == {
        "requirement": "test-req",
        "planning": "test-plan",
        "generator": "test-gen",
        "review": "test-review",
    }


# ── run_pipeline generate mode with pytest execution (pass on first try) ──

def test_pipeline_generate_pytest_passes_first_attempt(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()

    monkeypatch.setattr(pipeline_orchestrator, "create_run_id", lambda: "run-003")
    monkeypatch.setattr(pipeline_orchestrator, "load_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: None)
    monkeypatch.setattr(pipeline_orchestrator, "retrieve_context", lambda *a, **kw: "")
    monkeypatch.setattr(pipeline_orchestrator, "analyze_requirements", lambda *a, **kw: '{"module": "calc"}')
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_plan", lambda *a, **kw: '{"test_scenarios": []}')
    monkeypatch.setattr(pipeline_orchestrator, "parse_test_plan_rows", lambda x: [{"id": "TC-001"}])
    monkeypatch.setattr(pipeline_orchestrator, "estimate_test_generation_llm_calls", lambda fw, src: 1)
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_code", lambda *a, **kw: "def test_add(): assert 1+1==2")
    monkeypatch.setattr(
        pipeline_orchestrator, "run_generated_pytest_with_coverage",
        lambda **kw: {"passed": True, "coverage_percent": 95.0, "missing_lines": [], "output": "ok", "diagnosis": "", "failure_summary": ""},
    )
    monkeypatch.setattr(pipeline_orchestrator, "execution_result_score", lambda summary, threshold: (1, 1, 95.0))
    monkeypatch.setattr(pipeline_orchestrator, "review_test_code", lambda *a, **kw: "Review")
    monkeypatch.setattr(pipeline_orchestrator, "save_generated_code", lambda code, fw, run_id: "/code.py")
    monkeypatch.setattr(pipeline_orchestrator, "save_test_plan_excel", lambda plan, run_id: "/plan.xlsx")
    monkeypatch.setattr(pipeline_orchestrator, "save_review_report", lambda report, run_id: "/review.pdf")
    monkeypatch.setattr(pipeline_orchestrator, "persist_run_history", lambda **kw: None)

    result = run_pipeline(
        requirement_text="test calc",
        docs_files=[], source_code_text="def add(a,b): return a+b", source_files=[],
        test_code_text="", test_files=[], retrieval_query="calc",
        framework="pytest", test_technique="White-box",
        workflow_mode="generate_tests", profile=profile, api_key="",
        use_preindexed_docs=False, helpers=helpers,
    )

    assert result["diagnostics"]["pytest_passed"] is True
    assert result["diagnostics"]["pytest_coverage_percent"] == 95.0
    assert result["diagnostics"]["attempts"] == 1


# ── run_pipeline generate pytest fails all attempts ──

def test_pipeline_generate_pytest_fails_raises_value_error(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()

    monkeypatch.setattr(pipeline_orchestrator, "create_run_id", lambda: "run-004")
    monkeypatch.setattr(pipeline_orchestrator, "load_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: None)
    monkeypatch.setattr(pipeline_orchestrator, "retrieve_context", lambda *a, **kw: "")
    monkeypatch.setattr(pipeline_orchestrator, "analyze_requirements", lambda *a, **kw: '{}')
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_plan", lambda *a, **kw: '{}')
    monkeypatch.setattr(pipeline_orchestrator, "parse_test_plan_rows", lambda x: [])
    monkeypatch.setattr(pipeline_orchestrator, "estimate_test_generation_llm_calls", lambda fw, src: 1)
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_code", lambda *a, **kw: "def test_x(): pass")
    monkeypatch.setattr(
        pipeline_orchestrator, "run_generated_pytest_with_coverage",
        lambda **kw: {"passed": False, "coverage_percent": 30.0, "missing_lines": [5, 6], "output": "FAILED", "diagnosis": "assertion error", "failure_summary": "1 failed"},
    )
    monkeypatch.setattr(pipeline_orchestrator, "execution_result_score", lambda summary, threshold: (0, 0, 30.0))

    with pytest.raises(ValueError, match="Từ chối xuất"):
        run_pipeline(
            requirement_text="test",
            docs_files=[], source_code_text="def f(): return 1", source_files=[],
            test_code_text="", test_files=[], retrieval_query="test",
            framework="pytest", test_technique="Hybrid",
            workflow_mode="generate_tests", profile=profile, api_key="",
            use_preindexed_docs=False, helpers=helpers,
        )


# ── run_pipeline with RAG docs ──

def test_pipeline_with_docs_creates_rag_context(monkeypatch):
    profile = _make_profile("openrouter")
    helpers = _make_helpers()
    captured_rag = {}

    def fake_build_rag_context(*args, **kwargs):
        captured_rag["embedding_backend"] = args[4]
        return "rag context", 5, False, "docs-signature"

    helpers["_build_rag_context"] = fake_build_rag_context

    monkeypatch.setattr(pipeline_orchestrator, "create_run_id", lambda: "run-005")
    monkeypatch.setattr(pipeline_orchestrator, "load_uploaded_file_entries", lambda files: [("doc.pdf", "doc content")])
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: None)
    monkeypatch.setattr(pipeline_orchestrator, "analyze_requirements", lambda *a, **kw: '{}')
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_plan", lambda *a, **kw: '{}')
    monkeypatch.setattr(pipeline_orchestrator, "parse_test_plan_rows", lambda x: [])
    monkeypatch.setattr(pipeline_orchestrator, "estimate_test_generation_llm_calls", lambda fw, src: 1)
    monkeypatch.setattr(pipeline_orchestrator, "generate_test_code", lambda *a, **kw: "test code")
    monkeypatch.setattr(pipeline_orchestrator, "review_test_code", lambda *a, **kw: "review")
    monkeypatch.setattr(pipeline_orchestrator, "save_generated_code", lambda code, fw, run_id: "/c")
    monkeypatch.setattr(pipeline_orchestrator, "save_test_plan_excel", lambda plan, run_id: "/p")
    monkeypatch.setattr(pipeline_orchestrator, "save_review_report", lambda report, run_id: "/r")
    monkeypatch.setattr(pipeline_orchestrator, "persist_run_history", lambda **kw: None)
    monkeypatch.setattr(pipeline_stages, "get_test_executor", lambda framework, **kwargs: None)

    result = run_pipeline(
        requirement_text="test auth",
        docs_files=["doc1.pdf"], source_code_text="", source_files=[],
        test_code_text="", test_files=[], retrieval_query="auth",
        framework="Jest", test_technique="Black-box",
        workflow_mode="generate_tests", profile=profile, api_key="openrouter-key",
        use_preindexed_docs=False, helpers=helpers,
    )

    assert result["docs_context"] == "rag context"
    assert result["diagnostics"]["docs_chunks_indexed"] == 5
    assert result["embedding_backend"] == "ollama"
    assert captured_rag["embedding_backend"] == "ollama"


# ── run_pipeline source code framework mismatch ──

def test_pipeline_source_framework_mismatch_raises(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()

    monkeypatch.setattr(pipeline_orchestrator, "load_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: "Language mismatch!")

    with pytest.raises(ValueError, match="Language mismatch"):
        run_pipeline(
            requirement_text="test",
            docs_files=[], source_code_text="public class Calc {}", source_files=[],
            test_code_text="", test_files=[], retrieval_query="test",
            framework="pytest", test_technique="Hybrid",
            workflow_mode="generate_tests", profile=profile, api_key="",
            use_preindexed_docs=False, helpers=helpers,
        )


# ── run_pipeline persist_run_history OSError is silently caught ──

def test_pipeline_review_survives_persist_failure(monkeypatch):
    profile = _make_profile("ollama")
    helpers = _make_helpers()

    monkeypatch.setattr(pipeline_orchestrator, "review_test_code", lambda *a, **kw: "Review")
    monkeypatch.setattr(pipeline_orchestrator, "create_run_id", lambda: "run-006")
    monkeypatch.setattr(pipeline_orchestrator, "save_review_report", lambda report, run_id: "/review.pdf")
    monkeypatch.setattr(pipeline_orchestrator, "persist_run_history", MagicMock(side_effect=OSError("disk full")))
    monkeypatch.setattr(pipeline_orchestrator, "load_text_uploaded_file_entries", lambda files: [])
    monkeypatch.setattr(pipeline_orchestrator, "validate_framework_sections", lambda fw, sec: None)

    result = run_pipeline(
        requirement_text="", docs_files=[], source_code_text="", source_files=[],
        test_code_text="def test(): pass", test_files=[], retrieval_query="",
        framework="pytest", test_technique="Hybrid",
        workflow_mode="review_tests", profile=profile, api_key="",
        use_preindexed_docs=False, helpers=helpers,
    )

    assert result["review_report"] == "Review"
