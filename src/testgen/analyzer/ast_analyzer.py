import ast
import textwrap
from dataclasses import dataclass, field

from testgen.analyzer.tree_sitter_adapter import parse_source_structure, normalize_source_language


@dataclass
class FunctionInfo:
    name: str
    params: list[str]
    source: str
    conditions: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    has_return_value: bool = False


@dataclass
class ClassInfo:
    name: str
    methods: list[FunctionInfo] = field(default_factory=list)


class AdvancedASTAnalyzer:
    def __init__(self, source_code: str, language: str = "python", source_name: str = ""):
        self.source_code = source_code
        self.language = normalize_source_language(language, source_name)
        self.source_name = source_name
        self.syntax_error = ""
        self.tree = None
        self.structured_parse = None
        if self.language == "python":
            try:
                self.tree = ast.parse(source_code)
            except SyntaxError as exc:
                self.syntax_error = self._format_syntax_error(exc)
        elif self.language in {"java", "javascript", "typescript"}:
            self.structured_parse = parse_source_structure(source_code, self.language, source_name=source_name)
        self.lines = source_code.splitlines()

    def get_context_summary(self) -> str:
        if self.syntax_error:
            return "\n".join(
                [
                    "--- CHI TIẾT CẤU TRÚC TỪ AST ANALYZER ---",
                    f"[SyntaxError]: {self.syntax_error}",
                    "Source code có lỗi cú pháp nên không thể trích xuất cây AST đầy đủ.",
                    "------------------------------------------",
                ]
            )
        if self.structured_parse is not None:
            return self._get_structured_context_summary()
        if self.tree is None:
            return ""

        classes, functions, imports = self.extract_info()
        if not classes and not functions and not imports:
            return "Không tìm thấy hàm nào trong AST."

        summary = ["--- CHI TIẾT CẤU TRÚC TỪ AST ANALYZER ---"]
        if imports:
            summary.append(f"Dependencies/Imports phát hiện: {', '.join(imports)}")
        for cls in classes:
            summary.append(f"[Class]: {cls.name}")
            for method in cls.methods:
                self._append_function_summary(summary, method, prefix="Method")
        for func in functions:
            self._append_function_summary(summary, func, prefix="[Function độc lập]")
        summary.append("------------------------------------------")
        return "\n".join(summary)

    def _format_syntax_error(self, exc: SyntaxError) -> str:
        location = []
        if self.source_name:
            location.append(self.source_name)
        if exc.lineno:
            location.append(f"line {exc.lineno}")
        if exc.offset:
            location.append(f"column {exc.offset}")
        where = f" ({', '.join(location)})" if location else ""
        return f"SyntaxError{where}: {exc.msg}"

    def _get_structured_context_summary(self) -> str:
        parsed = self.structured_parse
        if parsed is None:
            return ""
        summary = ["--- CHI TIẾT CẤU TRÚC TỪ TREE-SITTER ANALYZER ---"]
        summary.append(f"Ngôn ngữ: {parsed.language}")
        summary.append(f"Parser: {parsed.parser_backend}")
        if parsed.syntax_error:
            summary.append(f"[SyntaxError]: {parsed.syntax_error}")
        if not parsed.symbols:
            summary.append("Không tìm thấy class/function/method nào trong cây cú pháp.")
            summary.append("------------------------------------------")
            return "\n".join(summary)
        for symbol in parsed.symbols:
            summary.append(f"[{symbol.kind}]: {symbol.name} (lines {symbol.line_start}-{symbol.line_end})")
            if getattr(symbol, "params", None):
                summary.append(f"  Tham số: {', '.join(symbol.params)}")
            if getattr(symbol, "conditions", None):
                summary.append("  Các nhánh điều kiện:")
                for condition in symbol.conditions:
                    summary.append(f"    - if {condition}")
            if getattr(symbol, "exceptions", None):
                summary.append("  Ném ngoại lệ (Throw):")
                for exception in symbol.exceptions:
                    summary.append(f"    - throw {exception}")
            if getattr(symbol, "has_return_value", False):
                summary.append("  Có trả về giá trị (return)")
        summary.append("------------------------------------------")
        return "\n".join(summary)

    def extract_info(self) -> tuple[list[ClassInfo], list[FunctionInfo], list[str]]:
        if self.tree is None:
            return [], [], []

        classes: list[ClassInfo] = []
        functions: list[FunctionInfo] = []
        imports = self._extract_imports()

        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                methods = [
                    self._extract_function_info(child)
                    for child in node.body
                    if isinstance(child, ast.FunctionDef)
                ]
                classes.append(ClassInfo(name=node.name, methods=methods))
            elif isinstance(node, ast.FunctionDef):
                functions.append(self._extract_function_info(node))

        return classes, functions, imports

    def extract_functions(self) -> list[FunctionInfo]:
        functions = []
        if self.tree is not None:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    info = self._extract_function_info(node)
                    functions.append(info)
        elif self.structured_parse is not None:
            for symbol in self.structured_parse.symbols:
                if "function" in symbol.kind or "method" in symbol.kind:
                    info = FunctionInfo(
                        name=symbol.name,
                        params=list(getattr(symbol, "params", [])),
                        source=symbol.source,
                        conditions=list(getattr(symbol, "conditions", [])),
                        exceptions=list(getattr(symbol, "exceptions", [])),
                        has_return_value=getattr(symbol, "has_return_value", False)
                    )
                    functions.append(info)
        return functions

    def _extract_function_info(self, node: ast.FunctionDef) -> FunctionInfo:
        params = [arg.arg for arg in node.args.args]
        source = self._get_function_source(node)
        conditions = self._extract_conditions(node)
        exceptions = self._extract_exceptions(node)
        has_return_value = self._has_return_value(node)

        return FunctionInfo(
            name=node.name,
            params=params,
            source=source,
            conditions=conditions,
            exceptions=exceptions,
            has_return_value=has_return_value,
        )

    def _get_function_source(self, node: ast.FunctionDef) -> str:
        start = node.lineno - 1
        end = node.end_lineno
        raw = "\n".join(self.lines[start:end])
        return textwrap.dedent(raw)

    def _extract_conditions(self, node: ast.FunctionDef) -> list[str]:
        conditions = []
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                conditions.append(ast.unparse(child.test))
        return conditions

    def _extract_exceptions(self, node: ast.FunctionDef) -> list[str]:
        exceptions = []
        for child in ast.walk(node):
            if isinstance(child, ast.Raise) and child.exc is not None:
                exceptions.append(ast.unparse(child.exc))
        return exceptions

    def _extract_imports(self) -> list[str]:
        imports: list[str] = []
        if self.tree is None:
            return imports
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.extend(
                    f"{module}.{alias.name}" if module else alias.name
                    for alias in node.names
                )
        return imports

    def _has_return_value(self, node: ast.FunctionDef) -> bool:
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                return True
        return False

    def _append_function_summary(
        self,
        summary: list[str],
        func: FunctionInfo,
        *,
        prefix: str,
    ) -> None:
        summary.append(f"{prefix}: {func.name}({', '.join(func.params)})")
        if func.conditions:
            summary.append("  Các nhánh IF:")
            for condition in func.conditions:
                summary.append(f"    - if {condition}")
        if func.exceptions:
            summary.append("  Raise exceptions:")
            for exception in func.exceptions:
                summary.append(f"    - raise {exception}")
        if func.has_return_value:
            summary.append("  Có trả về giá trị (return)")
