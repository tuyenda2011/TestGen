from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import time
from typing import Any, Callable

from testgen.core.config import (
    DOC_COLLECTION_NAME,
    GENERATION_CONTEXT_BUDGET,
    OUTPUT_RUNS_PATH,
    PIPELINE_MAX_WORKERS,
    PYTEST_COVERAGE_THRESHOLD,
    PYTEST_MAX_ATTEMPTS,
    REQUIREMENT_CONTEXT_BUDGET,
    REVIEW_CONTEXT_BUDGET,
    SOURCE_COLLECTION_NAME,
    TOP_K,
)
from testgen.core.constants import REVIEW_WORKFLOW
from testgen.core.models import PipelineInput, PipelineProfile, PipelineCancelledError, PipelineResult
from testgen.executors.base import TestExecutionRequest
from testgen.executors.registry import get_test_executor
from testgen.core.post_review_quality import assess_post_review_quality
from testgen.rag.quality import assess_rag_quality


ProgressCallback = Callable[[dict[str, str]], None] | None


@dataclass
class PipelineDependencies:
    create_run_id: Callable[[], str]
    emit_progress: Callable[..., None]
    normalize_text: Callable[..., str]
    clip_text: Callable[..., str]
    combine_sections: Callable[..., list[tuple[str, str]]]
    load_uploaded_file_entries: Callable[..., list[tuple[str, str]]]
    load_text_uploaded_file_entries: Callable[..., list[tuple[str, str]]]
    validate_framework_sections: Callable[..., str | None]
    resolve_retrieval_source: Callable[..., str]
    workflow_label: Callable[..., str]
    build_rag_context: Callable[..., Any]
    retrieve_preindexed_rag_context: Callable[..., Any]
    collection_count: Callable[..., int]
    merge_contexts: Callable[..., str]
    python_source_for_generation: Callable[..., str]
    analyze_requirements: Callable[..., str]
    generate_test_plan: Callable[..., str]
    parse_test_plan_rows: Callable[..., list[dict[str, str]]]
    estimate_test_generation_llm_calls: Callable[..., int]
    generate_test_code: Callable[..., str]
    generate_targeted_pytest_code: Callable[..., str]
    heal_pytest_code: Callable[..., str]
    generate_targeted_junit_code: Callable[..., str]
    review_test_code: Callable[..., str]
    save_generated_code: Callable[..., str]
    save_test_plan_excel: Callable[..., str]
    save_review_report: Callable[..., Any]
    save_combined_coverage_report: Callable[..., tuple[str, str, str]]
    persist_run_history: Callable[..., Any]
    run_generated_pytest_with_coverage: Callable[..., dict[str, Any]]
    execution_result_score: Callable[..., tuple[int, int, float]]
    generate_targeted_jest_code: Callable[..., str] | None = None
    heal_jest_code: Callable[..., str] | None = None
    heal_junit_code: Callable[..., str] | None = None
    heal_postman_code: Callable[..., str] | None = None
    doc_collection_name: str = DOC_COLLECTION_NAME
    source_collection_name: str = SOURCE_COLLECTION_NAME


@dataclass
class PipelineRunContext:
    input_data: PipelineInput
    profile: PipelineProfile
    run_id: str
    backend: str
    embedding_backend: str
    embedding_label: str
    progress: list[dict[str, str]] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    progress_callback: ProgressCallback = None
    cancel_check: Callable[[], bool] | None = None

    def check_cancelled(self):
        if self.cancel_check and self.cancel_check():
            raise PipelineCancelledError("Tiến trình đã bị người dùng dừng.")


@dataclass(frozen=True)
class InputStageOutput:
    manual_requirement: str
    docs_sections: list[tuple[str, str]]
    source_sections: list[tuple[str, str]]
    test_sections: list[tuple[str, str]]
    has_docs: bool
    has_source: bool
    has_test_code: bool
    review_only_mode: bool
    retrieval_source: str


@dataclass(frozen=True)
class RagStageOutput:
    docs_context: str = ""
    source_context: str = ""
    context: str = ""
    docs_new_signature: str = ""
    source_new_signature: str = ""
    used_preindexed_docs: bool = False


@dataclass(frozen=True)
class RequirementStageOutput:
    requirement_json: str
    ast_context: str
    python_source_text: str


@dataclass(frozen=True)
class PlanningStageOutput:
    test_plan_json: str
    test_case_rows: list[dict[str, str]]


@dataclass(frozen=True)
class GenerationStageOutput:
    generated_code: str
    generation_call_count: int


@dataclass(frozen=True)
class ExecutionStageOutput:
    generated_code: str
    execution_summary: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReviewStageOutput:
    review_report: str
    review_target_code: str
    review_target_label: str


@dataclass(frozen=True)
class ArtifactStageOutput:
    code_path: str = ""
    test_plan_path: str = ""
    review_path: str = ""
    review_md_path: str = ""
    coverage_report_path: str = ""
    coverage_json_path: str = ""
    coverage_raw_path: str = ""
    pytest_log_path: str = ""
    collection_log_path: str = ""


def emit_progress(
    progress: list[dict[str, str]],
    callback,
    step: str,
    agent: str,
    model: str,
    status: str,
    result: str,
) -> None:
    item = {
        "step": step,
        "agent": agent,
        "model": model,
        "status": status,
        "result": result,
    }
    progress.append(item)
    if callback:
        callback(item)


def coerce_review_paths(saved_review) -> tuple[str, str]:
    if isinstance(saved_review, (list, tuple)):
        review_path = str(saved_review[0]) if saved_review else ""
        review_md_path = str(saved_review[1]) if len(saved_review) > 1 else ""
        return review_path, review_md_path
    return str(saved_review or ""), ""


def coerce_rag_result(result) -> tuple[str, int, bool, str, dict[str, Any]]:
    if isinstance(result, (list, tuple)):
        if len(result) >= 4:
            diagnostics = result[4] if len(result) >= 5 and isinstance(result[4], dict) else {}
            return str(result[0]), int(result[1]), bool(result[2]), str(result[3]), diagnostics
        if len(result) == 3:
            return str(result[0]), int(result[1]), bool(result[2]), "", {}
    raise ValueError("Kết quả RAG không hợp lệ.")


def coerce_preindexed_rag_result(result) -> tuple[str, bool, dict[str, Any]]:
    if isinstance(result, (list, tuple)):
        if len(result) >= 3:
            diagnostics = result[2] if isinstance(result[2], dict) else {}
            return str(result[0]), bool(result[1]), diagnostics
        if len(result) == 2:
            return str(result[0]), bool(result[1]), {}
    raise ValueError("Kết quả RAG pre-indexed không hợp lệ.")


def coerce_coverage_paths(saved_coverage) -> tuple[str, str, str]:
    if isinstance(saved_coverage, (list, tuple)):
        report_path = str(saved_coverage[0]) if len(saved_coverage) > 0 else ""
        json_path = str(saved_coverage[1]) if len(saved_coverage) > 1 else ""
        raw_path = str(saved_coverage[2]) if len(saved_coverage) > 2 else ""
        return report_path, json_path, raw_path
    return "", "", ""


def format_missing_lines_snippet(
    missing_lines: list,
    source_text: str,
    max_lines: int = 30,
) -> str:
    if not missing_lines or not source_text:
        return str(missing_lines)
    source_lines = source_text.splitlines()
    snippets: list[str] = []
    for line_no in missing_lines:
        idx = int(line_no) - 1
        if 0 <= idx < len(source_lines):
            snippets.append(f"    {line_no}: {source_lines[idx]}")
        if len(snippets) >= max_lines:
            snippets.append(f"    ... (còn {len(missing_lines) - max_lines} dòng nữa)")
            break
    if not snippets:
        return str(missing_lines)
    return "\n" + "\n".join(snippets)


def format_execution_issue_for_review(execution_summary: dict[str, object]) -> str:
    issue = execution_summary.get("execution_issue") if isinstance(execution_summary, dict) else None
    if not isinstance(issue, dict) or not issue:
        return ""
    return (
        "\n\nExecution classification từ pytest executor:\n"
        f"- Loại lỗi: {issue.get('type', '')}\n"
        f"- Mô tả: {issue.get('title', '')}\n"
        f"- Gợi ý sửa: {issue.get('hint', '')}\n"
        f"- Missing lines count: {issue.get('missing_lines_count', '')}\n"
    )


class InputStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def run(self, ctx: PipelineRunContext) -> InputStageOutput:
        input_data = ctx.input_data
        backend = ctx.backend

        if backend == "gemini" and not input_data.api_key:
            raise ValueError("Nhập Gemini API key trước khi tạo mã.")
        if backend == "openrouter" and not input_data.api_key:
            raise ValueError("Nhập OpenRouter API key trước khi tạo mã.")

        manual_requirement = self.deps.normalize_text(input_data.requirement_text)

        if input_data.workflow_mode == REVIEW_WORKFLOW:
            docs_sections = []
        elif input_data.use_preindexed_docs:
            docs_sections = [("__preindexed_docs__", "ready")]
        else:
            docs_sections = (
                self.deps.load_uploaded_file_entries(input_data.docs_files)
                if input_data.docs_files
                else []
            )

        source_sections = self.deps.combine_sections(
            self.deps.load_text_uploaded_file_entries(input_data.source_files),
            input_data.source_code_text,
            "Dán source code",
        )
        test_sections = self.deps.combine_sections(
            self.deps.load_text_uploaded_file_entries(input_data.test_files),
            input_data.test_code_text,
            "Dán test code",
        )

        has_docs = bool(docs_sections)
        has_source = bool(source_sections)
        has_test_code = bool(test_sections)
        review_only_mode = input_data.workflow_mode == REVIEW_WORKFLOW

        if has_source and not review_only_mode:
            mismatch_message = self.deps.validate_framework_sections(
                input_data.framework,
                source_sections,
            )
            if mismatch_message:
                raise ValueError(mismatch_message)

        if review_only_mode and not has_test_code:
            raise ValueError("Hãy dán hoặc tải test code trước khi chạy review.")
        if review_only_mode and has_test_code:
            mismatch_message = self.deps.validate_framework_sections(
                input_data.framework,
                test_sections,
            )
            if mismatch_message:
                raise ValueError(mismatch_message)

        retrieval_source = self.deps.resolve_retrieval_source(
            retrieval_query=input_data.retrieval_query,
            manual_requirement=manual_requirement,
            has_docs=has_docs,
            has_source=has_source,
            has_test_code=has_test_code,
        )

        if not retrieval_source and not has_docs and not has_source and not has_test_code:
            raise ValueError(
                "Hãy nhập source code, test code hoặc tải lên tài liệu trước khi chạy."
            )

        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "1",
            "Input Loader",
            "Python rule-based",
            "Xong",
            (
                f"Đã nhận {len(input_data.docs_files)} tệp tài liệu, "
                f"{len(input_data.source_files)} tệp source và {len(input_data.test_files)} tệp test. "
                + (
                    "Đang dùng kho tìm nhanh tài liệu đã có sẵn."
                    if input_data.use_preindexed_docs
                    else f"Số tệp tài liệu đưa vào xử lý: {len(docs_sections)}."
                )
            ),
        )

        return InputStageOutput(
            manual_requirement=manual_requirement,
            docs_sections=docs_sections,
            source_sections=source_sections,
            test_sections=test_sections,
            has_docs=has_docs,
            has_source=has_source,
            has_test_code=has_test_code,
            review_only_mode=review_only_mode,
            retrieval_source=retrieval_source,
        )


class RagStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def run(self, ctx: PipelineRunContext, stage_input: InputStageOutput) -> RagStageOutput:
        docs_query = stage_input.retrieval_source
        source_query = stage_input.retrieval_source

        def process_docs():
            if not stage_input.has_docs:
                return "", 0, False, False, "", {}
            if ctx.input_data.use_preindexed_docs:
                rag_context, has_preindexed, retrieval_diagnostics = coerce_preindexed_rag_result(
                    self.deps.retrieve_preindexed_rag_context(
                        self.deps.doc_collection_name,
                        docs_query,
                        ctx.embedding_backend,
                        ctx.input_data.api_key,
                    )
                )
                if not has_preindexed:
                    return "", 0, False, False, "", retrieval_diagnostics
                return (
                    rag_context,
                    self.deps.collection_count(self.deps.doc_collection_name),
                    True,
                    True,
                    "",
                    retrieval_diagnostics,
                )

            rag_context, count, reused, new_signature, retrieval_diagnostics = coerce_rag_result(
                self.deps.build_rag_context(
                    self.deps.doc_collection_name,
                    stage_input.docs_sections,
                    docs_query,
                    "Tài liệu",
                    ctx.embedding_backend,
                    ctx.input_data.api_key,
                    ctx.input_data.previous_docs_signature,
                )
            )
            return rag_context, count, reused, False, new_signature, retrieval_diagnostics

        def process_source():
            if not stage_input.has_source:
                return "", 0, False, "", {}
            
            # GIẢI QUYẾT NÚT THẮT CỔ CHAI:
            # Nếu là mã nguồn Python/pytest, bỏ qua RAG hoàn toàn vì đã có AST lo phần context này.
            if ctx.input_data.framework in ("pytest",):
                return "", 0, False, "", {"skipped_reason": "pytest_ast_context"}

            rag_context, count, reused, new_signature, retrieval_diagnostics = coerce_rag_result(
                self.deps.build_rag_context(
                    self.deps.source_collection_name,
                    stage_input.source_sections,
                    source_query,
                    "Source code",
                    ctx.embedding_backend,
                    ctx.input_data.api_key,
                    ctx.input_data.previous_source_signature,
                )
            )
            return rag_context, count, reused, new_signature, retrieval_diagnostics

        with ThreadPoolExecutor(max_workers=PIPELINE_MAX_WORKERS) as executor:
            future_docs = executor.submit(process_docs)
            future_source = executor.submit(process_source)

            (
                docs_context,
                docs_chunk_count,
                docs_reused,
                used_preindexed_docs,
                docs_new_signature,
                docs_retrieval_diagnostics,
            ) = future_docs.result()
            (
                source_context,
                source_chunk_count,
                source_reused,
                source_new_signature,
                source_retrieval_diagnostics,
            ) = future_source.result()

        ctx.diagnostics["rag_retrieval"] = {
            "docs": docs_retrieval_diagnostics,
            "source": source_retrieval_diagnostics,
        }

        if docs_chunk_count > 0:
            if docs_reused:
                ctx.diagnostics["rag_reused_collections"] = int(ctx.diagnostics["rag_reused_collections"]) + 1
                ctx.diagnostics["docs_chunks_reused"] = docs_chunk_count
            else:
                ctx.diagnostics["docs_chunks_indexed"] = docs_chunk_count

        if source_chunk_count > 0:
            if source_reused:
                ctx.diagnostics["rag_reused_collections"] = int(ctx.diagnostics["rag_reused_collections"]) + 1
                ctx.diagnostics["source_chunks_reused"] = source_chunk_count
            else:
                ctx.diagnostics["source_chunks_indexed"] = source_chunk_count

        if used_preindexed_docs or docs_chunk_count or source_chunk_count:
            index_message_parts = []
            if used_preindexed_docs:
                index_message_parts.append("tài liệu từ kho tìm nhanh sẵn có")
            elif docs_chunk_count:
                index_message_parts.append(f"{docs_chunk_count} chunk tài liệu")
            if source_chunk_count:
                index_message_parts.append(f"{source_chunk_count} chunk source code")
            self.deps.emit_progress(
                ctx.progress,
                ctx.progress_callback,
                "2",
                "RAG Retriever + Embedding + Vector DB",
                ctx.embedding_label,
                "Xong",
                f"Đã xử lý kho tìm nhanh ({', '.join(index_message_parts)}) và truy xuất top {TOP_K}.",
            )
        else:
            self.deps.emit_progress(
                ctx.progress,
                ctx.progress_callback,
                "2",
                "RAG Retriever + Embedding + Vector DB",
                ctx.embedding_label,
                "Bỏ qua",
                "Chưa có tài liệu hoặc source code được tải lên, nên chưa có dữ liệu để truy xuất.",
            )

        return RagStageOutput(
            docs_context=docs_context,
            source_context=source_context,
            context=self.deps.merge_contexts(docs_context, source_context),
            docs_new_signature=docs_new_signature,
            source_new_signature=source_new_signature,
            used_preindexed_docs=used_preindexed_docs,
        )


class RequirementStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def run(
        self,
        ctx: PipelineRunContext,
        input_stage: InputStageOutput,
        rag_stage: RagStageOutput,
    ) -> RequirementStageOutput:
        python_source_text = self.deps.python_source_for_generation(input_stage.source_sections)

        def analyze_reqs():
            return self.deps.analyze_requirements(
                self.deps.clip_text(input_stage.retrieval_source, 5000),
                self.deps.clip_text(rag_stage.context, REQUIREMENT_CONTEXT_BUDGET),
                ctx.input_data.framework,
                backend=ctx.backend,
                api_key=ctx.input_data.api_key,
                model=ctx.profile.requirement_model,
            )

        def analyze_ast():
            if python_source_text:
                from testgen.analyzer.ast_analyzer import AdvancedASTAnalyzer
                from testgen.core.language_guard import expected_language_for_framework

                language = expected_language_for_framework(ctx.input_data.framework) or "python"
                if language in {"python", "java", "javascript"}:
                    analyzer = AdvancedASTAnalyzer(python_source_text, language=language)
                    return analyzer.get_context_summary()
            return ""

        with ThreadPoolExecutor(max_workers=PIPELINE_MAX_WORKERS) as executor:
            future_req = executor.submit(analyze_reqs)
            future_ast = executor.submit(analyze_ast)

            requirement_json = future_req.result()
            ast_context = future_ast.result()

        ctx.diagnostics["llm_calls_estimated"] = int(ctx.diagnostics["llm_calls_estimated"]) + 1
        ctx.diagnostics["context_lengths"] = {
            **dict(ctx.diagnostics.get("context_lengths", {})),
            "retrieval_context_chars": len(rag_stage.context or ""),
            "python_source_chars": len(python_source_text or ""),
        }
        ctx.diagnostics["context_budget_chars"] = {
            **dict(ctx.diagnostics.get("context_budget_chars", {})),
            "requirement": REQUIREMENT_CONTEXT_BUDGET,
            "generation": GENERATION_CONTEXT_BUDGET,
            "review": REVIEW_CONTEXT_BUDGET,
        }
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "3",
            "Requirement Agent",
            ctx.profile.requirement_model,
            "Xong",
            "Đã trích xuất yêu cầu có cấu trúc.",
        )
        return RequirementStageOutput(
            requirement_json=requirement_json,
            ast_context=ast_context,
            python_source_text=python_source_text,
        )


class PlanningStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def run(
        self,
        ctx: PipelineRunContext,
        requirement_stage: RequirementStageOutput,
    ) -> PlanningStageOutput:
        test_plan_json = self.deps.generate_test_plan(
            self.deps.clip_text(requirement_stage.requirement_json, 8000),
            ctx.input_data.test_technique,
            backend=ctx.backend,
            api_key=ctx.input_data.api_key,
            ast_context=requirement_stage.ast_context,
            model=ctx.profile.planning_model,
        )
        ctx.diagnostics["llm_calls_estimated"] = int(ctx.diagnostics["llm_calls_estimated"]) + 1
        test_case_rows = self.deps.parse_test_plan_rows(test_plan_json)
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "4",
            "Test Planning Agent",
            ctx.profile.planning_model,
            "Xong",
            f"Đã tạo {len(test_case_rows)} dòng test case."
            + (" (Hỗ trợ bởi AST)" if requirement_stage.ast_context else ""),
        )
        return PlanningStageOutput(test_plan_json=test_plan_json, test_case_rows=test_case_rows)


class GenerationStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def run(
        self,
        ctx: PipelineRunContext,
        requirement_stage: RequirementStageOutput,
        planning_stage: PlanningStageOutput,
        previous_review_feedback: str = "",
    ) -> GenerationStageOutput:
        generation_call_count = self.deps.estimate_test_generation_llm_calls(
            ctx.input_data.framework,
            requirement_stage.python_source_text,
        )
        req_json = self.deps.clip_text(requirement_stage.requirement_json, GENERATION_CONTEXT_BUDGET)
        if previous_review_feedback:
            req_json += f"\n\n[FEEDBACK TỪ REVIEWER LẦN CHẠY TRƯỚC]:\n{previous_review_feedback}\n\nHãy sửa lại code để khắc phục các lỗi trên, đảm bảo liêm chính và code vượt qua các rào cản thực thi."

        generated_code = self.deps.generate_test_code(
            req_json,
            self.deps.clip_text(planning_stage.test_plan_json, GENERATION_CONTEXT_BUDGET),
            ctx.input_data.framework,
            ctx.input_data.test_technique,
            backend=ctx.backend,
            api_key=ctx.input_data.api_key,
            model=ctx.profile.generator_model,
            source_code_text=requirement_stage.python_source_text,
        )
        ctx.diagnostics["llm_calls_estimated"] = int(ctx.diagnostics["llm_calls_estimated"]) + generation_call_count
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "5",
            "Code Test Generator Agent",
            ctx.profile.generator_model,
            "Xong",
            f"Đã sinh {len(generated_code):,} ký tự mã kiểm thử.",
        )
        return GenerationStageOutput(
            generated_code=generated_code,
            generation_call_count=generation_call_count,
        )


class ExecutionStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def _run_external_once(
        self,
        ctx: PipelineRunContext,
        executor,
        requirement_stage: RequirementStageOutput,
        generation_stage: GenerationStageOutput,
    ) -> ExecutionStageOutput:
        execution_dir = OUTPUT_RUNS_PATH / "tmp_execution" / ctx.run_id
        outcome = executor.execute(
            TestExecutionRequest(
                source_code_text=requirement_stage.python_source_text,
                generated_test_code=generation_stage.generated_code,
                workspace_dir=execution_dir,
                coverage_threshold=PYTEST_COVERAGE_THRESHOLD,
                metadata={"framework": ctx.input_data.framework},
            )
        )
        execution_summary = dict(outcome.summary)
        passed = bool(execution_summary.get("passed", False))
        coverage_percent = float(execution_summary.get("coverage_percent", 0.0) or 0.0)
        coverage_available = bool(execution_summary.get("coverage_available", False))
        coverage_supported = bool(execution_summary.get("coverage_supported", False))
        coverage_status = str(execution_summary.get("coverage_status", "") or "")
        retry_supported = bool(execution_summary.get("retry_supported", False))
        issue = execution_summary.get("execution_issue", {})
        issue_type = str(issue.get("type", "")) if isinstance(issue, dict) else ""
        normalized_framework = str(executor.framework).lower().replace(" ", "_")

        ctx.diagnostics["test_execution_framework"] = executor.framework
        ctx.diagnostics["external_attempts"] = 1
        ctx.diagnostics["external_execution_passed"] = passed
        ctx.diagnostics["external_execution_issue_type"] = issue_type
        ctx.diagnostics["external_execution_command"] = execution_summary.get("command_text", "")
        ctx.diagnostics["external_coverage_percent"] = coverage_percent
        ctx.diagnostics["external_coverage_available"] = coverage_available
        ctx.diagnostics["external_coverage_supported"] = coverage_supported
        ctx.diagnostics["external_coverage_status"] = coverage_status
        ctx.diagnostics["external_retry_supported"] = retry_supported
        ctx.diagnostics[f"{normalized_framework}_passed"] = passed
        ctx.diagnostics[f"{normalized_framework}_execution_issue_type"] = issue_type
        ctx.diagnostics[f"{normalized_framework}_coverage_percent"] = coverage_percent
        ctx.diagnostics[f"{normalized_framework}_coverage_available"] = coverage_available
        ctx.diagnostics[f"{normalized_framework}_retry_supported"] = retry_supported

        coverage_text = (
            f"coverage={coverage_percent:.1f}%"
            if coverage_available
            else f"coverage=N/A ({coverage_status or 'not_supported'})"
        )

        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "6",
            f"{executor.framework} Executor",
            executor.display_name,
            "Dat" if passed else "Chua dat",
            (
                f"pass={passed}, {coverage_text}. "
                f"Issue={issue_type or 'none'}."
            ),
        )
        return ExecutionStageOutput(
            generated_code=generation_stage.generated_code,
            execution_summary=execution_summary,
        )

    def run(
        self,
        ctx: PipelineRunContext,
        requirement_stage: RequirementStageOutput,
        planning_stage: PlanningStageOutput,
        generation_stage: GenerationStageOutput,
    ) -> ExecutionStageOutput:
        executor = get_test_executor(
            ctx.input_data.framework,
            pytest_runner=self.deps.run_generated_pytest_with_coverage,
            pytest_scorer=self.deps.execution_result_score,
        )
        if executor is None:
            return ExecutionStageOutput(generated_code=generation_stage.generated_code)
        
        if not self.deps.normalize_text(requirement_stage.python_source_text):
            return ExecutionStageOutput(generated_code=generation_stage.generated_code)

        execution_dir = OUTPUT_RUNS_PATH / "tmp_execution" / ctx.run_id
        generated_code = generation_stage.generated_code
        base_generated_code = generated_code
        targeted_retry_parts: list[str] = []
        best_code = generated_code
        best_summary: dict[str, Any] = {}
        best_score = (-1, -1, -1.0)
        execution_summary: dict[str, Any] = {}

        for attempt in range(1, PYTEST_MAX_ATTEMPTS + 1):
            ctx.check_cancelled()
            retry_mode = "initial"
            if attempt > 1:
                previous_missing = execution_summary.get("missing_lines", [])
                missing_for_prompt = previous_missing if isinstance(previous_missing, list) else []
                previous_output = self.deps.clip_text(str(execution_summary.get("output", "")), 3000)
                previous_failure_summary = self.deps.clip_text(
                    str(execution_summary.get("failure_summary", "")),
                    1600,
                )
                previous_diagnosis = self.deps.normalize_text(str(execution_summary.get("diagnosis", "")))
                previous_issue = execution_summary.get("execution_issue", {})
                previous_coverage = float(execution_summary.get("coverage_percent", 0.0))
                previous_passed = bool(execution_summary.get("passed", False))
                targeted_retry_code = ""
                if (previous_passed or previous_issue.get("type") == "low_coverage") and missing_for_prompt and executor.framework in ("pytest", "JUnit", "Jest"):
                    req_json = (
                        self.deps.clip_text(requirement_stage.requirement_json, 8000)
                        + "\n\nLần chạy trước đã pass nhưng coverage chưa đạt."
                        + f"\nCoverage={previous_coverage:.1f}% "
                        + f"(ngưỡng {PYTEST_COVERAGE_THRESHOLD:.0f}%)."
                        + f"\nDòng source chưa bao phủ:{format_missing_lines_snippet(missing_for_prompt, requirement_stage.python_source_text)}"
                    )
                    if executor.framework == "pytest":
                        targeted_retry_code = self.deps.generate_targeted_pytest_code(
                            requirement_json=req_json,
                            test_plan_json=self.deps.clip_text(planning_stage.test_plan_json, 8000),
                            test_technique=ctx.input_data.test_technique,
                            source_code_text=requirement_stage.python_source_text,
                            missing_lines=missing_for_prompt,
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                            retry_namespace=f"retry_{attempt}",
                        )
                    elif executor.framework == "Jest" and self.deps.generate_targeted_jest_code:
                        targeted_retry_code = self.deps.generate_targeted_jest_code(
                            requirement_json=req_json,
                            test_plan_json=self.deps.clip_text(planning_stage.test_plan_json, 8000),
                            test_technique=ctx.input_data.test_technique,
                            source_code_text=requirement_stage.python_source_text,
                            base_generated_code=base_generated_code,
                            missing_lines=missing_for_prompt,
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                            retry_namespace=f"retry_{attempt}",
                        )
                    elif executor.framework == "JUnit":
                        # Truyền coverage_gaps (method-level) để LLM biết method nào cần cover
                        junit_coverage_gaps = execution_summary.get("junit_coverage_gaps") or {}
                        targeted_retry_code = self.deps.generate_targeted_junit_code(
                            requirement_json=req_json,
                            test_plan_json=self.deps.clip_text(planning_stage.test_plan_json, 8000),
                            test_technique=ctx.input_data.test_technique,
                            source_code_text=requirement_stage.python_source_text,
                            base_generated_code=base_generated_code,
                            missing_lines=missing_for_prompt,
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                            retry_namespace=f"retry_{attempt}",
                            coverage_gaps=junit_coverage_gaps,
                        )

                if targeted_retry_code.strip():
                    if executor.framework == "pytest":
                        targeted_retry_parts.append(targeted_retry_code)
                        generated_code = (
                            base_generated_code
                            + "\n\n# ===== Targeted retry tests =====\n\n"
                            + "\n\n".join(targeted_retry_parts)
                        )
                    elif executor.framework == "Jest":
                        generated_code = (
                            base_generated_code
                            + "\n\n// ===== Targeted retry tests =====\n\n"
                            + targeted_retry_code
                        )
                        base_generated_code = generated_code
                    elif executor.framework == "JUnit":
                        last_brace_idx = base_generated_code.rfind("}")
                        if last_brace_idx != -1:
                            generated_code = (
                                base_generated_code[:last_brace_idx]
                                + "\n\n    // ===== Targeted retry tests =====\n\n"
                                + targeted_retry_code
                                + "\n"
                                + base_generated_code[last_brace_idx:]
                            )
                        else:
                            generated_code = base_generated_code + "\n" + targeted_retry_code
                        base_generated_code = generated_code # Update base to accumulate
                        
                    retry_mode = "targeted_function_retry"
                    ctx.diagnostics["targeted_retries"] = int(ctx.diagnostics.get("targeted_retries", 0)) + 1
                    ctx.diagnostics["llm_calls_estimated"] = int(ctx.diagnostics.get("llm_calls_estimated", 0)) + 1
                else:
                    issue_hint = ""
                    if isinstance(previous_issue, dict) and previous_issue:
                        issue_hint = (
                            "\nPhân loại lỗi execution: "
                            + f"{previous_issue.get('type', '')} - {previous_issue.get('hint', '')}."
                        )
                    retry_requirement = (
                        self.deps.clip_text(requirement_stage.requirement_json, 8000)
                        + "\n\nLần chạy trước chưa đạt chất lượng."
                        + f"\n{executor.framework} pass={previous_passed}, coverage={previous_coverage:.1f}% "
                        + f"(ngưỡng {PYTEST_COVERAGE_THRESHOLD:.0f}%)."
                        + "\nMục tiêu bắt buộc: tất cả test phải pass và coverage phải đạt ngưỡng."
                        + "\nNếu log cho thấy assertion hoặc kỳ vọng exception sai, hãy sửa kỳ vọng test theo đúng source."
                        + issue_hint
                        + f"\nDòng source chưa bao phủ:{format_missing_lines_snippet(missing_for_prompt, requirement_stage.python_source_text)}"
                        + (f"\nNguyên nhân lỗi: {previous_diagnosis}." if previous_diagnosis else "")
                        + (
                            f"\nTóm tắt lỗi {executor.framework} trọng yếu:\n{previous_failure_summary}"
                            if previous_failure_summary
                            else ""
                        )
                        + f"\nLog {executor.framework} rút gọn:\n{previous_output}\n"
                        + "\n--- MÃ TEST BỊ LỖI Ở LẦN CHẠY TRƯỚC ---\n"
                        + self.deps.clip_text(base_generated_code, 4000)
                        + f"Hãy sinh lại test {executor.framework} để pass và tăng coverage. Chỉ xuất mã test."
                    )
                    
                    if executor.framework == "Jest" and attempt >= 4:
                        retry_requirement += "\n\nCẢNH BÁO TỚI AI: Các cách tiếp cận test trước đây đã gây crash nặng hoặc không đạt coverage sau nhiều lần thử. BẠN BẮT BUỘC PHẢI TÌM MỘT HƯỚNG TEST HOÀN TOÀN MỚI, có thể phải mock nhiều thứ hơn hoặc setup lại môi trường. TUYỆT ĐỐI KHÔNG LẶP LẠI MÃ TEST CŨ."

                    if executor.framework in ("pytest", "Selenium", "Playwright") and (
                        previous_coverage >= PYTEST_COVERAGE_THRESHOLD
                        or (isinstance(previous_issue, dict) and previous_issue.get("type") in [
                            "wrong_expected_value",
                            "wrong_exception_expectation",
                            "collection_error",   # NameError/ImportError during pytest collection
                            "import_error",       # Module import failure
                            "syntax_error",       # Python syntax error in generated code
                            "execution_error",    # Generic E2E UI crash
                        ])
                    ):
                        retry_mode = "heal_retry"
                        ctx.diagnostics["pytest_heal_retries"] = int(ctx.diagnostics.get("pytest_heal_retries", 0)) + 1
                        ctx.diagnostics["pytest_last_heal_issue_type"] = previous_issue.get("type") if isinstance(previous_issue, dict) else ""
                        generated_code = self.deps.heal_pytest_code(
                            test_code=base_generated_code,
                            error_log=self.deps.clip_text(previous_failure_summary + "\n" + previous_output, 4000),
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                            source_code_text=requirement_stage.python_source_text,
                            issue_type=previous_issue.get("type") if isinstance(previous_issue, dict) else "",
                            coverage_percent=previous_coverage,
                            coverage_threshold=PYTEST_COVERAGE_THRESHOLD,
                            failure_summary=previous_failure_summary,
                        )
                    elif executor.framework == "JUnit" and attempt < 4 and self.deps.heal_junit_code and isinstance(previous_issue, dict) and previous_issue.get("type") in ["security_block", "assertion_error", "test_compilation_error", "null_pointer_error", "runtime_exception", "low_coverage"]:
                        # Fail-fast JUnit security_block: chỉ cho 1 vòng security sanitize retry
                        junit_security_block_count = int(ctx.diagnostics.get("junit_security_block_count", 0))
                        if previous_issue.get("type") == "security_block":
                            if junit_security_block_count >= 1:
                                break  # Đã dùng 1 vòng sanitize, dừng ngay
                            ctx.diagnostics["junit_security_block_count"] = junit_security_block_count + 1
                        retry_mode = "heal_retry"
                        junit_coverage_gaps = execution_summary.get("junit_coverage_gaps") or {}
                        generated_code = self.deps.heal_junit_code(
                            test_code=base_generated_code,
                            error_log=self.deps.clip_text(previous_failure_summary + "\n" + previous_output, 4000),
                            issue_type=previous_issue.get("type") if isinstance(previous_issue, dict) else "",
                            source_code_text=requirement_stage.python_source_text,
                            coverage_gaps=junit_coverage_gaps,
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                        )
                        ctx.diagnostics["junit_heal_retries"] = int(ctx.diagnostics.get("junit_heal_retries", 0)) + 1
                    elif executor.framework == "Jest" and attempt < 4 and self.deps.heal_jest_code and isinstance(previous_issue, dict) and previous_issue.get("type") in ["test_failed", "assertion_error", "runtime_type_error", "wrong_exception_expectation"]:
                        retry_mode = "heal_retry"
                        generated_code = self.deps.heal_jest_code(
                            test_code=base_generated_code,
                            error_log=self.deps.clip_text(previous_output, 4000),
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                        )
                    elif executor.framework == "Postman script" and attempt < 4 and self.deps.heal_postman_code and isinstance(previous_issue, dict) and previous_issue.get("type") in ["test_failed", "assertion_error"]:
                        retry_mode = "heal_retry"
                        generated_code = self.deps.heal_postman_code(
                            test_code=base_generated_code,
                            error_log=self.deps.clip_text(previous_output, 4000),
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                        )
                    else:
                        generated_code = self.deps.generate_test_code(
                            retry_requirement,
                            self.deps.clip_text(planning_stage.test_plan_json, 8000),
                            ctx.input_data.framework,
                            ctx.input_data.test_technique,
                            backend=ctx.backend,
                            api_key=ctx.input_data.api_key,
                            model=ctx.profile.generator_model,
                            source_code_text=requirement_stage.python_source_text,
                        )
                    base_generated_code = generated_code
                    targeted_retry_parts = []
                    if "retry_mode" not in locals() or retry_mode != "heal_retry":
                        if isinstance(previous_issue, dict) and previous_issue.get("type") == "security_block":
                            retry_mode = "security_sanitize"
                        elif previous_passed or (isinstance(previous_issue, dict) and previous_issue.get("type") == "low_coverage"):
                            retry_mode = "coverage_topup"
                        else:
                            retry_mode = "runtime_heal"
                    ctx.diagnostics["full_retries"] = int(ctx.diagnostics.get("full_retries", 0)) + 1
                    ctx.diagnostics["llm_calls_estimated"] = (
                        int(ctx.diagnostics.get("llm_calls_estimated", 0)) + generation_stage.generation_call_count
                    )

            outcome = executor.execute(
                TestExecutionRequest(
                    source_code_text=requirement_stage.python_source_text,
                    generated_test_code=generated_code,
                    workspace_dir=execution_dir,
                    coverage_threshold=PYTEST_COVERAGE_THRESHOLD,
                )
            )
            ctx.diagnostics["test_execution_framework"] = executor.framework
            execution_summary = dict(outcome.summary)
            execution_summary["retry_mode"] = retry_mode
            retry_modes = ctx.diagnostics.setdefault("retry_modes", [])
            if isinstance(retry_modes, list):
                retry_modes.append(retry_mode)
            ctx.diagnostics["attempts"] = attempt
            coverage_percent = float(execution_summary.get("coverage_percent", 0.0))
            passed = bool(execution_summary.get("passed", False))
            issue = execution_summary.get("execution_issue", {})
            if isinstance(issue, dict):
                ctx.diagnostics["execution_issue_type"] = str(issue.get("type", ""))
            
            coverage_supported = bool(execution_summary.get("coverage_supported", getattr(executor, "coverage_supported", False)))
            # Giả lập điểm số tạm nếu chưa có hàm score_result chung
            score = (1 if passed else 0, coverage_percent, coverage_percent)
            if hasattr(executor, "score_result"):
                score = executor.score_result(execution_summary, PYTEST_COVERAGE_THRESHOLD)
                
            if score >= best_score:
                best_code = execution_summary.get("final_code", generated_code)
                best_summary = execution_summary
                best_score = score

            is_success = passed and (coverage_percent >= PYTEST_COVERAGE_THRESHOLD or not coverage_supported)
            self.deps.emit_progress(
                ctx.progress,
                ctx.progress_callback,
                f"6.{attempt}",
                f"{executor.framework} Executor",
                executor.display_name,
                "Đạt" if is_success else "Chưa đạt",
                (
                    f"Lần {attempt}/{PYTEST_MAX_ATTEMPTS}: "
                    f"pass={passed}, coverage={'N/A (không hỗ trợ)' if not coverage_supported else f'{coverage_percent:.1f}% (ngưỡng {PYTEST_COVERAGE_THRESHOLD:.0f}%)'}. "
                    f"Retry mode={retry_mode}."
                ),
            )

            # Break early if tests passed and coverage requirement is met (or unsupported)
            if is_success:
                break
            
            # Break early if it's an unrecoverable environment error
            if isinstance(issue, dict) and issue.get("type") in ("project_config_missing", "source_compilation_error"):
                break

        generated_code = best_code
        execution_summary = best_summary

        final_coverage = float(execution_summary.get("coverage_percent", 0.0))
        final_passed = bool(execution_summary.get("passed", False))
        normalized_fw = executor.framework.lower().replace(" ", "_")
        ctx.diagnostics[f"{normalized_fw}_passed"] = final_passed
        ctx.diagnostics[f"{normalized_fw}_coverage_percent"] = final_coverage
        
        final_issue = execution_summary.get("execution_issue", {})
        if isinstance(final_issue, dict):
            ctx.diagnostics[f"{normalized_fw}_execution_issue_type"] = str(final_issue.get("type", ""))
        final_missing = execution_summary.get("missing_lines", [])
        final_diagnosis = self.deps.normalize_text(str(execution_summary.get("diagnosis", "")))
        final_coverage_supported = bool(execution_summary.get("coverage_supported", getattr(executor, "coverage_supported", False)))
        final_success = final_passed and (final_coverage >= PYTEST_COVERAGE_THRESHOLD or not final_coverage_supported)
        
        if not final_success:
            if str(final_issue.get("type")) == "project_config_missing":
                self.deps.emit_progress(
                    ctx.progress,
                    ctx.progress_callback,
                    "6.99",
                    f"{executor.framework} Executor",
                    "Cảnh báo",
                    "Bỏ qua",
                    "Không tìm thấy cấu hình Maven/Gradle. Sẽ bỏ qua kiểm tra tự động và tiếp tục xuất mã.",
                )
            else:
                missing_count = len(final_missing) if isinstance(final_missing, list) else 0
                failure_stage = str(execution_summary.get("failure_stage", ""))
                issue_type = str(final_issue.get("type", "execution_failed"))
                quality_gate = execution_summary.get("quality_gate", "coverage")
                
                if not final_coverage_supported:
                    if failure_stage in ("preflight", "import", "browser_boot"):
                        diagnosis_msg = "test fail sớm trước khi chạy được luồng E2E chính"
                    else:
                        diagnosis_msg = "chưa đạt quality gate E2E flow/assertions"
                    
                    if issue_type in ("selenium_package_missing", "playwright_package_missing"):
                        diagnosis_msg = "thiếu package selenium/playwright trong môi trường Python đang chạy app"
                    elif issue_type in ("driver_missing", "playwright_browser_missing"):
                        diagnosis_msg = "thiếu browser driver nên chưa khởi động được trình duyệt"
                    
                    raise ValueError(
                        f"Từ chối xuất kết quả: chất lượng test chưa đạt.\n"
                        f"{executor.framework} pass={final_passed}, coverage=N/A, quality_gate={quality_gate}.\n"
                        f"Lỗi: {issue_type}.\n"
                        f"Nguyên nhân: {diagnosis_msg}."
                    )
                elif executor.framework == "JUnit":
                    # Refusal message tường minh cho JUnit
                    if issue_type == "low_coverage":
                        # Lấy method-level gaps từ execution_summary
                        gaps = execution_summary.get("junit_coverage_gaps") or {}
                        missed_methods = gaps.get("missed_methods", [])
                        partial_methods = gaps.get("partial_methods", [])
                        method_names = ", ".join(
                            m.get("name", "") for m in (missed_methods + partial_methods) if m.get("name")
                        ) or "N/A"
                        missing_lines_str = ", ".join(str(l) for l in (final_missing or [])[:20])
                        raise ValueError(
                            f"Từ chối xuất kết quả: pipeline không đạt chất lượng.\n"
                            f"framework=JUnit, passed=True, coverage={final_coverage:.1f}%, quality_gate={quality_gate}.\n"
                            f"Lỗi: low_coverage.\n"
                            f"Nguyên nhân: JUnit/Surefire pass nhưng JaCoCo coverage thấp hơn ngưỡng {PYTEST_COVERAGE_THRESHOLD:.0f}%.\n"
                            f"Missing methods: {method_names}.\n"
                            f"Missing lines: {missing_lines_str}.\n"
                            f"Gợi ý: thêm JUnit tests cho {method_names}."
                        )
                    elif issue_type == "security_block":
                        blocked_imports = execution_summary.get("junit_blocked_imports") or []
                        blocked_apis = execution_summary.get("junit_blocked_apis") or []
                        diagnosis_msg = final_diagnosis if final_diagnosis else "Generated JUnit test uses unsafe filesystem/network APIs"
                        raise ValueError(
                            f"Từ chối xuất kết quả: pipeline không đạt chất lượng.\n"
                            f"framework=JUnit, passed=False, coverage=0.0%, quality_gate={quality_gate}.\n"
                            f"Lỗi: security_block.\n"
                            f"Nguyên nhân: {diagnosis_msg}\n"
                            f"Blocked imports: {blocked_imports}. Blocked APIs: {blocked_apis}.\n"
                            f"Gợi ý: Xóa test @TempDir/filesystem và chỉ kiểm thử public API của source class."
                        )
                    elif issue_type == "missing_test_cases" and final_coverage >= PYTEST_COVERAGE_THRESHOLD:
                        # Coverage đạt nhưng plan có IDs out-of-scope -> invalid_plan_scope
                        raise ValueError(
                            f"Từ chối xuất kết quả: plan sai phạm vi.\n"
                            f"framework=JUnit, passed=True, coverage={final_coverage:.1f}%.\n"
                            f"Lỗi: invalid_plan_scope.\n"
                            f"Nguyên nhân: Coverage đạt {final_coverage:.1f}% nhưng test plan có IDs out-of-scope "
                            f"(test JUnit framework extension thay vì public API của source).\n"
                            f"Gợi ý: Xem xét lại test plan và loại bỏ các case @TempDir/MigrationTest/ParameterizedTest không liên quan đến source."
                        )
                    else:
                        diagnosis_msg = final_diagnosis if final_diagnosis else "JUnit execution failed"
                        raise ValueError(
                            f"Từ chối xuất kết quả: pipeline không đạt chất lượng.\n"
                            f"framework=JUnit, passed={final_passed}, coverage={final_coverage:.1f}% "
                            f"(ngưỡng {PYTEST_COVERAGE_THRESHOLD:.0f}%), quality_gate={quality_gate}.\n"
                            f"Lỗi: {issue_type}.\n"
                            f"Nguyên nhân: {diagnosis_msg}.\n"
                            f"Missing lines: {missing_count}."
                        )
                else:
                    diagnosis_msg = final_diagnosis if final_diagnosis else "Execution failed"
                    raise ValueError(
                        f"Từ chối xuất kết quả: chất lượng test chưa đạt.\n"
                        f"{executor.framework} pass={final_passed}, coverage={final_coverage:.1f}% "
                        f"(ngưỡng {PYTEST_COVERAGE_THRESHOLD:.0f}%), quality_gate={quality_gate}.\n"
                        f"Lỗi: {issue_type}.\n"
                        f"Nguyên nhân: {diagnosis_msg}.\n"
                        f"Missing lines: {missing_count}."
                    )

        return ExecutionStageOutput(
            generated_code=generated_code,
            execution_summary=execution_summary,
        )


class ReviewStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def run_review_only(
        self,
        ctx: PipelineRunContext,
        input_stage: InputStageOutput,
    ) -> ReviewStageOutput:
        review_target_code = "\n\n---\n\n".join(
            f"# Test code: {name}\n\n{text}" for name, text in input_stage.test_sections
        )
        review_target_label = "Test code người dùng cung cấp"

        review_report = self.deps.review_test_code(
            "",
            "",
            self.deps.clip_text(review_target_code, 12000),
            ctx.input_data.framework,
            ctx.input_data.test_technique,
            backend=ctx.backend,
            api_key=ctx.input_data.api_key,
            model=ctx.profile.review_model,
            review_target_label=review_target_label,
            source_code_text="",
        )
        ctx.diagnostics["llm_calls_estimated"] = 1
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "2",
            "Code Review Agent",
            ctx.profile.review_model,
            "Xong",
            "Đã tạo báo cáo rà soát từ test code đầu vào.",
        )
        return ReviewStageOutput(
            review_report=review_report,
            review_target_code=review_target_code,
            review_target_label=review_target_label,
        )

    def run_generated(
        self,
        ctx: PipelineRunContext,
        input_stage: InputStageOutput,
        requirement_stage: RequirementStageOutput,
        planning_stage: PlanningStageOutput,
        execution_stage: ExecutionStageOutput,
    ) -> ReviewStageOutput:
        review_target_code = execution_stage.generated_code
        review_target_label = "Mã kiểm thử đã sinh"
        if input_stage.has_test_code:
            review_target_code = "\n\n---\n\n".join(
                f"# Test code: {name}\n\n{text}" for name, text in input_stage.test_sections
            )
            review_target_label = "Test code người dùng cung cấp"
        source_reference = "\n\n---\n\n".join(
            f"# Source code: {name}\n\n{text}" for name, text in input_stage.source_sections
        )

        review_report = self.deps.review_test_code(
            self.deps.clip_text(requirement_stage.requirement_json, REVIEW_CONTEXT_BUDGET),
            self.deps.clip_text(
                planning_stage.test_plan_json + format_execution_issue_for_review(execution_stage.execution_summary),
                REVIEW_CONTEXT_BUDGET,
            ),
            self.deps.clip_text(review_target_code, 12000),
            ctx.input_data.framework,
            ctx.input_data.test_technique,
            backend=ctx.backend,
            api_key=ctx.input_data.api_key,
            model=ctx.profile.review_model,
            review_target_label=review_target_label,
            source_code_text=self.deps.clip_text(
                source_reference or requirement_stage.python_source_text,
                REVIEW_CONTEXT_BUDGET,
            ),
        )
        prq = assess_post_review_quality(
            framework=ctx.input_data.framework,
            execution_summary=execution_stage.execution_summary,
            review_report=review_report,
            generated_code=execution_stage.generated_code,
            test_plan_json=planning_stage.test_plan_json,
            requirement_json=requirement_stage.requirement_json,
            diagnostics=ctx.diagnostics,
        )
        score = prq.get("score", 0)

        ctx.diagnostics["llm_calls_estimated"] = int(ctx.diagnostics["llm_calls_estimated"]) + 1
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "7",
            "Code Review Agent",
            ctx.profile.review_model,
            "Xong",
            f"Đã tạo báo cáo rà soát PDF. Điểm review: {score}/100.",
        )
        return ReviewStageOutput(
            review_report=review_report,
            review_target_code=review_target_code,
            review_target_label=review_target_label,
        )


class ArtifactStage:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps

    def _record_artifact_error(self, ctx: PipelineRunContext, stage: str, exc: OSError) -> None:
        errors = ctx.diagnostics.setdefault("artifact_errors", [])
        item = {
            "stage": stage,
            "error": str(exc),
        }
        if isinstance(errors, list):
            errors.append(item)
        else:
            ctx.diagnostics["artifact_errors"] = [item]

    def _safe_artifact_call(
        self,
        ctx: PipelineRunContext,
        stage: str,
        action: Callable[[], Any],
        default: Any,
    ) -> Any:
        try:
            return action()
        except OSError as exc:
            self._record_artifact_error(ctx, stage, exc)
            return default

    def _persist_history(self, ctx: PipelineRunContext, **kwargs: Any) -> None:
        try:
            self.deps.persist_run_history(**kwargs)
        except OSError as exc:
            ctx.diagnostics["history_persist_error"] = str(exc)

    def save_review_only(
        self,
        ctx: PipelineRunContext,
        review_stage: ReviewStageOutput,
    ) -> ArtifactStageOutput:
        review_path, review_md_path = coerce_review_paths(
            self._safe_artifact_call(
                ctx,
                "review_report",
                lambda: self.deps.save_review_report(review_stage.review_report, run_id=ctx.run_id),
                ("", ""),
            )
        )
        try:
            self._persist_history(
                ctx,
                run_id=ctx.run_id,
                workflow=self.deps.workflow_label(ctx.input_data.workflow_mode),
                mode=ctx.profile.mode_label,
                backend=ctx.backend,
                framework=ctx.input_data.framework,
                test_technique=ctx.input_data.test_technique,
                review_path=review_path,
                review_md_path=review_md_path,
                diagnostics=ctx.diagnostics,
                metadata={
                    "models": {
                        "review": ctx.profile.review_model,
                        "embedding": ctx.profile.embed_model,
                    },
                    "embedding_backend": ctx.embedding_backend,
                },
            )
        except OSError:
            pass
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "3",
            "Formatter / Xuất file",
            "Python rule-based",
            "Xong",
            "Đã xuất review report.",
        )
        return ArtifactStageOutput(review_path=review_path, review_md_path=review_md_path)

    def save_generated(
        self,
        ctx: PipelineRunContext,
        planning_stage: PlanningStageOutput,
        execution_stage: ExecutionStageOutput,
        review_stage: ReviewStageOutput,
    ) -> ArtifactStageOutput:
        coverage_report_path = ""
        coverage_json_path = ""
        coverage_raw_path = ""
        if execution_stage.execution_summary:
            coverage_report_path, coverage_json_path, coverage_raw_path = (
                coerce_coverage_paths(
                    self._safe_artifact_call(
                        ctx,
                        "coverage_report",
                        lambda: self.deps.save_combined_coverage_report(
                            execution_stage.execution_summary,
                            run_id=ctx.run_id,
                        ),
                        ("", "", ""),
                    )
                )
            )

        code_path = self._safe_artifact_call(
            ctx,
            "generated_code",
            lambda: self.deps.save_generated_code(
                execution_stage.generated_code,
                ctx.input_data.framework,
                run_id=ctx.run_id,
            ),
            "",
        )
        test_plan_path = self._safe_artifact_call(
            ctx,
            "test_plan",
            lambda: self.deps.save_test_plan_excel(
                planning_stage.test_plan_json,
                run_id=ctx.run_id,
            ),
            "",
        )
        review_path, review_md_path = coerce_review_paths(
            self._safe_artifact_call(
                ctx,
                "review_report",
                lambda: self.deps.save_review_report(review_stage.review_report, run_id=ctx.run_id),
                ("", ""),
            )
        )
        pytest_log_path = str(execution_stage.execution_summary.get("pytest_log_path", "") or "")
        collection_log_path = str(execution_stage.execution_summary.get("collection_log_path", "") or "")
        try:
            self._persist_history(
                ctx,
                run_id=ctx.run_id,
                workflow=self.deps.workflow_label(ctx.input_data.workflow_mode),
                mode=ctx.profile.mode_label,
                backend=ctx.backend,
                framework=ctx.input_data.framework,
                test_technique=ctx.input_data.test_technique,
                code_path=code_path,
                test_plan_path=test_plan_path,
                review_path=review_path,
                review_md_path=review_md_path,
                coverage_report_path=coverage_report_path,
                coverage_json_path=coverage_json_path,
                coverage_raw_path=coverage_raw_path,
                pytest_log_path=pytest_log_path,
                collection_log_path=collection_log_path,
                diagnostics=ctx.diagnostics,
                metadata={
                    "models": {
                        "requirement": ctx.profile.requirement_model,
                        "planning": ctx.profile.planning_model,
                        "code_generator": ctx.profile.generator_model,
                        "review": ctx.profile.review_model,
                        "embedding": ctx.profile.embed_model,
                    },
                    "embedding_backend": ctx.embedding_backend,
                },
            )
        except OSError:
            pass
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "8",
            "Formatter / Xuất file",
            "Python rule-based",
            "Xong",
            "Đã xuất code, bảng test case Excel và review report.",
        )
        return ArtifactStageOutput(
            code_path=code_path,
            test_plan_path=test_plan_path,
            review_path=review_path,
            review_md_path=review_md_path,
            coverage_report_path=coverage_report_path,
            coverage_json_path=coverage_json_path,
            coverage_raw_path=coverage_raw_path,
            pytest_log_path=pytest_log_path,
            collection_log_path=collection_log_path,
        )


class PipelineRunner:
    def __init__(self, deps: PipelineDependencies) -> None:
        self.deps = deps
        self.input_stage = InputStage(deps)
        self.rag_stage = RagStage(deps)
        self.requirement_stage = RequirementStage(deps)
        self.planning_stage = PlanningStage(deps)
        self.generation_stage = GenerationStage(deps)
        self.execution_stage = ExecutionStage(deps)
        self.review_stage = ReviewStage(deps)
        self.artifact_stage = ArtifactStage(deps)

    def _run_timed_stage(
        self,
        ctx: PipelineRunContext,
        stage_name: str,
        action: Callable[[], Any],
    ) -> Any:
        ctx.check_cancelled()
        started_at = time.perf_counter()
        try:
            return action()
        finally:
            elapsed_ms = (time.perf_counter() - started_at) * 1000
            timings = ctx.diagnostics.setdefault("stage_timings_ms", {})
            if isinstance(timings, dict):
                timings[stage_name] = round(elapsed_ms, 2)

    def _finalize_diagnostics(self, ctx: PipelineRunContext) -> None:
        timings = ctx.diagnostics.get("stage_timings_ms")
        if isinstance(timings, dict) and timings:
            sorted_timings = sorted(
                ((str(name), float(value or 0.0)) for name, value in timings.items()),
                key=lambda item: item[1],
                reverse=True,
            )
            ctx.diagnostics["stage_total_ms"] = round(sum(value for _name, value in sorted_timings), 2)
            ctx.diagnostics["stage_bottleneck"] = {
                "stage": sorted_timings[0][0],
                "elapsed_ms": round(sorted_timings[0][1], 2),
            }
            ctx.diagnostics["stage_bottlenecks"] = [
                {"stage": name, "elapsed_ms": round(value, 2)}
                for name, value in sorted_timings[:3]
            ]

        ctx.diagnostics["models_used"] = {
            "requirement": ctx.profile.requirement_model,
            "planning": ctx.profile.planning_model,
            "code_generator": ctx.profile.generator_model,
            "code_reviewer": ctx.profile.review_model,
            "embedding": ctx.profile.embed_model,
            "backend": ctx.backend,
            "embedding_backend": ctx.embedding_backend,
        }
        execution_framework = str(ctx.diagnostics.get("test_execution_framework", "") or "")
        if execution_framework and execution_framework != "pytest":
            ctx.diagnostics["retry_summary"] = {
                "framework": execution_framework,
                "attempts": int(ctx.diagnostics.get("external_attempts", 0) or 0),
                "retry_supported": bool(ctx.diagnostics.get("external_retry_supported", False)),
                "reason": "external_framework_retry_not_supported",
            }
        else:
            ctx.diagnostics["retry_summary"] = {
                "pytest_attempts": int(ctx.diagnostics.get("pytest_attempts", 0) or 0),
                "targeted_retries": int(ctx.diagnostics.get("pytest_targeted_retries", 0) or 0),
                "full_retries": int(ctx.diagnostics.get("pytest_full_retries", 0) or 0),
                "retry_modes": list(ctx.diagnostics.get("pytest_retry_modes", [])),
            }

        rag_retrieval = ctx.diagnostics.get("rag_retrieval")
        if rag_retrieval:
            ctx.diagnostics["rag_quality"] = assess_rag_quality(
                rag_retrieval,
                expected_framework=execution_framework or ctx.input_data.framework
            )

    def run(
        self,
        input_data: PipelineInput,
        profile: PipelineProfile,
        progress_callback=None,
        cancel_check=None,
    ) -> PipelineResult:
        backend = profile.backend
        embedding_backend = profile.embedding_backend or ("ollama" if backend == "openrouter" else backend)
        ctx = PipelineRunContext(
            input_data=input_data,
            profile=profile,
            run_id=self.deps.create_run_id(),
            backend=backend,
            embedding_backend=embedding_backend,
            embedding_label=f"{profile.embed_model} ({embedding_backend})",
            progress=[],
            diagnostics={
                "docs_chunks_indexed": 0,
                "docs_chunks_reused": 0,
                "source_chunks_indexed": 0,
                "source_chunks_reused": 0,
                "rag_reused_collections": 0,
                "llm_calls_estimated": 0,
                "pytest_attempts": 0,
                "pytest_passed": False,
                "pytest_coverage_percent": 0.0,
                "pytest_combined_coverage_percent": 0.0,
                "pytest_targeted_retries": 0,
                "pytest_full_retries": 0,
                "pytest_retry_modes": [],
                "stage_timings_ms": {},
            },
            progress_callback=progress_callback,
            cancel_check=cancel_check,
        )

        input_result = self._run_timed_stage(ctx, "input", lambda: self.input_stage.run(ctx))
        if input_result.review_only_mode:
            review_result = self._run_timed_stage(
                ctx,
                "review",
                lambda: self.review_stage.run_review_only(ctx, input_result),
            )
            artifacts = self._run_timed_stage(
                ctx,
                "artifacts",
                lambda: self.artifact_stage.save_review_only(ctx, review_result),
            )
            self._finalize_diagnostics(ctx)
            return PipelineResult(
                context="",
                docs_context="",
                source_context="",
                requirement_json="",
                test_plan_json="",
                test_case_rows=[],
                generated_code="",
                review_report=review_result.review_report,
                review_target_code=review_result.review_target_code,
                review_target_label=review_result.review_target_label,
                code_path="",
                test_plan_path="",
                review_path=artifacts.review_path,
                review_md_path=artifacts.review_md_path,
                run_id=ctx.run_id,
                framework=input_data.framework,
                test_technique=input_data.test_technique,
                mode=profile.mode_label,
                backend=backend,
                embedding_backend=embedding_backend,
                embed_model=profile.embed_model,
                requirement_model=profile.requirement_model,
                planning_model=profile.planning_model,
                generator_model=profile.generator_model,
                review_model=profile.review_model,
                workflow=input_data.workflow_mode,
                workflow_label=self.deps.workflow_label(input_data.workflow_mode),
                progress=ctx.progress,
                diagnostics=ctx.diagnostics,
            )

        rag_result = self._run_timed_stage(ctx, "rag", lambda: self.rag_stage.run(ctx, input_result))
        requirement_result = self._run_timed_stage(
            ctx,
            "requirement",
            lambda: self.requirement_stage.run(ctx, input_result, rag_result),
        )
        planning_result = self._run_timed_stage(
            ctx,
            "planning",
            lambda: self.planning_stage.run(ctx, requirement_result),
        )
        attempt = 0
        max_retries = 3
        best_prq_score = -1
        best_execution = None
        best_review = None
        best_generation = None
        best_prq = None
        
        previous_feedback = ""
        
        while attempt < max_retries:
            attempt += 1
            ctx.diagnostics["review_loop_attempt"] = attempt
            
            # Lưu ý dùng default argument trong lambda để bind chặt biến thay vì tham chiếu biến của loop
            generation_result = self._run_timed_stage(
                ctx,
                f"generation_{attempt}",
                lambda fb=previous_feedback: self.generation_stage.run(ctx, requirement_result, planning_result, fb),
            )
            execution_result = self._run_timed_stage(
                ctx,
                f"execution_{attempt}",
                lambda g=generation_result: self.execution_stage.run(
                    ctx,
                    requirement_result,
                    planning_result,
                    g,
                ),
            )
            review_result = self._run_timed_stage(
                ctx,
                f"review_{attempt}",
                lambda e=execution_result: self.review_stage.run_generated(
                    ctx,
                    input_result,
                    requirement_result,
                    planning_result,
                    e,
                ),
            )
            
            prq = assess_post_review_quality(
                framework=input_data.framework,
                execution_summary=execution_result.execution_summary,
                review_report=review_result.review_report,
                generated_code=execution_result.generated_code,
                test_plan_json=planning_result.test_plan_json,
                requirement_json=requirement_result.requirement_json,
                diagnostics=ctx.diagnostics,
            )
            score = prq.get("score", 0)
            
            if score > best_prq_score:
                best_prq_score = score
                best_execution = execution_result
                best_review = review_result
                best_generation = generation_result
                best_prq = prq
                
            if score >= 90:
                break
                
            previous_feedback = review_result.review_report
            
        execution_result = best_execution
        review_result = best_review
        generation_result = best_generation
        prq = best_prq

        artifacts = self._run_timed_stage(
            ctx,
            "artifacts",
            lambda e=execution_result, r=review_result: self.artifact_stage.save_generated(
                ctx,
                planning_result,
                e,
                r,
            ),
        )
        
        ctx.diagnostics["post_review_quality_score"] = prq.get("score", 0)
        ctx.diagnostics["post_review_quality_verdict"] = prq.get("verdict", "")
        ctx.diagnostics["post_review_quality_gate"] = prq.get("quality_gate", "")

        prq_score = int(prq.get("score", 0))
        prq_verdict = str(prq.get("verdict", ""))
        review_attempt = int(ctx.diagnostics.get("review_loop_attempt", 1))
        score_label = f"{prq_score}/100"
        verdict_emoji = "✅" if prq_score >= 90 else ("⚠️" if prq_score >= 60 else "❌")
        self.deps.emit_progress(
            ctx.progress,
            ctx.progress_callback,
            "9",
            "Post-Review Quality",
            "rule-based scorer",
            f"{verdict_emoji} {prq_verdict}",
            f"Điểm chất lượng tổng thể: {score_label} (vòng lặp {review_attempt}/{3}).",
        )
        
        self._finalize_diagnostics(ctx)

        return PipelineResult(
            context=rag_result.context,
            docs_context=rag_result.docs_context,
            source_context=rag_result.source_context,
            requirement_json=requirement_result.requirement_json,
            test_plan_json=planning_result.test_plan_json,
            test_case_rows=planning_result.test_case_rows,
            generated_code=execution_result.generated_code,
            review_report=review_result.review_report,
            review_target_code=review_result.review_target_code,
            review_target_label=review_result.review_target_label,
            code_path=artifacts.code_path,
            test_plan_path=artifacts.test_plan_path,
            review_path=artifacts.review_path,
            review_md_path=artifacts.review_md_path,
            coverage_report_path=artifacts.coverage_report_path,
            coverage_json_path=artifacts.coverage_json_path,
            coverage_raw_path=artifacts.coverage_raw_path,
            pytest_log_path=artifacts.pytest_log_path,
            collection_log_path=artifacts.collection_log_path,
            run_id=ctx.run_id,
            framework=input_data.framework,
            test_technique=input_data.test_technique,
            mode=profile.mode_label,
            backend=backend,
            embedding_backend=embedding_backend,
            embed_model=profile.embed_model,
            requirement_model=profile.requirement_model,
            planning_model=profile.planning_model,
            generator_model=profile.generator_model,
            review_model=profile.review_model,
            workflow=input_data.workflow_mode,
            workflow_label=self.deps.workflow_label(input_data.workflow_mode),
            progress=ctx.progress,
            execution_summary=execution_result.execution_summary,
            diagnostics=ctx.diagnostics,
            new_docs_signature=rag_result.docs_new_signature,
            new_source_signature=rag_result.source_new_signature,
            post_review_quality=prq,
        )
