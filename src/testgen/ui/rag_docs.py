# pyrefly: ignore [missing-import]
import streamlit as st
from testgen.core.config import DOC_UPLOAD_PATH, DOC_COLLECTION_NAME, SOURCE_COLLECTION_NAME
from testgen.rag.document_loader import (
    delete_saved_doc_file,
    list_saved_doc_files,
    load_saved_doc_entries,
    load_uploaded_file_entries,
    persist_uploaded_doc_files,
)
from testgen.rag.vector_store import clear_vector_store
from testgen.ui.rag_state import sync_docs_rag_state, invalidate_docs_rag_index, index_rag_sections, _rag_signature_key
from testgen.core.utils import normalize_text

def render_rag_docs_panel(
    enable_preindexed_toggle: bool,
    selected_mode: str,
    gemini_api_key: str,
    profile: dict,
) -> tuple[list | None, bool]:
    indexed_chunk_count = sync_docs_rag_state()
    step_title = "Bước 3 - Chuẩn bị kho tìm nhanh tài liệu" if enable_preindexed_toggle else "Quản lý tài liệu"
    st.markdown(
        f"""
        <div class="flow-title" style="margin-bottom: 1rem;">{step_title}</div>
        """,
        unsafe_allow_html=True,
    )
    notice_area = st.empty()
    pending_notice = st.session_state.pop("docs_rag_notice", "")
    current_notice = ""
    suppress_pending_notice = False
    docs_uploader_version = int(st.session_state.get("docs_uploader_version", 0))
    docs_uploader_key = f"docs_uploaded_files_{docs_uploader_version}"

    docs_files = st.file_uploader(
        "Tải tài liệu PDF/TXT/Markdown",
        type=["pdf", "txt", "md", "markdown"],
        accept_multiple_files=True,
        key=docs_uploader_key,
    )
    uploaded_docs_count = len(docs_files or [])
    if docs_files:
        st.caption(f"Đã chọn {uploaded_docs_count} tệp tài liệu.")
        upload_signature = tuple(
            sorted(
                f"{getattr(item, 'name', '')}:{getattr(item, 'size', 0)}"
                for item in docs_files
            )
        )
        if upload_signature != st.session_state.get("last_docs_upload_signature"):
            suppress_pending_notice = True
            st.session_state["last_docs_upload_signature"] = upload_signature
            persisted_docs = persist_uploaded_doc_files(docs_files, DOC_UPLOAD_PATH)
            if persisted_docs:
                st.caption(f"Đã lưu/ghi đè {len(persisted_docs)} tệp tài liệu vào: {DOC_UPLOAD_PATH}")
                invalidate_docs_rag_index()
                current_notice = (
                    f"Đã lưu/ghi đè {len(persisted_docs)} tệp tài liệu và gỡ kho tìm nhanh cũ. "
                    "Bấm 'Tạo kho tìm nhanh' để cập nhật lại."
                )

    action_area = st.container()
    with action_area:
        index_cols = st.columns(4) if enable_preindexed_toggle else st.columns(3)
        with index_cols[0]:
            process_docs_clicked = st.button("Tạo kho tìm nhanh", use_container_width=True, key="process_docs_rag")
        with index_cols[1]:
            stop_process_clicked = st.button("Dừng tạo", use_container_width=True, key="stop_process_docs_rag")
        with index_cols[2]:
            clear_index_clicked = st.button(
                "Xóa kho tìm nhanh",
                use_container_width=True,
                key="clear_docs_rag_index",
            )

    use_preindexed_local = False
    if enable_preindexed_toggle:
        with index_cols[3]:
            use_preindexed_local = st.checkbox(
                "Dùng kho tìm nhanh sẵn có",
                value=bool(st.session_state.get("docs_rag_ready", False)),
                key="use_preindexed_docs",
            )

    details_area = st.empty()
    saved_doc_files = list_saved_doc_files(DOC_UPLOAD_PATH)

    if stop_process_clicked:
        st.session_state["stop_indexing"] = True
        st.session_state["docs_rag_notice"] = "Đã yêu cầu dừng tạo kho tìm nhanh."
        st.rerun()

    if clear_index_clicked:
        suppress_pending_notice = True
        cleared, disk_purged = clear_vector_store(
            [DOC_COLLECTION_NAME, SOURCE_COLLECTION_NAME],
            purge_disk=True,
        )
        st.session_state.pop(_rag_signature_key(DOC_COLLECTION_NAME), None)
        st.session_state.pop(_rag_signature_key(SOURCE_COLLECTION_NAME), None)
        docs_cleared = bool(cleared.get(DOC_COLLECTION_NAME, False))
        source_cleared = bool(cleared.get(SOURCE_COLLECTION_NAME, False))
        if docs_cleared:
            st.session_state["docs_rag_ready"] = False
            st.session_state["docs_rag_stale"] = bool(saved_doc_files)
            st.session_state["docs_rag_stale_reason"] = "manual_clear"
            st.session_state["docs_rag_chunk_count"] = 0
            indexed_chunk_count = 0

            if source_cleared and disk_purged:
                current_notice = (
                    "Đã xóa kho tìm nhanh (docs + source) và dọn dữ liệu lưu trữ. "
                    "File đang chọn trên uploader đã được bỏ khỏi giao diện."
                )
            elif source_cleared:
                current_notice = (
                    "Đã xóa collection docs + source, nhưng chưa dọn sạch file trên disk "
                    "(thường do file đang bị tiến trình khác giữ)."
                )
            else:
                current_notice = (
                    "Đã xóa kho tài liệu, nhưng chưa xóa được kho source code. "
                    "Hãy thử lại nếu cần dọn sạch toàn bộ."
                )
            st.session_state["docs_rag_notice"] = current_notice
            st.session_state["docs_uploader_version"] = docs_uploader_version + 1
            st.session_state.pop("last_docs_upload_signature", None)
            st.rerun()
        else:
            st.warning("Chưa xóa được kho tìm nhanh tài liệu. Hãy thử lại.")

    if process_docs_clicked:
        suppress_pending_notice = True
        if selected_mode == "API key" and not normalize_text(gemini_api_key):
            st.warning("Nhập Gemini API key trước khi tạo kho tìm nhanh.")
        else:
            docs_for_indexing = (
                load_uploaded_file_entries(list(docs_files or []))
                if docs_files
                else load_saved_doc_entries(DOC_UPLOAD_PATH)
            )
            if not docs_for_indexing:
                st.warning("Không có tài liệu để xử lý. Hãy tải PDF/TXT/Markdown lên hoặc thêm tài liệu vào thư viện đã lưu.")
            else:
                with details_area.container():
                    with st.spinner("Đang tạo kho tìm nhanh tài liệu..."):
                        docs_chunk_count, docs_reused = index_rag_sections(
                            DOC_COLLECTION_NAME,
                            docs_for_indexing,
                            "Tài liệu",
                            profile.get("embedding_backend", profile["backend"]),
                            normalize_text(gemini_api_key),
                        )
                st.session_state["docs_rag_ready"] = docs_chunk_count > 0
                st.session_state["docs_rag_chunk_count"] = docs_chunk_count
                st.session_state["docs_rag_stale"] = False
                st.session_state.pop("docs_rag_stale_reason", None)
                indexed_chunk_count = docs_chunk_count
                if docs_reused:
                    current_notice = f"Kho tìm nhanh đã đồng bộ sẵn, tái sử dụng {docs_chunk_count} chunk tài liệu."
                else:
                    current_notice = f"Đã tạo kho tìm nhanh với {docs_chunk_count} chunk tài liệu."

    if current_notice:
        notice_area.success(current_notice)
    elif pending_notice and not suppress_pending_notice:
        notice_area.success(pending_notice)

    saved_doc_files = list_saved_doc_files(DOC_UPLOAD_PATH)
    if not saved_doc_files and st.session_state.get("docs_rag_stale"):
        st.session_state["docs_rag_stale"] = False
        st.session_state.pop("docs_rag_stale_reason", None)
    index_ready = bool(st.session_state.get("docs_rag_ready", False)) and not st.session_state.get("docs_rag_stale", False)
    index_status = "Đồng bộ" if index_ready else "Cần xử lý"
    if not saved_doc_files and indexed_chunk_count == 0:
        index_status = "Trống"
    with details_area.container():
        docs_cols = st.columns(4)
        docs_cols[0].metric("Tài liệu tải lên lần này", f"{uploaded_docs_count:,}")
        docs_cols[1].metric("Thư viện tài liệu", f"{len(saved_doc_files):,} file")
        docs_cols[2].metric("Kho tìm nhanh", f"{indexed_chunk_count:,} chunk")
        docs_cols[3].metric("Trạng thái", index_status)
        if st.session_state.get("docs_rag_stale"):
            stale_reason = st.session_state.get("docs_rag_stale_reason", "")
            if stale_reason != "manual_clear":
                st.warning("Thư viện tài liệu đã thay đổi. Kho tìm nhanh cũ đã được xóa để tránh truy xuất nhầm dữ liệu.")
        if saved_doc_files:
            st.markdown('<div class="action-title" style="margin-top: 1.5rem; margin-bottom: 0.5rem;">📁 Danh sách tài liệu đã lưu</div>', unsafe_allow_html=True)
            list_container = st.container(border=True)
            with list_container:
                if len(saved_doc_files) > 1:
                    header_cols = st.columns([0.8, 0.2])
                    header_cols[0].caption("Tất cả tài liệu trong thư viện")
                    with header_cols[1]:
                        if st.button("Xóa tất cả", key="delete_all_saved_docs", use_container_width=True, type="primary"):
                            for path in saved_doc_files:
                                delete_saved_doc_file(DOC_UPLOAD_PATH, path.name)
                            invalidate_docs_rag_index()
                            st.session_state["docs_rag_notice"] = "Đã xóa toàn bộ tài liệu đã lưu và gỡ kho tìm nhanh cũ."
                            st.rerun()
                    st.divider()
                
                for index, path in enumerate(saved_doc_files):
                    file_cols = st.columns([0.65, 0.2, 0.15], vertical_alignment="center")
                    file_cols[0].markdown(f"**📄 {path.name}**")
                    file_cols[1].caption(f"{path.stat().st_size / 1024:.1f} KB")
                    with file_cols[2]:
                        if st.button("Xóa", key=f"delete_doc_{index}_{path.name}", use_container_width=True):
                            if delete_saved_doc_file(DOC_UPLOAD_PATH, path.name):
                                invalidate_docs_rag_index()
                                st.session_state["docs_rag_notice"] = (
                                    f"Đã xóa {path.name} và gỡ kho tìm nhanh cũ. "
                                    "Hãy tạo lại kho tìm nhanh nếu cần dùng các tài liệu còn lại."
                                )
                                st.rerun()
                            else:
                                st.warning(f"Không xóa được {path.name}.")

        if st.session_state.get("docs_rag_ready"):
            st.caption(
                f"Kho tìm nhanh đã sẵn sàng: {st.session_state.get('docs_rag_chunk_count', 0)} chunk. "
                "Bạn có thể tái sử dụng ngay cho lần chạy tiếp theo."
            )
            if enable_preindexed_toggle:
                st.caption("Nếu chỉ cần sinh test nhanh, bật 'Dùng kho tìm nhanh sẵn có'.")
        elif enable_preindexed_toggle:
            st.caption("Bạn có thể chuẩn bị kho tìm nhanh trước để lần chạy sinh mã nhanh hơn.")
        elif st.session_state.get("docs_rag_stale"):
            stale_reason = st.session_state.get("docs_rag_stale_reason", "")
            if stale_reason != "manual_clear":
                st.caption("Tài liệu đã thay đổi. Hãy bấm 'Tạo kho tìm nhanh' để cập nhật trước khi dùng.")

    return docs_files, use_preindexed_local
