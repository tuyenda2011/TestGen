import pytest
from unittest.mock import patch

from testgen.agents import requirement_agent
from testgen.agents import test_planning_agent
from testgen.agents import code_reviewer_agent
from testgen.agents import formatter_agent

def test_requirement_ensure_valid_json():
    with pytest.raises(ValueError):
        requirement_agent._ensure_valid_requirement_json("bad")
    
    valid_json = '{"module": "mod", "features": [], "inputs": [], "outputs": [], "business_rules": [], "validations": [], "assumptions": [], "missing_information": []}'
    assert requirement_agent._ensure_valid_requirement_json(valid_json) == valid_json

def test_formatter_save_code(tmp_path):
    with patch("testgen.agents.formatter_agent.OUTPUT_PATH", tmp_path):
        path = formatter_agent.save_generated_code("code", "pytest")
        assert "ma_kiem_thu" in path

def test_formatter_save_combined_coverage(tmp_path):
    with patch("testgen.agents.formatter_agent.OUTPUT_PATH", tmp_path):
        md, json_p, raw = formatter_agent.save_combined_coverage_report({"passed": True, "coverage_percent": 100})
        assert "combined_coverage" in md
        assert "combined_coverage" in json_p

def test_formatter_save_review_report(tmp_path):
    with patch("testgen.agents.formatter_agent.OUTPUT_PATH", tmp_path):
        pdf, md = formatter_agent.save_review_report("review")
        assert "bao_cao_phan_tich" in pdf

def test_formatter_save_test_plan_excel(tmp_path):
    with patch("testgen.agents.formatter_agent.OUTPUT_PATH", tmp_path):
        xlsx = formatter_agent.save_test_plan_excel('{"test_scenarios": [{"id": 1}]}')
        assert "ke_hoach_kiem_thu" in xlsx
