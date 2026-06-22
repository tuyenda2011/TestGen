from __future__ import annotations

import ast
from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionInfo:
    name: str
    qualified_name: str
    owner_class: str | None
    source: str
    context_source: str
    import_statement: str
    call_hint: str
    test_name_prefix: str
    constructor_signature: str
    dependency_names: list[str]
    params: list[str]
    conditions: list[str]
    exceptions: list[str]
    returns: list[str]
    decorators: list[str]
    is_async: bool
    method_kind: str
    start_line: int = 0
    end_line: int = 0


def target_slug(value: str) -> str:
    import re

    slug = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()
    return slug or "target"


def source_segment(cleaned: str, lines: list[str], node: ast.AST) -> str:
    source = ast.get_source_segment(cleaned, node)
    if source:
        return source
    if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
        start = max(int(node.lineno) - 1, 0)
        end = int(node.end_lineno)
        return "\n".join(lines[start:end])
    return ""


def safe_unparse(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def module_context(cleaned: str, lines: list[str], max_chars: int = 1800) -> str:
    try:
        tree = ast.parse(cleaned)
    except SyntaxError:
        return ""

    context_parts: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            source = source_segment(cleaned, lines, node)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            source = source_segment(cleaned, lines, node)
        else:
            continue
        if source.strip():
            context_parts.append(source.strip())

    context = "\n".join(context_parts).strip()
    if len(context) <= max_chars:
        return context
    return context[:max_chars].rstrip() + "\n# ... module context truncated ..."


def target_names(target: ast.AST) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        names: list[str] = []
        for item in target.elts:
            names.extend(target_names(item))
        return names
    return []


def module_context_symbols(tree: ast.Module, max_symbols: int = 8) -> list[str]:
    symbols: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                symbols.append(alias.asname or alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                symbols.append(alias.asname or alias.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                symbols.extend(target_names(target))
        elif isinstance(node, ast.AnnAssign):
            symbols.extend(target_names(node.target))

    unique_symbols: list[str] = []
    for symbol in symbols:
        if not symbol.isidentifier() or symbol in unique_symbols:
            continue
        unique_symbols.append(symbol)
        if len(unique_symbols) >= max_symbols:
            break
    return unique_symbols


def source_import_statement(primary_symbol: str, context_symbols: list[str]) -> str:
    names = [primary_symbol]
    names.extend(symbol for symbol in context_symbols if symbol != primary_symbol and not symbol.startswith("__"))
    return f"from source_under_test import {', '.join(names)}"


def function_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = safe_unparse(node.args)
    return f"{node.name}({args})" if args else f"{node.name}()"


def class_constructor_signature(class_node: ast.ClassDef) -> str:
    for child in class_node.body:
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == "__init__":
            return function_signature(child)
    return ""


def function_details(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[list[str], list[str], list[str]]:
    conditions: list[str] = []
    exceptions: list[str] = []
    returns: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.If):
            expression = safe_unparse(child.test)
            if expression:
                conditions.append(expression)
        elif isinstance(child, ast.Raise) and child.exc is not None:
            expression = safe_unparse(child.exc)
            if expression:
                exceptions.append(expression)
        elif isinstance(child, ast.Return):
            expression = safe_unparse(child.value) or "None"
            returns.append(expression)
    return conditions, exceptions, returns


def dependency_names(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    params: list[str],
    max_names: int = 12,
) -> list[str]:
    local_names = set(params)
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, (ast.Store, ast.Del)):
            local_names.add(child.id)

    names: list[str] = []
    for child in ast.walk(node):
        if not isinstance(child, ast.Name) or not isinstance(child.ctx, ast.Load):
            continue
        if child.id in local_names or child.id in {"True", "False", "None"}:
            continue
        if child.id not in names:
            names.append(child.id)
        if len(names) >= max_names:
            break
    return names


def decorators(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    return [item for item in (safe_unparse(decorator) for decorator in node.decorator_list) if item]


def method_kind(decorators_: list[str]) -> str:
    if any(item.endswith("staticmethod") or item == "staticmethod" for item in decorators_):
        return "staticmethod"
    if any(item.endswith("classmethod") or item == "classmethod" for item in decorators_):
        return "classmethod"
    if any(item.endswith("property") or item == "property" for item in decorators_):
        return "property"
    return "instance"


def class_call_hint(class_name: str, method_name: str, method_kind_: str) -> str:
    if method_kind_ == "staticmethod":
        return f"Call {class_name}.{method_name}(...) directly."
    if method_kind_ == "classmethod":
        return f"Call {class_name}.{method_name}(...) directly and assert the returned value/object."
    if method_kind_ == "property":
        return f"Instantiate {class_name} with valid constructor args, then assert instance.{method_name}."
    return f"Instantiate {class_name} with valid constructor args, then call instance.{method_name}(...)."


def build_function_info(
    *,
    cleaned: str,
    lines: list[str],
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    module_context_: str,
    module_symbols: list[str],
    owner_class: str | None = None,
    class_source: str = "",
    constructor_signature: str = "",
) -> FunctionInfo:
    source = source_segment(cleaned, lines, node) or f"def {node.name}(...):\n    pass"
    params = [arg.arg for arg in node.args.args]
    decorators_ = decorators(node)
    dependency_names_ = dependency_names(node, params)
    conditions, exceptions, returns = function_details(node)
    qualified_name = f"{owner_class}.{node.name}" if owner_class else node.name
    if owner_class:
        method_kind_ = method_kind(decorators_)
        import_statement = source_import_statement(owner_class, module_symbols)
        call_hint = class_call_hint(owner_class, node.name, method_kind_)
        context_source = "\n\n".join(part for part in [module_context_, class_source] if part.strip())
    else:
        method_kind_ = "function"
        import_statement = source_import_statement(node.name, module_symbols)
        call_hint = f"Call {node.name}(...) directly."
        context_source = module_context_

    return FunctionInfo(
        name=node.name,
        qualified_name=qualified_name,
        owner_class=owner_class,
        source=source,
        context_source=context_source,
        import_statement=import_statement,
        call_hint=call_hint,
        test_name_prefix=target_slug(qualified_name),
        constructor_signature=constructor_signature,
        dependency_names=dependency_names_,
        params=params,
        conditions=conditions,
        exceptions=exceptions,
        returns=returns,
        decorators=decorators_,
        is_async=isinstance(node, ast.AsyncFunctionDef),
        method_kind=method_kind_,
        start_line=int(getattr(node, "lineno", 0) or 0),
        end_line=int(getattr(node, "end_lineno", 0) or 0),
    )


def batched_function_infos(items: list[FunctionInfo], batch_size: int) -> list[list[FunctionInfo]]:
    size = max(int(batch_size or 1), 1)
    return [items[index : index + size] for index in range(0, len(items), size)]


def extract_python_functions(source_code_text: str, max_functions: int = 16) -> list[FunctionInfo]:
    cleaned = (source_code_text or "").strip()
    if not cleaned:
        return []

    try:
        tree = ast.parse(cleaned)
    except SyntaxError:
        return []

    lines = cleaned.splitlines()
    module_context_ = module_context(cleaned, lines)
    module_symbols = module_context_symbols(tree)
    functions: list[FunctionInfo] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(
                build_function_info(
                    cleaned=cleaned,
                    lines=lines,
                    node=node,
                    module_context_=module_context_,
                    module_symbols=module_symbols,
                )
            )
        elif isinstance(node, ast.ClassDef):
            class_source = source_segment(cleaned, lines, node)
            constructor_signature = class_constructor_signature(node)
            if len(class_source) > 2500:
                class_source = class_source[:2500].rstrip() + "\n# ... class context truncated ..."
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if child.name == "__init__":
                        continue
                    functions.append(
                        build_function_info(
                            cleaned=cleaned,
                            lines=lines,
                            node=child,
                            module_context_=module_context_,
                            module_symbols=module_symbols,
                            owner_class=node.name,
                            class_source=class_source,
                            constructor_signature=constructor_signature,
                        )
                    )
                    if len(functions) >= max_functions:
                        return functions
        if len(functions) >= max_functions:
            return functions
    return functions


def select_functions_for_lines(
    source_code_text: str,
    line_numbers: list[int] | list[str] | tuple[int, ...],
    max_functions: int = 16,
) -> list[FunctionInfo]:
    selected_lines: set[int] = set()
    for value in line_numbers or []:
        try:
            selected_lines.add(int(value))
        except (TypeError, ValueError):
            continue
    if not selected_lines:
        return []

    selected: list[FunctionInfo] = []
    for function_info in extract_python_functions(source_code_text, max_functions=max_functions):
        if not function_info.start_line or not function_info.end_line:
            continue
        if any(function_info.start_line <= line_no <= function_info.end_line for line_no in selected_lines):
            selected.append(function_info)
    return selected


def function_prompt_block(function_info: FunctionInfo) -> str:
    conditions = function_info.conditions or ["(none)"]
    exceptions = function_info.exceptions or ["(none)"]
    condition_text = "\n".join(f"- {item}" for item in conditions)
    exception_text = "\n".join(f"- {item}" for item in exceptions)
    returns = function_info.returns or ["(no explicit return)"]
    return_text = "\n".join(f"- {item}" for item in returns)
    decorators_ = function_info.decorators or ["(none)"]
    decorator_text = "\n".join(f"- {item}" for item in decorators_)
    dependency_names_ = function_info.dependency_names or ["(none)"]
    dependency_text = "\n".join(f"- {item}" for item in dependency_names_)
    constructor_text = function_info.constructor_signature or "(none or not required)"
    params_text = ", ".join(function_info.params) if function_info.params else "(no parameters)"
    context_text = function_info.context_source.strip() or "(none)"
    required_test_prefix = f"test_{function_info.test_name_prefix}_"

    return (
        f"Target: {function_info.qualified_name}({params_text})\n"
        f"Target type: {function_info.method_kind}\n"
        f"Async: {function_info.is_async}\n"
        f"Required import: {function_info.import_statement}\n"
        f"Suggested call hint: {function_info.call_hint}\n\n"
        f"Constructor signature (if class): {constructor_text}\n"
        f"Required test function prefix: {required_test_prefix}\n\n"
        "Decorators:\n"
        f"{decorator_text}\n\n"
        "Dependencies the target reads/calls:\n"
        f"{dependency_text}\n\n"
        "Conditions to cover:\n"
        f"{condition_text}\n\n"
        "Exceptions detected:\n"
        f"{exception_text}\n\n"
        "Returns detected:\n"
        f"{return_text}\n\n"
        "Module/class context to preserve:\n"
        "```python\n"
        f"{context_text}\n"
        "```\n\n"
        "Target source code:\n"
        "```python\n"
        f"{function_info.source}\n"
        "```"
    )


def build_function_level_prompt(
    *,
    requirement_json: str,
    test_plan_json: str,
    function_info: FunctionInfo,
    test_technique: str,
) -> str:
    required_test_prefix = f"test_{function_info.test_name_prefix}_"
    return (
        "Objective: Generate runnable pytest code for ONE Python target below.\n"
        f"Test technique: {test_technique}\n\n"
        "Requirement JSON:\n"
        f"{requirement_json.strip() or 'Needs clarification'}\n\n"
        "Test Plan JSON:\n"
        f"{test_plan_json.strip() or 'Needs clarification'}\n\n"
        f"{function_prompt_block(function_info)}\n\n"
        "Output requirements:\n"
        "- Only return runnable pytest code.\n"
        f"- Must include import statement: {function_info.import_statement}\n"
        f"- Every test function must start with prefix: {required_test_prefix}\n"
        "- The behavior in the source code is the ultimate truth; if it contradicts the JSON plan, follow the source.\n"
        "- For exceptions, use pytest.raises and match type/message exactly if message exists in source.\n"
        "- For async targets, use pytest.mark.asyncio.\n"
        "- Do not use TODO/placeholders in generated pytest code.\n"
        "- Do not rely on fixtures, helpers, or conftest not present in the provided source/context.\n"
        "- Use explicit asserts.\n"
        "- Cover valid/invalid cases for conditions and exception cases if present.\n"
        "- Do not use markdown."
    )


def build_function_batch_prompt(
    *,
    requirement_json: str,
    test_plan_json: str,
    function_infos: list[FunctionInfo],
    test_technique: str,
) -> str:
    target_rules = "\n".join(
        (
            f"- {item.qualified_name}: use header `# ===== Tests for {item.qualified_name} =====`, "
            f"import `{item.import_statement}`, prefix `test_{item.test_name_prefix}_`."
        )
        for item in function_infos
    )
    target_blocks = "\n\n---\n\n".join(function_prompt_block(item) for item in function_infos)
    return (
        "Objective: Generate runnable pytest code for a BATCH of Python targets below.\n"
        f"Test technique: {test_technique}\n\n"
        "Requirement JSON:\n"
        f"{requirement_json.strip() or 'Needs clarification'}\n\n"
        "Test Plan JSON:\n"
        f"{test_plan_json.strip() or 'Needs clarification'}\n\n"
        "Mandatory rules per target:\n"
        f"{target_rules}\n\n"
        "Targets to test:\n"
        f"{target_blocks}\n\n"
        "Output requirements:\n"
        "- Only return runnable pytest code.\n"
        "- Separate code exactly by the mandatory target headers.\n"
        "- Each target must have its required import and all its test functions must use its specific prefix.\n"
        "- The behavior in the source code is the ultimate truth; if it contradicts the JSON plan, follow the source.\n"
        "- For exceptions, use pytest.raises and match type/message exactly if message exists in source.\n"
        "- For async targets, use pytest.mark.asyncio.\n"
        "- Do not use TODO/placeholders, print-only tests or always-true asserts.\n"
        "- Do not rely on fixtures, helpers, or conftest not present in the provided source/context.\n"
        "- Do not use markdown."
    )


class FunctionPromptBuilder:
    """Build deterministic prompts from Python AST metadata."""

    extract_python_functions = staticmethod(extract_python_functions)
    select_functions_for_lines = staticmethod(select_functions_for_lines)
    batched = staticmethod(batched_function_infos)
    function_prompt_block = staticmethod(function_prompt_block)
    build_function_level_prompt = staticmethod(build_function_level_prompt)
    build_function_batch_prompt = staticmethod(build_function_batch_prompt)
