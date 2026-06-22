from __future__ import annotations

# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

from testgen.core.config import BASE_DIR
from testgen.ui.styles import apply_custom_styles
from testgen.core.constants import (
    GENERATE_WORKFLOW,
    HISTORY_WORKFLOW,
    PRIVACY_WORKFLOW,
    RAG_WORKFLOW,
    REVIEW_WORKFLOW,
)
from testgen.ui.sidebar import render_sidebar
from testgen.ui.requirement import render_requirement_panel
from testgen.ui.rag_docs import render_rag_docs_panel
from testgen.ui.review import render_review_panel
from testgen.ui.history import render_history_panel
from testgen.ui.privacy import render_privacy_panel
from testgen.ui.results import render_results
from testgen.pipeline_orchestrator import run_pipeline as _run_pipeline_external
from testgen.core.models import PipelineInput, PipelineProfile, PipelineCancelledError
from testgen.ui.rag_state import _rag_signature_key
from testgen.core.config import DOC_COLLECTION_NAME, SOURCE_COLLECTION_NAME
from testgen.core.utils import normalize_text
from testgen.core.llm import use_stream_writer

ROOT = BASE_DIR
load_dotenv(ROOT / ".env")

def render_app():
    st.set_page_config(page_title="Trình tạo mã kiểm thử tự động đa tác tử", layout="wide")
    apply_custom_styles()
    print("STREAMLIT_APP configured page", flush=True)

    st.markdown(
        """
        <div class="app-hero">
            <div class="app-hero-title">
                TestGen
            </div>
            Hệ thống kiểm thử tự động multi-agent
            <div class="app-hero-subtitle">
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_mode, workflow_mode, framework, test_technique, gemini_api_key, profile, use_preindexed_docs = render_sidebar()
    print(f"STREAMLIT_APP sidebar workflow={workflow_mode}", flush=True)

    requirement_text = ""
    source_code_text = ""
    source_uploaded_files = None
    test_code_text = ""
    test_uploaded_files = None
    docs_uploaded_files = None
    retrieval_query = ""
    use_preindexed_docs_local = False
    generate_clicked = False
    clear_clicked = False

    if workflow_mode == RAG_WORKFLOW:
        docs_uploaded_files, use_preindexed_docs_local = render_rag_docs_panel(enable_preindexed_toggle=False, selected_mode=selected_mode, gemini_api_key=gemini_api_key, profile=profile)
    elif workflow_mode == GENERATE_WORKFLOW:
        requirement_text, retrieval_query, source_code_text, source_uploaded_files = render_requirement_panel()
        docs_uploaded_files = None
        use_preindexed_docs_local = use_preindexed_docs
        button_col, stop_col, clear_col = st.columns([0.5, 0.25, 0.25])
        with button_col:
            generate_clicked = st.button(
                "Sinh mã kiểm thử",
                type="primary",
                use_container_width=True,
                disabled=selected_mode == "API key" and not normalize_text(gemini_api_key),
                key="generate_button_requirement_main",
            )
        with stop_col:
            if st.button("Dừng tiến trình", use_container_width=True, key="stop_button_requirement_main"):
                st.session_state.cancel_requested = True
        with clear_col:
            clear_clicked = st.button("Xóa kết quả", use_container_width=True, key="clear_button_requirement_main")
    elif workflow_mode == REVIEW_WORKFLOW:
        test_code_text, test_uploaded_files = render_review_panel()
        button_col, stop_col, clear_col = st.columns([0.5, 0.25, 0.25])
        with button_col:
            generate_clicked = st.button(
                "Rà soát test code",
                type="primary",
                use_container_width=True,
                disabled=selected_mode == "API key" and not normalize_text(gemini_api_key),
                key="generate_button_review_main",
            )
        with stop_col:
            if st.button("Dừng tiến trình", use_container_width=True, key="stop_button_review_main"):
                st.session_state.cancel_requested = True
        with clear_col:
            clear_clicked = st.button("Xóa kết quả", use_container_width=True, key="clear_button_review_main")
    elif workflow_mode == HISTORY_WORKFLOW:
        render_history_panel()
    else:
        render_privacy_panel()

    if clear_clicked:
        st.session_state.pop("last_result", None)
        st.rerun()

    def _progress_frame(progress: list[dict[str, str]]) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "Bước": item.get("step", ""),
                    "Agent": item.get("agent", ""),
                    "Model": item.get("model", ""),
                    "Trạng thái": item.get("status", ""),
                    "Kết quả": item.get("result", ""),
                }
                for item in progress
            ]
        )

    if generate_clicked:
        st.session_state.cancel_requested = False
        try:
            progress_rows: list[dict[str, str]] = []
            progress_bar = st.progress(0, text="Đang chuẩn bị pipeline...")
            progress_table = st.empty()

            def update_progress(item: dict[str, str]) -> None:
                progress_rows.append(item)
                progress_bar.progress(
                    min(len(progress_rows) / 9, 1.0),
                    text=f"🔄 {item.get('agent', '')}: {item.get('status', '')}",
                )
                progress_table.dataframe(_progress_frame(progress_rows), use_container_width=True, hide_index=True)

            with st.spinner("Đang chạy chuỗi tác tử..."):
                pipeline_input = PipelineInput(
                    requirement_text=requirement_text,
                    docs_files=list(docs_uploaded_files or []),
                    source_code_text=source_code_text,
                    source_files=list(source_uploaded_files or []),
                    test_code_text=test_code_text,
                    test_files=list(test_uploaded_files or []),
                    retrieval_query=retrieval_query,
                    framework=framework,
                    test_technique=test_technique,
                    workflow_mode=workflow_mode,
                    api_key=normalize_text(gemini_api_key),
                    use_preindexed_docs=use_preindexed_docs_local,
                    previous_docs_signature=str(st.session_state.get(_rag_signature_key(DOC_COLLECTION_NAME), "")),
                    previous_source_signature=str(st.session_state.get(_rag_signature_key(SOURCE_COLLECTION_NAME), "")),
                )
                pipeline_profile = PipelineProfile(**profile)

                stream_placeholder = st.empty()

                def write_llm_stream(chunks):
                    with stream_placeholder.container():
                        st.caption("Đang nhận phản hồi LLM...")
                        return st.write_stream(chunks)

                stream_writer = write_llm_stream if pipeline_profile.backend == "openrouter" else None
                
                def check_cancellation():
                    return st.session_state.get("cancel_requested", False)
                
                with use_stream_writer(stream_writer):
                    result_obj = _run_pipeline_external(
                        input_data=pipeline_input,
                        profile=pipeline_profile,
                        progress_callback=update_progress,
                        cancel_check=check_cancellation,
                    )
                stream_placeholder.empty()
                st.session_state[_rag_signature_key(DOC_COLLECTION_NAME)] = result_obj.new_docs_signature
                st.session_state[_rag_signature_key(SOURCE_COLLECTION_NAME)] = result_obj.new_source_signature
                st.session_state["last_result"] = result_obj.model_dump()
                
            progress_bar.progress(1.0, text="✅ Hoàn tất pipeline.")
            st.success("✅ Đã tạo xong! Xem kết quả bên dưới.")
        except PipelineCancelledError as exc:
            st.warning(f"⏹️ {exc}")
        except ValueError as exc:
            st.warning(f"⚠️ {exc}")
        except RuntimeError as exc:
            st.error(f"🔴 {exc}")
        except Exception as exc:
            st.error(f"❌ Lỗi không mong đợi: {exc}")

    result = st.session_state.get("last_result")
    if result and workflow_mode in {GENERATE_WORKFLOW, REVIEW_WORKFLOW}:
        render_results(result, workflow_mode, framework, test_technique)

    print("STREAMLIT_APP render complete", flush=True)

render_app()
