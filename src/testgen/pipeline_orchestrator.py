from __future__ import annotations

from typing import Any

from testgen.agents.code_generator_agent import (
    estimate_test_generation_llm_calls,
    generate_targeted_pytest_code,
    generate_targeted_junit_code,
    generate_targeted_jest_code,
    generate_test_code,
    heal_pytest_code,
    heal_jest_code,
    heal_junit_code,
    heal_postman_code,
)
from testgen.agents.code_reviewer_agent import review_test_code
from testgen.agents.formatter_agent import (
    create_run_id,
    parse_test_plan_rows,
    save_combined_coverage_report,
    save_generated_code,
    save_review_report,
    save_test_plan_excel,
)
from testgen.executors.pytest_runner import (
    execution_result_score,
    run_generated_pytest_with_coverage,
)
from testgen.agents.requirement_agent import analyze_requirements
from testgen.agents.test_planning_agent import generate_test_plan
from testgen.core.config import DOC_COLLECTION_NAME, SOURCE_COLLECTION_NAME
from testgen.core.constants import workflow_label
from testgen.core.language_guard import validate_framework_sections
from testgen.core.logger import get_logger
from testgen.core.models import PipelineInput, PipelineProfile, PipelineResult
from testgen.core.pipeline_services import (
    build_rag_context,
    clip_text,
    collection_count,
    combine_sections,
    merge_contexts,
    python_source_for_generation,
    retrieve_preindexed_rag_context,
)
from testgen.core.utils import normalize_text
from testgen.pipeline.stages import (
    PipelineDependencies,
    PipelineRunner,
    coerce_rag_result as _coerce_rag_result,
    coerce_review_paths as _coerce_review_paths,
    emit_progress as _emit_progress,
    format_execution_issue_for_review as _format_execution_issue_for_review,
    format_missing_lines_snippet as _format_missing_lines_snippet,
)
from testgen.rag.document_loader import (
    load_text_uploaded_file_entries,
    load_uploaded_file_entries,
)
from testgen.rag.retriever import retrieve_context
from testgen.rag.vector_store import get_collection
from testgen.run_history import persist_run_history
from testgen.workflow import resolve_retrieval_source

logger = get_logger(__name__)


def _make_dependencies() -> PipelineDependencies:
    return PipelineDependencies(
        create_run_id=create_run_id,
        emit_progress=_emit_progress,
        normalize_text=normalize_text,
        clip_text=clip_text,
        combine_sections=combine_sections,
        load_uploaded_file_entries=load_uploaded_file_entries,
        load_text_uploaded_file_entries=load_text_uploaded_file_entries,
        validate_framework_sections=validate_framework_sections,
        resolve_retrieval_source=resolve_retrieval_source,
        workflow_label=workflow_label,
        build_rag_context=build_rag_context,
        retrieve_preindexed_rag_context=retrieve_preindexed_rag_context,
        collection_count=collection_count,
        merge_contexts=merge_contexts,
        python_source_for_generation=python_source_for_generation,
        analyze_requirements=analyze_requirements,
        generate_test_plan=generate_test_plan,
        parse_test_plan_rows=parse_test_plan_rows,
        estimate_test_generation_llm_calls=estimate_test_generation_llm_calls,
        generate_test_code=generate_test_code,
        generate_targeted_pytest_code=generate_targeted_pytest_code,
        heal_pytest_code=heal_pytest_code,
        generate_targeted_junit_code=generate_targeted_junit_code,
        generate_targeted_jest_code=generate_targeted_jest_code,
        heal_jest_code=heal_jest_code,
        heal_junit_code=heal_junit_code,
        heal_postman_code=heal_postman_code,
        review_test_code=review_test_code,
        save_generated_code=save_generated_code,
        save_test_plan_excel=save_test_plan_excel,
        save_review_report=save_review_report,
        save_combined_coverage_report=save_combined_coverage_report,
        persist_run_history=persist_run_history,
        run_generated_pytest_with_coverage=run_generated_pytest_with_coverage,
        execution_result_score=execution_result_score,
        doc_collection_name=DOC_COLLECTION_NAME,
        source_collection_name=SOURCE_COLLECTION_NAME,
    )


def run_pipeline(
    input_data: PipelineInput | dict[str, Any] | None = None,
    profile: PipelineProfile | dict[str, str] | None = None,
    progress_callback=None,
    cancel_check=None,
    **kwargs: Any,
) -> PipelineResult | dict[str, Any]:
    helpers = kwargs.pop("helpers", None) or {}
    legacy_call = input_data is None

    if input_data is None:
        input_fields = set(PipelineInput.model_fields)
        input_payload = {
            key: kwargs.pop(key)
            for key in list(kwargs)
            if key in input_fields
        }
        input_data = PipelineInput(**input_payload)
    elif isinstance(input_data, dict):
        input_data = PipelineInput(**input_data)

    if profile is None:
        raise TypeError("run_pipeline() missing required argument: 'profile'")
    if isinstance(profile, dict):
        profile = PipelineProfile(**profile)

    if kwargs:
        unexpected = next(iter(kwargs))
        raise TypeError(f"run_pipeline() got an unexpected keyword argument '{unexpected}'")

    helper_globals = {
        "_normalize_text": "normalize_text",
        "_clip_text": "clip_text",
        "_combine_sections": "combine_sections",
        "_build_rag_context": "build_rag_context",
        "_retrieve_preindexed_rag_context": "retrieve_preindexed_rag_context",
        "_collection_count": "collection_count",
        "_merge_contexts": "merge_contexts",
        "_workflow_label": "workflow_label",
        "_python_source_for_generation": "python_source_for_generation",
        "DOC_COLLECTION_NAME": "DOC_COLLECTION_NAME",
        "SOURCE_COLLECTION_NAME": "SOURCE_COLLECTION_NAME",
    }
    originals: dict[str, Any] = {}
    for helper_key, global_name in helper_globals.items():
        if helper_key in helpers:
            originals[global_name] = globals()[global_name]
            globals()[global_name] = helpers[helper_key]

    try:
        result = _run_pipeline_model(input_data, profile, progress_callback, cancel_check)
    finally:
        for global_name, value in originals.items():
            globals()[global_name] = value

    if legacy_call:
        return result.model_dump()
    return result


def _run_pipeline_model(
    input_data: PipelineInput,
    profile: PipelineProfile,
    progress_callback=None,
    cancel_check=None,
) -> PipelineResult:
    return PipelineRunner(_make_dependencies()).run(input_data, profile, progress_callback, cancel_check)
