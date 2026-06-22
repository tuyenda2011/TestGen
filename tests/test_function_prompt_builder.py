from __future__ import annotations

from testgen.prompts.function_prompt_builder import FunctionPromptBuilder


def test_function_prompt_builder_extracts_function_metadata():
    functions = FunctionPromptBuilder.extract_python_functions(
        "LIMIT = 10\n\n"
        "def clamp(value):\n"
        "    if value > LIMIT:\n"
        "        return LIMIT\n"
        "    return value\n"
    )

    assert len(functions) == 1
    target = functions[0]
    assert target.name == "clamp"
    assert target.qualified_name == "clamp"
    assert "value > LIMIT" in target.conditions
    assert "LIMIT" in target.dependency_names
    assert target.import_statement == "from source_under_test import clamp, LIMIT"


def test_function_prompt_builder_builds_batch_prompt():
    functions = FunctionPromptBuilder.extract_python_functions(
        "class Wallet:\n"
        "    def __init__(self, balance):\n"
        "        self.balance = balance\n\n"
        "    def withdraw(self, amount):\n"
        "        if amount <= 0:\n"
        "            raise ValueError('positive amount required')\n"
        "        return self.balance - amount\n"
    )

    prompt = FunctionPromptBuilder.build_function_batch_prompt(
        requirement_json='{"module":"wallet"}',
        test_plan_json='{"test_scenarios":[]}',
        function_infos=functions,
        test_technique="White-box",
    )

    assert "Target: Wallet.withdraw" in prompt
    assert "Constructor signature (if class): __init__(self, balance)" in prompt
    assert "amount <= 0" in prompt
    assert "ValueError('positive amount required')" in prompt
    assert "Do not rely on fixtures" in prompt

