import shutil
from pathlib import Path

# pyrefly: ignore [missing-import]
import streamlit as st

from testgen.core.config import CHROMA_PATH, OUTPUT_RUNS_PATH
from testgen.run_history import cleanup_run_history


def _get_size_str(path: Path) -> str:
    if not path.exists():
        return "0 MB"
    total_size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return f"{total_size / (1024 * 1024):.2f} MB"


def render_privacy_panel() -> None:
    st.markdown(
        """
        <div class="flow-card">
            <div class="flow-title">Quản lý dữ liệu & dung lượng</div>
            <div class="flow-desc">Xem dung lượng và dọn lịch sử chạy hoặc vector database.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Dung lượng hiện tại")
    col1, col2 = st.columns(2)
    col1.metric("Lịch sử chạy (outputs/runs)", _get_size_str(OUTPUT_RUNS_PATH))
    col2.metric("Vector Database (ChromaDB)", _get_size_str(CHROMA_PATH))

    st.divider()
    st.subheader("Dọn dẹp")
    st.warning("Các thao tác dưới đây không thể hoàn tác. Hãy chắc chắn trước khi thực hiện.")

    keep_runs = st.number_input("Giữ lại số run mới nhất", min_value=1, max_value=500, value=100, step=10)
    if st.button("Dọn lịch sử cũ", use_container_width=True):
        deleted = cleanup_run_history(max_runs=int(keep_runs), max_age_days=None)
        if deleted:
            st.success(f"Đã dọn {len(deleted)} run cũ.")
            st.rerun()
        else:
            st.info("Chưa có run cũ cần dọn.")

    if st.button("Xóa toàn bộ lịch sử chạy", use_container_width=True):
        if OUTPUT_RUNS_PATH.exists():
            shutil.rmtree(OUTPUT_RUNS_PATH, ignore_errors=True)
            OUTPUT_RUNS_PATH.mkdir(parents=True, exist_ok=True)
            st.success("Đã xóa toàn bộ lịch sử chạy.")
            st.rerun()
        else:
            st.info("Thư mục lịch sử chạy trống.")

    if st.button("Xóa toàn bộ Vector DB (Chroma)", use_container_width=True):
        if CHROMA_PATH.exists():
            from testgen.rag.vector_store import clear_vector_store

            clear_vector_store([], purge_disk=True)
            st.success("Đã xóa toàn bộ dữ liệu ChromaDB.")
            st.rerun()
        else:
            st.info("Thư mục Vector DB trống.")
