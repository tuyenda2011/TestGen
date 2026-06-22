import pytest
from testgen.agents.code_generator_agent import (
    _strip_markdown_code_fences,
    _ensure_pytest_import,
    _deduplicate_top_level_imports,
    _ensure_required_import,
    _extract_python_functions,
    estimate_test_generation_llm_calls,
    _module_context_symbols,
    _safe_unparse
)
import ast

def test_strip_markdown_code_fences_mixed():
    text = "Here is the code:\n```python\ndef a(): pass\n```\nMore text."
    cleaned = _strip_markdown_code_fences(text)
    assert "def a(): pass" in cleaned
    assert "Here is the code:" not in cleaned

def test_ensure_pytest_import_edges():
    assert _ensure_pytest_import("") == ""
    assert _ensure_pytest_import("import pytest\ndef test_a(): pass") == "import pytest\ndef test_a(): pass"
    assert "import pytest" in _ensure_pytest_import("pytest.raises(ValueError)")

def test_deduplicate_top_level_imports():
    code = "import os\nimport sys\nimport os\nfrom pathlib import Path\ndef x():\n    import os"
    dedup = _deduplicate_top_level_imports(code)
    assert dedup.count("import os") == 2 # One top level, one inside func
    assert "import sys" in dedup

def test_ensure_required_import():
    assert _ensure_required_import("", "import math") == ""
    assert _ensure_required_import("import math", "import math") == "import math"
    assert "import sys" in _ensure_required_import("import math", "import sys")

def test_extract_python_functions_invalid():
    assert _extract_python_functions("") == []
    assert _extract_python_functions("def 123invalid(): pass") == []

def test_estimate_test_generation_llm_calls():
    assert estimate_test_generation_llm_calls("JUnit", "def a(): pass") == 1
    assert estimate_test_generation_llm_calls("pytest", "") == 1
    assert estimate_test_generation_llm_calls("pytest", "def a(): pass\ndef b(): pass") == 1

def test_module_context_symbols():
    tree = ast.parse("import os\nfrom sys import exit as sys_exit\nx = 1\ny: int = 2\n")
    symbols = _module_context_symbols(tree)
    assert "os" in symbols
    assert "sys_exit" in symbols
    assert "x" in symbols
    assert "y" in symbols

def test_safe_unparse():
    assert _safe_unparse(None) == ""
