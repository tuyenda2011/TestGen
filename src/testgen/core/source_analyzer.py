import ast
import re
from typing import Any, Dict

from testgen.analyzer.tree_sitter_adapter import parse_source_structure


def _extract_javascript_public_exports(source_code: str) -> set[str]:
    exports: set[str] = set()
    source = source_code or ""

    for match in re.finditer(r"\bexports\.([A-Za-z_$][\w$]*)\s*=", source):
        exports.add(match.group(1))
    for match in re.finditer(r"\bmodule\.exports\.([A-Za-z_$][\w$]*)\s*=", source):
        exports.add(match.group(1))
    for match in re.finditer(r"\bmodule\.exports\s*=\s*([A-Za-z_$][\w$]*)\b", source):
        exports.add(match.group(1))
    for match in re.finditer(r"\bmodule\.exports\s*=\s*\{(?P<body>.*?)\}", source, re.DOTALL):
        body = match.group("body")
        for key_match in re.finditer(r"(?:^|,)\s*([A-Za-z_$][\w$]*)\s*(?=[:=,}\n])", body):
            exports.add(key_match.group(1))

    return exports


def analyze_source_symbols(source_code: str) -> Dict[str, Any]:
    """
    Ph?n t?ch source code Python (d?ng AST) d? tr?ch xu?t danh s?ch c?c symbol (function, class, method).
    Tr? v? d?nh d?ng:
    {
        "language": "python",
        "symbols": [
            {"name": "factorial", "kind": "function", "signature": "factorial(n)"},
            {"name": "MyClass", "kind": "class", "signature": "class MyClass"},
            {"name": "MyClass.method", "kind": "method", "signature": "method(self)"}
        ],
        "names": ["factorial", "MyClass", "MyClass.method"]
    }
    """
    if not source_code or not source_code.strip():
        return {"language": "python", "symbols": [], "names": []}

    stripped = source_code.strip()
    likely_language = "python"
    if "public class " in stripped or re_search_java_declaration(stripped):
        likely_language = "java"
    elif "function " in stripped or "module.exports" in stripped or "export " in stripped:
        likely_language = "javascript"

    if likely_language in {"java", "javascript"}:
        parsed = parse_source_structure(stripped, likely_language)
        javascript_public_exports = (
            _extract_javascript_public_exports(stripped)
            if likely_language == "javascript"
            else set()
        )
        symbols: list[dict[str, Any]] = []
        names: set[str] = set()
        class_symbols = [symbol for symbol in parsed.symbols if symbol.kind.endswith("_class")]
        for symbol in parsed.symbols:
            if likely_language == "java" and "private " in (symbol.source or "") and not symbol.kind.endswith("_class"):
                continue

            owner = ""
            if not symbol.kind.endswith("_class"):
                for cls in class_symbols:
                    if cls.line_start <= symbol.line_start <= cls.line_end:
                        owner = cls.name
                        break

            display_name = f"{owner}.{symbol.name}" if owner and symbol.name != owner else symbol.name
            if (
                likely_language == "javascript"
                and javascript_public_exports
                and symbol.name not in javascript_public_exports
                and owner not in javascript_public_exports
            ):
                continue
            symbols.append(
                {
                    "name": display_name,
                    "kind": symbol.kind,
                    "signature": display_name,
                    "line_start": symbol.line_start,
                    "line_end": symbol.line_end,
                }
            )
            names.add(symbol.name)
            names.add(display_name)

        return {
            "language": parsed.language,
            "symbols": symbols,
            "names": sorted(name for name in names if name),
            "public_exports": sorted(javascript_public_exports) if likely_language == "javascript" else [],
        }
        
    symbols = []
    names = []
    
    try:
        tree = ast.parse(source_code)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                if not node.name.startswith("_"):
                    args = [arg.arg for arg in node.args.args]
                    sig = f"{node.name}({', '.join(args)})"
                    symbols.append({
                        "name": node.name,
                        "kind": "function",
                        "signature": sig
                    })
                    names.append(node.name)
            elif isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    symbols.append({
                        "name": node.name,
                        "kind": "class",
                        "signature": f"class {node.name}"
                    })
                    names.append(node.name)
                    # Get public methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not item.name.startswith("_") or item.name == "__init__":
                                method_name = f"{node.name}.{item.name}"
                                args = [arg.arg for arg in item.args.args]
                                sig = f"{item.name}({', '.join(args)})"
                                symbols.append({
                                    "name": method_name,
                                    "kind": "method",
                                    "signature": sig
                                })
                                names.append(method_name)
    except Exception:
        pass
        
    return {
        "language": "python",
        "symbols": symbols,
        "names": names
    }


def re_search_java_declaration(source_code: str) -> bool:
    return bool(re.search(r"\b(?:class|interface|enum|record)\s+[A-Za-z_]\w*", source_code))
