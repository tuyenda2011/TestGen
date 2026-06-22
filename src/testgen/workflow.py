from __future__ import annotations

from testgen.core.utils import normalize_text


def resolve_retrieval_source(
    *,
    retrieval_query: str,
    manual_requirement: str,
    has_docs: bool,
    has_source: bool,
    has_test_code: bool,
) -> str:
    source = normalize_text(retrieval_query) or normalize_text(manual_requirement)
    if source:
        return source
    if has_docs and has_source:
        return "Hãy phân tích tài liệu và source code đã tải lên để suy ra yêu cầu kiểm thử."
    if has_source:
        return "Hãy phân tích source code đã tải lên để suy ra yêu cầu kiểm thử."
    if has_docs:
        return "Hãy phân tích tài liệu đã tải lên để suy ra yêu cầu kiểm thử."
    if has_test_code:
        return "Hãy rà soát test code người dùng cung cấp theo thực hành kiểm thử tốt."
    return ""
