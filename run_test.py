from testgen.pipeline_orchestrator import run_pipeline
from testgen.core.models import PipelineInput, PipelineProfile
from testgen.core.constants import profile_for_mode
with open(r'D:\Chatbot\outputs\runs\tmp_execution\run_20260622_214442_640637\source_under_test.py', 'r') as f:
    src = f.read()
res = run_pipeline(PipelineInput(source_code_text=src, framework='pytest', workflow_mode='generate_tests', test_technique='White-box'), PipelineProfile(**profile_for_mode("API key")))
print("COVERAGE:", res.final_coverage)
