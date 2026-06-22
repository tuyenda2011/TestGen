import pytest
from testgen.analyzer.ast_analyzer import AdvancedASTAnalyzer, FunctionInfo, ClassInfo

def test_ast_analyzer_syntax_error():
    analyzer = AdvancedASTAnalyzer("def 123_invalid(): pass")
    assert analyzer.tree is None
    assert "SyntaxError" in analyzer.syntax_error
    classes, functions, imports = analyzer.extract_info()
    assert classes == []
    assert functions == []
    assert imports == []
    summary = analyzer.get_context_summary()
    assert "SyntaxError" in summary
    assert "AST" in summary

def test_ast_analyzer_imports():
    code = """
import os
import sys, math
from pathlib import Path
from dataclasses import dataclass, field
"""
    analyzer = AdvancedASTAnalyzer(code)
    _, _, imports = analyzer.extract_info()
    assert "os" in imports
    assert "sys" in imports
    assert "math" in imports
    assert "pathlib.Path" in imports
    assert "dataclasses.dataclass" in imports

def test_ast_analyzer_classes_and_functions():
    code = """
class MyClass:
    def my_method(self, a, b):
        if a > b:
            raise ValueError("a cannot be greater than b")
        return a + b

def my_func(x):
    if x < 0:
        raise ValueError("x must be positive")
    if x == 0:
        return 0
    return x * 2
"""
    analyzer = AdvancedASTAnalyzer(code)
    classes, functions, imports = analyzer.extract_info()
    
    assert len(classes) == 1
    assert classes[0].name == "MyClass"
    assert len(classes[0].methods) == 1
    assert classes[0].methods[0].name == "my_method"
    assert classes[0].methods[0].params == ["self", "a", "b"]
    assert len(classes[0].methods[0].conditions) == 1
    assert "a > b" in classes[0].methods[0].conditions[0]
    assert len(classes[0].methods[0].exceptions) == 1
    assert classes[0].methods[0].has_return_value is True
    
    assert len(functions) == 1
    assert functions[0].name == "my_func"
    assert functions[0].params == ["x"]
    assert len(functions[0].conditions) == 2
    assert "x < 0" in functions[0].conditions[0]
    assert "x == 0" in functions[0].conditions[1]
    assert len(functions[0].exceptions) == 1
    assert functions[0].has_return_value is True

def test_get_context_summary():
    code = """
import os

class User:
    def get_age(self, user_id):
        if not user_id:
            raise ValueError("Empty")
        pass

def helper(a):
    if a:
        raise Exception("error")
"""
    analyzer = AdvancedASTAnalyzer(code)
    summary = analyzer.get_context_summary()
    assert "CHI TIẾT CẤU TRÚC" in summary
    assert "Dependencies/Imports phát hiện: os" in summary
    assert "[Class]: User" in summary
    assert "Method: get_age(self, user_id)" in summary
    assert "if not user_id" in summary
    assert "raise ValueError('Empty')" in summary
    assert "[Function độc lập]: helper(a)" in summary
    assert "if a" in summary
    assert "raise Exception('error')" in summary


def test_tree_sitter_context_summary_for_java():
    code = "public class Calculator { int add(int a, int b) { return a + b; } }"
    analyzer = AdvancedASTAnalyzer(code, language="java", source_name="Calculator.java")

    summary = analyzer.get_context_summary()

    assert "TREE-SITTER" in summary
    assert "java_class" in summary
    assert "Calculator" in summary
    assert "java_method" in summary
    assert "add" in summary


def test_tree_sitter_context_summary_for_javascript():
    code = "class Cart { total(a, b) { return a + b; } }\nconst tax = (value) => value * 0.1;"
    analyzer = AdvancedASTAnalyzer(code, language="javascript", source_name="cart.js")

    summary = analyzer.get_context_summary()

    assert "TREE-SITTER" in summary
    assert "javascript_class" in summary
    assert "Cart" in summary
    assert "javascript_function" in summary
    assert "tax" in summary
