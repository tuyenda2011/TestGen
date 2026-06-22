from typing import Any
import pandas as pd
import streamlit as st

from testgen.core.config import OUTPUT_RUNS_PATH
from testgen.run_history import (
    delete_run_history,
    load_history_entries,
    load_run_manifest,
    rebuild_history_index,
)
from pathlib import Path

def _file_mime_from_extension(path: Path) -> str:
    if path.suffix == ".xlsx":
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if path.suffix == ".pdf":
        return "application/pdf"
    if path.suffix == ".md":
        return "text/markdown"
    return "text/plain"

def _download_button(label: str, path: str, key: str) -> None:
    if not path:
        st.caption(f"Thiếu đường dẫn cho {label}.")
        return
    file_path = Path(path)
    if not file_path.exists() or file_path.is_dir():
        st.caption(f"Thiếu tệp: {file_path}")
        return

    if file_path.suffix in {".xlsx", ".pdf"}:
        data = file_path.read_bytes()
    else:
        data = file_path.read_text(encoding="utf-8")

    st.download_button(
        label,
        data=data,
        file_name=file_path.name,
        mime=_file_mime_from_extension(file_path),
        key=key,
        use_container_width=True,
    )

def _history_frame(entries: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Thời gian": str(item.get("created_at", "")).replace("T", " "),
                "Run ID": item.get("run_id", ""),
                "Luồng": item.get("workflow", ""),
                "Framework": item.get("framework", ""),
                "Kỹ thuật": item.get("test_technique", ""),
                "Tệp": item.get("artifact_count", 0),
            }
            for item in entries
        ]
    )

def render_history_panel() -> None:
    st.markdown(
        """
        <div class="flow-card">
            <div class="flow-title">Lịch sử chạy</div>
            <div class="flow-desc">Xem lại các lần chạy đã xuất file trong outputs/runs.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history_notice = st.session_state.pop("history_notice", "")
    if history_notice:
        st.success(history_notice)

    actions = st.columns([0.18, 0.18, 0.64])
    with actions[0]:
        refresh_clicked = st.button("Làm mới", key="history_refresh", use_container_width=True)
    with actions[1]:
        rebuild_clicked = st.button("Quét lại", key="history_rebuild", use_container_width=True)

    if rebuild_clicked:
        entries = rebuild_history_index()
        st.session_state["history_notice"] = f"Đã quét lại lịch sử: {len(entries)} lần chạy."
        st.rerun()
    else:
        entries = load_history_entries(limit=500)
        if refresh_clicked:
            st.rerun()

    if not entries:
        st.info("Chưa có lịch sử chạy nào trong outputs/runs.")
        st.caption(f"Thư mục lịch sử: {OUTPUT_RUNS_PATH}")
        return

    st.dataframe(_history_frame(entries), use_container_width=True, hide_index=True)

    labels: list[str] = []
    lookup: dict[str, dict[str, Any]] = {}
    for item in entries:
        run_id = str(item.get("run_id", ""))
        created_at = str(item.get("created_at", "")).replace("T", " ")
        workflow = str(item.get("workflow", ""))
        label = f"{created_at} | {workflow} | {run_id}"
        labels.append(label)
        lookup[label] = item

    selected_label = st.selectbox("Chọn lần chạy", labels, key="history_selected_run")
    selected = lookup[selected_label]
    run_id = str(selected.get("run_id", ""))
    manifest = load_run_manifest(run_id)

    summary_cols = st.columns(4)
    summary_cols[0].metric("Run ID", run_id)
    summary_cols[1].metric("Luồng", str(selected.get("workflow", "")))
    summary_cols[2].metric("Framework", str(selected.get("framework", "")))
    summary_cols[3].metric("Số tệp", str(selected.get("artifact_count", 0)))

    if not manifest:
        st.warning("Không đọc được manifest của lần chạy này.")
        return

    artifacts_raw = manifest.get("artifacts")
    artifacts = artifacts_raw if isinstance(artifacts_raw, list) else []
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            continue
        label = str(artifact.get("label", "")).strip() or f"Tải tệp #{index + 1}"
        path = str(artifact.get("path", "")).strip()
        _download_button(label, path, key=f"history_download_{run_id}_{index}")

    if st.button("Xóa lần chạy này", key=f"history_delete_{run_id}", use_container_width=True):
        if delete_run_history(run_id):
            st.session_state["history_notice"] = f"Đã xóa lịch sử run {run_id}."
            st.rerun()
        else:
            st.warning(f"Không xóa được run {run_id}.")
