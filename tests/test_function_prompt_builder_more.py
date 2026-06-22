import pytest
from testgen.prompts import function_prompt_builder as builder

def test_target_slug():
    assert builder.target_slug("MyClass.my_method!") == "myclass_my_method"
    assert builder.target_slug("!") == "target"

def test_source_segment_fallback():
    class DummyNode:
        lineno = 2
        end_lineno = 3
    assert builder.source_segment("code", ["line1", "line2", "line3"], DummyNode()) == "line2\nline3"
    assert builder.source_segment("code", ["line1"], object()) == ""

def test_safe_unparse():
    assert builder.safe_unparse(None) == ""
    class BadNode: pass
    assert builder.safe_unparse(BadNode()) == ""

def test_module_context():
    assert builder.module_context("invalid syntax !!", []) == ""
    code = "import a\nx = 1\ndef f(): pass"
    res = builder.module_context(code, code.splitlines())
    assert "import a" in res
    assert "x = 1" in res
    assert "def f" not in res
    
    # Truncation
    code_long = "import a\n" + "x = 1\n" * 1000
    res_long = builder.module_context(code_long, code_long.splitlines(), max_chars=50)
    assert "truncated" in res_long

def test_target_names():
    import ast
    node = ast.parse("a, b = 1, 2").body[0].targets[0]
    assert builder.target_names(node) == ["a", "b"]
    assert builder.target_names(ast.parse("1").body[0].value) == []

def test_module_context_symbols():
    import ast
    tree = ast.parse("import os.path as p\nfrom math import *\nfrom sys import exit as e\na, b = 1, 2\nc: int = 3")
    syms = builder.module_context_symbols(tree)
    assert "p" in syms
    assert "e" in syms
    assert "a" in syms
    assert "b" in syms
    assert "c" in syms
    
    # Truncation
    tree2 = ast.parse("\n".join(f"x{i} = {i}" for i in range(20)))
    syms2 = builder.module_context_symbols(tree2, max_symbols=2)
    assert len(syms2) == 2

def test_source_import_statement():
    assert builder.source_import_statement("clamp", ["clamp", "LIMIT", "__private"]) == "from source_under_test import clamp, LIMIT"

def test_class_constructor_signature():
    import ast
    tree = ast.parse("class A:\n def m(): pass")
    assert builder.class_constructor_signature(tree.body[0]) == ""
    
    tree2 = ast.parse("class B:\n def __init__(self, x): pass")
    assert builder.class_constructor_signature(tree2.body[0]) == "__init__(self, x)"

def test_dependency_names():
    import ast
    tree = ast.parse("def f(x):\n y = 1\n z = x + w + True")
    assert builder.dependency_names(tree.body[0], ["x"]) == ["w"]

def test_method_kind_and_call_hint():
    assert builder.method_kind(["staticmethod"]) == "staticmethod"
    assert builder.method_kind(["classmethod"]) == "classmethod"
    assert builder.method_kind(["property"]) == "property"
    assert builder.method_kind(["other"]) == "instance"
    
    assert builder.class_call_hint("A", "m", "staticmethod") == "Call A.m(...) directly."
    assert builder.class_call_hint("A", "m", "classmethod") == "Call A.m(...) directly and assert the returned value/object."
    assert builder.class_call_hint("A", "m", "property") == "Instantiate A with valid constructor args, then assert instance.m."
    assert builder.class_call_hint("A", "m", "instance") == "Instantiate A with valid constructor args, then call instance.m(...)."

def test_extract_python_functions_edges():
    assert builder.extract_python_functions("") == []
    assert builder.extract_python_functions("invalid !!") == []
    
    code = "class A:\n def __init__(self): pass\n def m(self): pass"
    res = builder.extract_python_functions(code)
    assert len(res) == 1
    assert res[0].name == "m"
    assert res[0].owner_class == "A"
    
    # Long class truncates
    long_code = "class B:\n" + " x=1\n"*1000 + " def m(self): pass"
    res2 = builder.extract_python_functions(long_code)
    assert "truncated" in res2[0].context_source

def test_select_functions_for_lines():
    code = "def f():\n pass\ndef g():\n pass"
    res = builder.select_functions_for_lines(code, [1])
    assert len(res) == 1
    assert res[0].name == "f"
    
    res2 = builder.select_functions_for_lines(code, ["bad", 3])
    assert len(res2) == 1
    assert res2[0].name == "g"
    
    assert builder.select_functions_for_lines(code, []) == []

def test_build_function_level_prompt():
    funcs = builder.extract_python_functions("def f(): pass")
    prompt = builder.build_function_level_prompt(
        requirement_json="r",
        test_plan_json="p",
        function_info=funcs[0],
        test_technique="Black-box"
    )
    assert "Target: f" in prompt
    assert "Black-box" in prompt
    assert "r" in prompt
    assert "p" in prompt
