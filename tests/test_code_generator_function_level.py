from __future__ import annotations

from testgen.agents import code_generator_agent


def test_generate_test_code_uses_function_level_for_pytest(monkeypatch):
    captured_prompts: list[str] = []

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured_prompts.append(prompt)
        return (
            "# ===== Tests for add =====\n"
            "def test_add_ok():\n"
            "    assert add(1, 2) == 3\n\n"
            "# ===== Tests for sub =====\n"
            "def test_sub_ok():\n"
            "    assert sub(5, 3) == 2\n"
        )

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"math"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        test_technique="White-box",
        backend="gemini",
        api_key="test-key",
        source_code_text=(
            "def add(a, b):\n"
            "    return a + b\n\n"
            "def sub(a, b):\n"
            "    return a - b\n"
        ),
    )

    assert "Tests for add" in generated
    assert "Tests for sub" in generated
    assert "from source_under_test import add" in generated
    assert "from source_under_test import sub" in generated
    assert "def test_add_ok()" in generated
    assert "def test_sub_ok()" in generated
    assert len(captured_prompts) == 1
    assert "BATCH of Python targets" in captured_prompts[0]
    assert "Do not rely on fixtures" in captured_prompts[0]


def test_generate_test_code_fallback_for_non_pytest(monkeypatch):
    captured: dict[str, str] = {}

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured["prompt"] = prompt
        captured["backend"] = backend
        return "public class ExampleTest {}"

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"math"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="JUnit",
        backend="gemini",
        api_key="test-key",
        source_code_text="def add(a, b):\n    return a + b\n",
    )

    assert generated == "public class ExampleTest {}"
    assert "Framework" in captured["prompt"]
    assert "JUnit" in captured["prompt"]
    assert captured["backend"] == "gemini"


def test_generate_test_code_removes_markdown_fences_and_adds_pytest_import(monkeypatch):
    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        return (
            "```python\n"
            "def test_add_negative():\n"
            "    with pytest.raises(ValueError):\n"
            "        add(1, -1)\n"
            "```\n"
        )

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"math"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        backend="ollama",
        source_code_text=(
            "def add(a, b):\n"
            "    if b < 0:\n"
            "        raise ValueError('neg')\n"
            "    return a + b\n"
        ),
    )

    assert "```" not in generated
    assert "import pytest" in generated
    assert "with pytest.raises(ValueError):" in generated


def test_generate_test_code_extracts_class_methods_with_context(monkeypatch):
    captured_prompts: list[str] = []

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured_prompts.append(prompt)
        if "Target: Wallet.withdraw" in prompt:
            return (
                "def test_wallet_withdraw_ok():\n"
                "    wallet = Wallet(100)\n"
                "    assert wallet.withdraw(40) == 60\n"
            )
        return "def test_other():\n    assert True\n"

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"wallet"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        backend="ollama",
        source_code_text=(
            "class Wallet:\n"
            "    def __init__(self, balance):\n"
            "        self.balance = balance\n\n"
            "    def withdraw(self, amount):\n"
            "        if amount <= 0:\n"
            "            raise ValueError('positive amount required')\n"
            "        if amount > self.balance:\n"
            "            raise ValueError('insufficient funds')\n"
            "        self.balance -= amount\n"
            "        return self.balance\n"
        ),
    )

    assert "Tests for Wallet.withdraw" in generated
    assert "from source_under_test import Wallet" in generated
    assert "Wallet(100)" in generated
    assert len(captured_prompts) == 1
    assert "def __init__(self, balance)" in captured_prompts[0]
    assert "amount > self.balance" in captured_prompts[0]
    assert "ValueError('insufficient funds')" in captured_prompts[0]


def test_generate_test_code_includes_module_context_in_prompt(monkeypatch):
    captured: dict[str, str] = {}

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured["prompt"] = prompt
        return "def test_clamp_high():\n    assert clamp(20) == LIMIT\n"

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"limits"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        backend="ollama",
        source_code_text=(
            "LIMIT = 10\n\n"
            "def clamp(value):\n"
            "    if value > LIMIT:\n"
            "        return LIMIT\n"
            "    return value\n"
        ),
    )

    assert "LIMIT = 10" in captured["prompt"]
    assert "Returns detected" in captured["prompt"]
    assert "from source_under_test import clamp" in generated
    assert "LIMIT" in generated


def test_generate_test_code_prefixes_generic_test_names_per_target(monkeypatch):
    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        return (
            "# ===== Tests for add =====\n"
            "def test_ok():\n"
            "    assert add(1, 2) == 3\n\n"
            "# ===== Tests for sub =====\n"
            "def test_ok():\n"
            "    assert sub(3, 1) == 2\n"
        )

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"math"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        backend="ollama",
        source_code_text=(
            "def add(a, b):\n"
            "    return a + b\n\n"
            "def sub(a, b):\n"
            "    return a - b\n"
        ),
    )

    assert "def test_add_ok()" in generated
    assert "def test_sub_ok()" in generated
    assert "def test_ok()" not in generated


def test_prefix_pytest_test_names_preserves_class_indentation():
    code = (
        "class TestCalculator:\n"
        "    def test_ok(self):\n"
        "        assert add(1, 2) == 3\n\n"
        "    async def test_async_ok(self):\n"
        "        assert await run_add(1, 2) == 3\n"
    )

    generated = code_generator_agent._prefix_pytest_test_names(code, "Calculator.add")

    assert "    def test_calculator_add_ok(self):" in generated
    assert "    async def test_calculator_add_async_ok(self):" in generated
    assert "\ndef test_calculator_add_ok" not in generated


def test_generate_test_code_batches_pytest_targets(monkeypatch):
    captured_prompts: list[str] = []

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured_prompts.append(prompt)
        sections: list[str] = []
        for name in ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"]:
            if f"Target: {name}(" in prompt:
                sections.append(
                    f"# ===== Tests for {name} =====\n"
                    f"def test_{name}_ok():\n"
                    f"    assert {name}(1) == 1\n"
                )
        return "\n\n".join(sections)

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    source = "\n\n".join(f"def f{index}(value):\n    return value\n" for index in range(1, 9))

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"batch"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        backend="ollama",
        source_code_text=source,
    )

    assert len(captured_prompts) == 2
    assert "def test_f1_ok()" in generated
    assert "def test_f8_ok()" in generated
    assert "from source_under_test import f1" in generated
    assert "from source_under_test import f8" in generated


def test_function_level_prompt_includes_constructor_dependency_and_test_prefix(monkeypatch):
    captured_prompts: list[str] = []

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured_prompts.append(prompt)
        return "def test_ok():\n    assert Wallet(10).withdraw(1) == 9\n"

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_test_code(
        requirement_json='{"module":"wallet"}',
        test_plan_json='{"test_scenarios":[]}',
        framework="pytest",
        backend="ollama",
        source_code_text=(
            "class Wallet:\n"
            "    def __init__(self, balance):\n"
            "        self.balance = balance\n\n"
            "    def withdraw(self, amount):\n"
            "        if amount > self.balance:\n"
            "            raise ValueError('insufficient funds')\n"
            "        return self.balance - amount\n"
        ),
    )

    assert "def test_wallet_withdraw_ok()" in generated
    assert "Constructor signature (if class): __init__(self, balance)" in captured_prompts[0]
    assert "Required test function prefix: test_wallet_withdraw_" in captured_prompts[0]
    assert "- ValueError" in captured_prompts[0]


def test_generate_targeted_pytest_code_uses_missing_line_function(monkeypatch):
    captured_prompts: list[str] = []

    def fake_call_llm_chat(*, prompt, system_prompt, backend, model, api_key=None, agent_type=None):
        assert agent_type == "code_generator"
        captured_prompts.append(prompt)
        return (
            "# ===== Tests for withdraw =====\n"
            "def test_withdraw_rejects_zero():\n"
            "    with pytest.raises(ValueError):\n"
            "        withdraw(100, 0)\n"
        )

    monkeypatch.setattr(code_generator_agent, "call_llm_chat", fake_call_llm_chat)

    generated = code_generator_agent.generate_targeted_pytest_code(
        requirement_json='{"module":"bank"}',
        test_plan_json='{"test_scenarios":[]}',
        test_technique="White-box",
        source_code_text=(
            "def deposit(balance, amount):\n"
            "    return balance + amount\n\n"
            "def withdraw(balance, amount):\n"
            "    if amount <= 0:\n"
            "        raise ValueError('positive amount required')\n"
            "    return balance - amount\n"
        ),
        missing_lines=[5],
        backend="ollama",
        retry_namespace="retry_2",
    )

    assert "Target: withdraw" in captured_prompts[0]
    assert "Target: deposit" not in captured_prompts[0]
    assert "def test_retry_2_withdraw_rejects_zero()" in generated
    assert "from source_under_test import withdraw" in generated

