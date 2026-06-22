from __future__ import annotations

from testgen.core.models import PipelineInput, PipelineProfile
from testgen.executors.base import TestExecutionOutcome
from testgen.pipeline import stages as pipeline_stages
from testgen.pipeline.stages import (
    ArtifactStage,
    ExecutionStageOutput,
    ExecutionStage,
    GenerationStageOutput,
    InputStage,
    InputStageOutput,
    PlanningStageOutput,
    PipelineDependencies,
    PipelineRunContext,
    RagStage,
    RequirementStage,
    RequirementStageOutput,
    ReviewStageOutput,
    emit_progress,
)


def _noop(*args, **kwargs):
    return ""


def _make_deps() -> PipelineDependencies:
    return PipelineDependencies(
        create_run_id=lambda: "run-stage",
        emit_progress=emit_progress,
        normalize_text=lambda text: (text or "").strip(),
        clip_text=lambda text, max_chars: (text or "")[:max_chars],
        combine_sections=lambda loaded, pasted, label: loaded + ([(label, pasted.strip())] if (pasted or "").strip() else []),
        load_uploaded_file_entries=lambda files: [],
        load_text_uploaded_file_entries=lambda files: [],
        validate_framework_sections=lambda framework, sections: None,
        resolve_retrieval_source=lambda **kwargs: kwargs["manual_requirement"] or "source context",
        workflow_label=lambda workflow: workflow,
        build_rag_context=_noop,
        retrieve_preindexed_rag_context=_noop,
        collection_count=lambda name: 0,
        merge_contexts=lambda docs, source: "\n".join(part for part in [docs, source] if part),
        python_source_for_generation=lambda sections: "\n".join(text for _, text in sections),
        analyze_requirements=_noop,
        generate_test_plan=_noop,
        parse_test_plan_rows=lambda text: [],
        estimate_test_generation_llm_calls=lambda framework, source: 1,
        generate_test_code=_noop,
        generate_targeted_pytest_code=_noop,
        heal_pytest_code=_noop,
        generate_targeted_junit_code=_noop,
        review_test_code=_noop,
        save_generated_code=_noop,
        save_test_plan_excel=_noop,
        save_review_report=_noop,
        save_combined_coverage_report=lambda *args, **kwargs: ("", "", ""),
        persist_run_history=lambda **kwargs: None,
        run_generated_pytest_with_coverage=lambda **kwargs: {},
        execution_result_score=lambda summary, threshold: (0, 0, 0.0),
        heal_junit_code=_noop,
    )


def _make_context() -> PipelineRunContext:
    return PipelineRunContext(
        input_data=PipelineInput(
            requirement_text="test calc",
            source_code_text="def add(a, b): return a + b",
            framework="pytest",
            workflow_mode="generate_tests",
        ),
        profile=PipelineProfile(
            backend="ollama",
            mode_label="test",
            requirement_model="req",
            planning_model="plan",
            generator_model="gen",
            review_model="review",
            embed_model="embed",
            embedding_backend="ollama",
        ),
        run_id="run-stage",
        backend="ollama",
        embedding_backend="ollama",
        embedding_label="embed (ollama)",
        diagnostics={},
    )


def test_input_stage_returns_dataclass_and_progress():
    ctx = _make_context()
    result = InputStage(_make_deps()).run(ctx)

    assert isinstance(result, InputStageOutput)
    assert result.has_source is True
    assert result.source_sections == [("Dán source code", "def add(a, b): return a + b")]
    assert result.retrieval_source == "test calc"
    assert ctx.progress[0]["agent"] == "Input Loader"


def test_rag_stage_records_missing_preindexed_collection():
    deps = _make_deps()
    deps.retrieve_preindexed_rag_context = lambda *args, **kwargs: (
        "",
        False,
        {
            "top_k_requested": 4,
            "returned_chunks": 0,
            "sources": [],
            "skipped_reason": "preindexed_collection_missing",
            "collection_name": "docs",
        },
    )
    ctx = _make_context()
    ctx.input_data.use_preindexed_docs = True
    ctx.diagnostics = {
        "rag_reused_collections": 0,
        "docs_chunks_indexed": 0,
        "source_chunks_indexed": 0,
    }

    result = RagStage(deps).run(
        ctx,
        InputStageOutput(
            manual_requirement="query",
            docs_sections=[("__preindexed_docs__", "ready")],
            source_sections=[],
            test_sections=[],
            has_docs=True,
            has_source=False,
            has_test_code=False,
            review_only_mode=False,
            retrieval_source="query",
        ),
    )

    assert result.docs_context == ""
    assert ctx.diagnostics["rag_retrieval"]["docs"]["skipped_reason"] == "preindexed_collection_missing"
    assert ctx.progress[-1]["agent"] == "RAG Retriever + Embedding + Vector DB"


def test_requirement_stage_builds_java_ast_context():
    deps = _make_deps()
    deps.analyze_requirements = lambda *args, **kwargs: '{"ok": true}'
    ctx = _make_context()
    ctx.input_data.framework = "JUnit"
    ctx.diagnostics = {"llm_calls_estimated": 0}

    result = RequirementStage(deps).run(
        ctx,
        InputStageOutput(
            manual_requirement="test calc",
            docs_sections=[],
            source_sections=[
                (
                    "Calculator.java",
                    "public class Calculator { int add(int a, int b) { return a + b; } }",
                )
            ],
            test_sections=[],
            has_docs=False,
            has_source=True,
            has_test_code=False,
            review_only_mode=False,
            retrieval_source="test calc",
        ),
        pipeline_stages.RagStageOutput(
            docs_context="",
            source_context="",
            context="",
            docs_new_signature="",
            source_new_signature="",
            used_preindexed_docs=False,
        ),
    )

    assert result.requirement_json == '{"ok": true}'
    assert "TREE-SITTER" in result.ast_context
    assert "java_method" in result.ast_context
    assert "add" in result.ast_context


def test_artifact_stage_records_save_failure_and_persists_history():
    deps = _make_deps()
    persisted = {}

    def fail_save_code(*args, **kwargs):
        raise OSError("disk full")

    deps.save_generated_code = fail_save_code
    deps.save_test_plan_excel = lambda *args, **kwargs: "/tmp/plan.xlsx"
    deps.save_review_report = lambda *args, **kwargs: ("/tmp/review.pdf", "/tmp/review.md")
    deps.save_combined_coverage_report = lambda *args, **kwargs: ("/tmp/coverage.md", "/tmp/coverage.json", "")
    deps.persist_run_history = lambda **kwargs: persisted.update(kwargs)
    ctx = _make_context()
    ctx.diagnostics = {}

    artifacts = ArtifactStage(deps).save_generated(
        ctx,
        PlanningStageOutput(test_plan_json="{}", test_case_rows=[]),
        ExecutionStageOutput(
            generated_code="def test_ok():\n    assert True",
            execution_summary={
                "pytest_log_path": "/tmp/pytest.log",
                "collection_log_path": "/tmp/collect.log",
            },
        ),
        ReviewStageOutput(review_report="Review", review_target_code="", review_target_label="generated"),
    )

    assert artifacts.code_path == ""
    assert ctx.diagnostics["artifact_errors"][0]["stage"] == "generated_code"
    assert persisted["diagnostics"]["artifact_errors"][0]["error"] == "disk full"
    assert persisted["pytest_log_path"] == "/tmp/pytest.log"


def test_execution_stage_runs_external_executor_once_without_pytest_gate(monkeypatch):
    class FakeExternalExecutor:
        framework = "Jest"
        display_name = "Jest"

        def execute(self, request):
            return TestExecutionOutcome(
                framework=self.framework,
                summary={
                    "passed": True,
                    "coverage_percent": 90.0,
                    "coverage_supported": True,
                    "coverage_available": True,
                    "coverage_status": "success",
                    "retry_supported": False,
                    "command_text": "npx jest --coverage",
                    "execution_issue": {"type": "none"},
                },
            )
        
        def score_result(self, summary, threshold):
            return (1, 1, 90.0)

    monkeypatch.setattr(
        pipeline_stages,
        "get_test_executor",
        lambda framework, **kwargs: FakeExternalExecutor(),
    )
    deps = _make_deps()
    ctx = _make_context()
    ctx.input_data.framework = "Jest"
    ctx.diagnostics = {}

    result = ExecutionStage(deps).run(
        ctx,
        RequirementStageOutput(requirement_json="{}", ast_context="", python_source_text="def add(a, b): return a + b"),
        PlanningStageOutput(test_plan_json="{}", test_case_rows=[]),
        GenerationStageOutput(generated_code="test('x', () => {});", generation_call_count=1),
    )

    assert result.execution_summary["passed"] is True
    assert ctx.diagnostics["test_execution_framework"] == "Jest"
    assert ctx.diagnostics["jest_execution_issue_type"] == "none"
    assert ctx.progress[-1]["agent"] == "Jest Executor"


def test_review_stage_passes_original_source_to_reviewer():
    deps = _make_deps()
    captured = {}

    def fake_review_test_code(*args, **kwargs):
        captured.update(kwargs)
        return "review"

    deps.review_test_code = fake_review_test_code
    ctx = _make_context()
    ctx.diagnostics = {"llm_calls_estimated": 0}

    result = pipeline_stages.ReviewStage(deps).run_generated(
        ctx,
        InputStageOutput(
            manual_requirement="",
            docs_sections=[],
            source_sections=[("order.py", "def total():\n    return 42")],
            test_sections=[],
            has_docs=False,
            has_source=True,
            has_test_code=False,
            review_only_mode=False,
            retrieval_source="",
        ),
        RequirementStageOutput(requirement_json="{}", ast_context="", python_source_text="fallback source"),
        PlanningStageOutput(test_plan_json="{}", test_case_rows=[]),
        ExecutionStageOutput(generated_code="def test_total(): assert total() == 42", execution_summary={}),
    )

    assert result.review_report == "review"
    assert "# Source code: order.py" in captured["source_code_text"]
    assert "def total()" in captured["source_code_text"]
