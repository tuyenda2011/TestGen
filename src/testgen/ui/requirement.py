import streamlit as st
from testgen.core.utils import normalize_text
from testgen.core.constants import CODE_FILE_TYPES
from testgen.core.config import DOC_UPLOAD_PATH
from testgen.rag.document_loader import persist_uploaded_doc_files

def render_requirement_panel() -> tuple[str, str, str, list | None]:
    requirement_value = ""
    retrieval_value = ""
    
    source_value = ""
    source_files = None
    with st.expander("Nhập source code", expanded=True):
        source_value = st.text_area(
            "Source code nguồn",
            placeholder="Dán source code cần phân tích ở đây.",
            height=240,
            key="source_code_text",
        )
        source_files = st.file_uploader(
            "Tải source code text-based",
            type=CODE_FILE_TYPES,
            accept_multiple_files=True,
            key="source_uploaded_files",
        )
        total_chars = len(normalize_text(source_value))
        if source_files:
            st.caption(f"Đã chọn {len(source_files)} tệp source code.")
            for f in source_files:
                try:
                    content = f.getvalue().decode("utf-8")
                    total_chars += len(normalize_text(content))
                except Exception:
                    pass
            
            # Lưu các tệp mã nguồn vào uploaded_docs (để dùng chung cho RAG/Lưu trữ)
            upload_sig = tuple(sorted(f"{getattr(item, 'name', '')}:{getattr(item, 'size', 0)}" for item in source_files))
            if upload_sig != st.session_state.get("last_source_upload_signature"):
                st.session_state["last_source_upload_signature"] = upload_sig
                persisted = persist_uploaded_doc_files(source_files, DOC_UPLOAD_PATH)
                if persisted:
                    st.caption(f"Đã lưu/ghi đè {len(persisted)} tệp source code vào thư viện chung.")

        source_cols = st.columns(2)
        source_cols[0].metric("Ký tự source", f"{total_chars:,}")
        source_cols[1].metric("Số tệp source", f"{len(source_files or []):,}")

    st.caption("Hệ thống sẽ tự suy luận ngữ cảnh kiểm thử từ yêu cầu và source code đầu vào.")
    return requirement_value, retrieval_value, source_value, source_files
