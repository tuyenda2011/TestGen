import streamlit as st
from testgen.core.utils import normalize_text
from testgen.core.constants import CODE_FILE_TYPES
from testgen.core.config import DOC_UPLOAD_PATH
from testgen.rag.document_loader import persist_uploaded_doc_files

def render_review_panel() -> tuple[str, list | None]:
    test_value = st.text_area(
        "Test code cần review",
        placeholder="Dán test code cần rà soát ở đây.",
        height=240,
        key="test_code_text",
    )
    test_files = st.file_uploader(
        "Tải test code text-based",
        type=CODE_FILE_TYPES,
        accept_multiple_files=True,
        key="test_uploaded_files",
    )
    if test_files:
        st.caption(f"Đã chọn {len(test_files)} tệp test code.")
        
        # Lưu các tệp mã kiểm thử vào uploaded_docs
        upload_sig = tuple(sorted(f"{getattr(item, 'name', '')}:{getattr(item, 'size', 0)}" for item in test_files))
        if upload_sig != st.session_state.get("last_test_upload_signature"):
            st.session_state["last_test_upload_signature"] = upload_sig
            persisted = persist_uploaded_doc_files(test_files, DOC_UPLOAD_PATH)
            if persisted:
                st.caption(f"Đã lưu/ghi đè {len(persisted)} tệp test code vào thư viện chung.")

    code_cols = st.columns(2)
    code_cols[0].metric("Ký tự test code", f"{len(normalize_text(test_value)):,}")
    code_cols[1].metric("Số tệp test", f"{len(test_files or []):,}")
    return test_value, test_files
