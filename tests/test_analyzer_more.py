import pytest
from testgen.analyzer.ast_analyzer import AdvancedASTAnalyzer
from testgen.analyzer.tree_sitter_adapter import parse_source_structure

def test_ast_analyzer_extract_functions():
    code = """
def func1(): pass
class A:
    def func2(): pass
    """
    analyzer = AdvancedASTAnalyzer(code)
    funcs = analyzer.extract_functions()
    assert len(funcs) == 2
    assert funcs[0].name == "func1"
    assert funcs[1].name == "func2"

def test_ast_analyzer_unsupported_language():
    analyzer = AdvancedASTAnalyzer("func()", language="ruby")
    assert analyzer.tree is None
    assert analyzer.structured_parse is None
    assert analyzer.extract_info() == ([], [], [])
    assert analyzer.extract_functions() == []
    assert analyzer.get_context_summary() == ""
    assert analyzer._extract_imports() == []

def test_ast_analyzer_empty_ast():
    analyzer = AdvancedASTAnalyzer("")
    assert analyzer.get_context_summary() == "Không tìm thấy hàm nào trong AST."

def test_ast_analyzer_structured_parse_empty():
    # Force empty structured parse
    analyzer = AdvancedASTAnalyzer("", language="java")
    # Actually java parser might return empty symbols if code is empty
    assert "Không tìm thấy class/function/method" in analyzer.get_context_summary()

def test_ast_analyzer_no_conditions_or_exceptions():
    code = """
def plain():
    return 1
    """
    analyzer = AdvancedASTAnalyzer(code)
    summary = analyzer.get_context_summary()
    assert "plain()" in summary
    assert "Có trả về giá trị (return)" in summary
