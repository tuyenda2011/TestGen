import pytest
from unittest.mock import MagicMock, patch

from testgen import pipeline_orchestrator
from testgen.pipeline import stages
from testgen.core.models import PipelineInput, PipelineProfile, PipelineCancelledError

def get_dummy_profile():
    return PipelineProfile(
        backend="test", mode_label="test", requirement_model="test", 
        planning_model="test", generator_model="test", review_model="test", embed_model="test"
    )

@patch("testgen.pipeline_orchestrator._run_pipeline_model", return_value={"test": True})
def test_run_pipeline_input_dict(mock_run):
    res = pipeline_orchestrator.run_pipeline(
        input_data={"test_technique": "Black-box", "source_code_text": "code"},
        profile=get_dummy_profile(),
        helpers={"_workflow_label": lambda x: "test"}
    )
    assert res is not None

@patch("testgen.pipeline_orchestrator._run_pipeline_model", return_value={"test": True})
def test_run_pipeline_profile_dict(mock_run):
    res = pipeline_orchestrator.run_pipeline(
        input_data=PipelineInput(source_code_text="code"),
        profile={"backend":"t", "mode_label":"t", "requirement_model":"t", "planning_model":"t", "generator_model":"t", "review_model":"t", "embed_model":"t"}
    )
    assert res is not None

class MockResult:
    def model_dump(self):
        return {"test": True}

@patch("testgen.pipeline_orchestrator._run_pipeline_model", return_value=MockResult())
def test_run_pipeline_legacy_call(mock_run):
    res = pipeline_orchestrator.run_pipeline(
        profile=get_dummy_profile(),
        test_technique="Black-box",
        source_code_text="code"
    )
    assert isinstance(res, dict)

def test_run_pipeline_missing_profile():
    with pytest.raises(TypeError, match="missing required argument: 'profile'"):
        pipeline_orchestrator.run_pipeline(input_data={})

def test_run_pipeline_unexpected_kwarg():
    with pytest.raises(TypeError, match="unexpected keyword argument"):
        pipeline_orchestrator.run_pipeline(input_data={}, profile={"backend":"t", "mode_label":"t", "requirement_model":"t", "planning_model":"t", "generator_model":"t", "review_model":"t", "embed_model":"t"}, unknown=1)

def test_coerce_review_paths():
    assert stages.coerce_review_paths(["a", "b"]) == ("a", "b")
    assert stages.coerce_review_paths(["a"]) == ("a", "")
    assert stages.coerce_review_paths("a") == ("a", "")
    assert stages.coerce_review_paths(None) == ("", "")

def test_coerce_rag_result():
    with pytest.raises(ValueError):
        stages.coerce_rag_result(["invalid"])
    assert stages.coerce_rag_result(["ctx", 1, True, "sig", {"a": 1}]) == ("ctx", 1, True, "sig", {"a": 1})
    assert stages.coerce_rag_result(["ctx", 1, True]) == ("ctx", 1, True, "", {})

def test_coerce_preindexed_rag_result():
    with pytest.raises(ValueError):
        stages.coerce_preindexed_rag_result(["invalid"])
    assert stages.coerce_preindexed_rag_result(["ctx", True, {"a": 1}]) == ("ctx", True, {"a": 1})
    assert stages.coerce_preindexed_rag_result(["ctx", True]) == ("ctx", True, {})

def test_coerce_coverage_paths():
    assert stages.coerce_coverage_paths(["a", "b", "c"]) == ("a", "b", "c")
    assert stages.coerce_coverage_paths(["a", "b"]) == ("a", "b", "")
    assert stages.coerce_coverage_paths(["a"]) == ("a", "", "")
    assert stages.coerce_coverage_paths(None) == ("", "", "")

def test_format_missing_lines_snippet():
    assert stages.format_missing_lines_snippet([], "") == "[]"
    lines = [1, 2, 3, 4, 5]
    source = "a\nb\nc\nd\ne\nf"
    res = stages.format_missing_lines_snippet(lines, source, max_lines=2)
    assert "còn 3 dòng nữa" in res

def test_format_execution_issue_for_review():
    assert stages.format_execution_issue_for_review({}) == ""
    issue = {"execution_issue": {"type": "Error", "title": "T", "hint": "H", "missing_lines_count": 5}}
    res = stages.format_execution_issue_for_review(issue)
    assert "Error" in res
    assert "T" in res

def test_input_stage_no_docs_source_test():
    deps = MagicMock()
    deps.resolve_retrieval_source.return_value = ""
    deps.combine_sections.return_value = []
    
    stage = stages.InputStage(deps)
    ctx = MagicMock()
    ctx.input_data = PipelineInput()
    ctx.backend = "ollama"
    with pytest.raises(ValueError, match="Hãy nhập source code"):
        stage.run(ctx)

def test_pipeline_run_context_cancel():
    ctx = stages.PipelineRunContext(
        input_data=PipelineInput(),
        profile=get_dummy_profile(),
        run_id="1",
        backend="a",
        embedding_backend="b",
        embedding_label="c",
        cancel_check=lambda: True
    )
    with pytest.raises(PipelineCancelledError):
        ctx.check_cancelled()
