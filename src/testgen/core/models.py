from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field

class PipelineCancelledError(Exception):
    pass

class PipelineInput(BaseModel):
    requirement_text: str = ""
    docs_files: list[Any] = Field(default_factory=list)
    source_code_text: str = ""
    source_files: list[Any] = Field(default_factory=list)
    test_code_text: str = ""
    test_files: list[Any] = Field(default_factory=list)
    retrieval_query: str = ""
    framework: str = "pytest"
    test_technique: str = "Hybrid"
    workflow_mode: str = "generate_tests"
    api_key: str = ""
    use_preindexed_docs: bool = False
    previous_docs_signature: str = ""
    previous_source_signature: str = ""

class PipelineProfile(BaseModel):
    backend: str
    mode_label: str
    requirement_model: str
    planning_model: str
    generator_model: str
    review_model: str
    embed_model: str
    embedding_backend: str = ""

class PipelineResult(BaseModel):
    context: str = ""
    docs_context: str = ""
    source_context: str = ""
    requirement_json: str = ""
    test_plan_json: str = ""
    test_case_rows: list[dict[str, str]] = Field(default_factory=list)
    generated_code: str = ""
    review_report: str = ""
    review_target_code: str = ""
    review_target_label: str = ""
    code_path: str = ""
    test_plan_path: str = ""
    review_path: str = ""
    review_md_path: str = ""
    coverage_report_path: str = ""
    coverage_json_path: str = ""
    coverage_raw_path: str = ""
    pytest_log_path: str = ""
    collection_log_path: str = ""
    run_id: str = ""
    framework: str = ""
    test_technique: str = ""
    mode: str = ""
    backend: str = ""
    embed_model: str = ""
    embedding_backend: str = ""
    requirement_model: str = ""
    planning_model: str = ""
    generator_model: str = ""
    review_model: str = ""
    workflow: str = ""
    workflow_label: str = ""
    progress: list[dict[str, str]] = Field(default_factory=list)
    execution_summary: dict[str, Any] = Field(default_factory=dict)
    diagnostics: dict[str, Any] = Field(default_factory=dict)
    new_docs_signature: str = ""
    new_source_signature: str = ""
    post_review_quality: dict[str, Any] = Field(default_factory=dict)
