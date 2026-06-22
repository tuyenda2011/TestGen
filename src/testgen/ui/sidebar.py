import streamlit as st
from html import escape
from testgen.core.setup_commands import ollama_pull_commands
from testgen.core.utils import normalize_text
from testgen.core.constants import (
    MODE_OPTIONS,
    WORKFLOW_LABEL_OPTIONS,
    WORKFLOW_WIDGET_KEY,
    LEGACY_WORKFLOW_LOOKUP,
    RAG_WORKFLOW,
    GENERATE_WORKFLOW,
    REVIEW_WORKFLOW,
    HISTORY_WORKFLOW,
    FRAMEWORK_OPTIONS,
    FRAMEWORK_LOOKUP,
    OLLAMA_MODEL_OPTIONS,
    OPENROUTER_MODEL_OPTIONS,
    TEST_TECHNIQUE_OPTIONS,
    profile_for_mode,
    workflow_label,
)

def _normalize_workflow_value(value: str | None) -> str:
    cleaned = normalize_text(value)
    if cleaned in list(LEGACY_WORKFLOW_LOOKUP.values()):
        return cleaned
    return LEGACY_WORKFLOW_LOOKUP.get(cleaned, RAG_WORKFLOW)

def _initial_workflow_value() -> str:
    return _normalize_workflow_value(
        st.session_state.get(WORKFLOW_WIDGET_KEY)
        or st.session_state.get("workflow_choice_v2")
        or st.session_state.get("workflow_mode")
    )

def _status_box(label: str, value: str) -> str:
    return (
        '<div class="status-box">'
        f'<div class="status-label">{escape(label)}</div>'
        f'<div class="status-value">{escape(value)}</div>'
        "</div>"
    )

def _model_options(current_model: str, configured_options: list[str], fallback_model: str) -> list[str]:
    options = list(configured_options)
    if current_model and current_model not in options:
        options.insert(0, current_model)
    return options or [current_model or fallback_model]

def _readonly_field(label: str, value: str, key: str) -> None:
    st.selectbox(label, [value], index=0, key=key, disabled=True)

def _select_model(label: str, profile: dict, field_name: str, options: list[str], key_prefix: str) -> None:
    current_model = str(profile[field_name])
    profile[field_name] = st.selectbox(
        label,
        options,
        index=options.index(current_model) if current_model in options else 0,
        key=f"{key_prefix}_{field_name}",
    )

def _select_openrouter_model(label: str, profile: dict, field_name: str) -> None:
    current_model = str(profile[field_name])
    options = _model_options(current_model, list(OPENROUTER_MODEL_OPTIONS), "openai/gpt-oss-120b:free")
    _select_model(label, profile, field_name, options, "openrouter")

def _select_ollama_model(label: str, profile: dict, field_name: str) -> None:
    current_model = str(profile[field_name])
    options = _model_options(current_model, list(OLLAMA_MODEL_OPTIONS), "qwen2.5-coder:7b")
    _select_model(label, profile, field_name, options, "ollama")

def _render_model_profile(profile: dict, workflow_mode: str) -> None:
    boxes = [_status_box("Mode", str(profile["mode_label"]))]
    if workflow_mode == RAG_WORKFLOW:
        boxes.append(_status_box("Embedding Backend", str(profile.get("embedding_backend", profile["backend"]))))
        boxes.append(_status_box("Embedding", str(profile["embed_model"])))
    elif workflow_mode != HISTORY_WORKFLOW:
        boxes.extend(
            [
                _status_box("Requirement", str(profile["requirement_model"])),
                _status_box("Planning", str(profile["planning_model"])),
                _status_box("Code Generator", str(profile["generator_model"])),
                _status_box("Code Review", str(profile["review_model"])),
                _status_box("Embedding Backend", str(profile.get("embedding_backend", profile["backend"]))),
                _status_box("Embedding", str(profile["embed_model"])),
            ]
        )
    st.markdown("\n".join(boxes), unsafe_allow_html=True)

def _render_openrouter_model_profile(profile: dict, workflow_mode: str) -> None:
    _readonly_field("Mode", str(profile["mode_label"]), "openrouter_mode_label")
    if workflow_mode == RAG_WORKFLOW:
        _readonly_field("Embedding Backend", str(profile.get("embedding_backend", "ollama")), "openrouter_rag_embedding_backend")
        _readonly_field("Embedding", str(profile["embed_model"]), "openrouter_rag_embed_model")
        return
    if workflow_mode == HISTORY_WORKFLOW:
        return

    _select_openrouter_model("Requirement", profile, "requirement_model")
    _select_openrouter_model("Planning", profile, "planning_model")
    _select_openrouter_model("Code Generator", profile, "generator_model")
    _select_openrouter_model("Code Review", profile, "review_model")
    _readonly_field("Embedding Backend", str(profile.get("embedding_backend", "ollama")), "openrouter_embedding_backend")
    _readonly_field("Embedding", str(profile["embed_model"]), "openrouter_embed_model")

def _render_ollama_model_profile(profile: dict, workflow_mode: str) -> None:
    _readonly_field("Mode", str(profile["mode_label"]), "ollama_mode_label")
    if workflow_mode == RAG_WORKFLOW:
        _readonly_field("Embedding Backend", str(profile.get("embedding_backend", "ollama")), "ollama_rag_embedding_backend")
        _readonly_field("Embedding", str(profile["embed_model"]), "ollama_rag_embed_model")
        return
    if workflow_mode == HISTORY_WORKFLOW:
        return

    _select_ollama_model("Requirement", profile, "requirement_model")
    _select_ollama_model("Planning", profile, "planning_model")
    _select_ollama_model("Code Generator", profile, "generator_model")
    _select_ollama_model("Code Review", profile, "review_model")
    _readonly_field("Embedding Backend", str(profile.get("embedding_backend", "ollama")), "ollama_embedding_backend")
    _readonly_field("Embedding", str(profile["embed_model"]), "ollama_embed_model")

def _render_gemini_model_profile(profile: dict, workflow_mode: str) -> None:
    _readonly_field("Mode", str(profile["mode_label"]), "gemini_mode_label")
    if workflow_mode == RAG_WORKFLOW:
        _readonly_field("Embedding Backend", str(profile.get("embedding_backend", "gemini")), "gemini_rag_embedding_backend")
        _readonly_field("Embedding", str(profile["embed_model"]), "gemini_rag_embed_model")
        return
    if workflow_mode == HISTORY_WORKFLOW:
        return

    _readonly_field("Requirement", str(profile["requirement_model"]), "gemini_requirement_model")
    _readonly_field("Planning", str(profile["planning_model"]), "gemini_planning_model")
    _readonly_field("Code Generator", str(profile["generator_model"]), "gemini_generator_model")
    _readonly_field("Code Review", str(profile["review_model"]), "gemini_review_model")
    _readonly_field("Embedding Backend", str(profile.get("embedding_backend", "gemini")), "gemini_embedding_backend")
    _readonly_field("Embedding", str(profile["embed_model"]), "gemini_embed_model")

def _profile_ollama_models(profile: dict, selected_mode: str) -> list[str]:
    if selected_mode == "OpenRouter":
        return [str(profile["embed_model"])]
    return [
        str(profile["requirement_model"]),
        str(profile["planning_model"]),
        str(profile["generator_model"]),
        str(profile["review_model"]),
        str(profile["embed_model"]),
    ]

def render_sidebar() -> tuple[str, str, str, str, str, dict, bool]:
    with st.sidebar:
        st.subheader("Thiết lập phiên chạy")
        selected_mode = st.radio("Chế độ chạy", MODE_OPTIONS, index=1, horizontal=False, key="selected_mode")
        profile = profile_for_mode(selected_mode)
        normalized_workflow = _initial_workflow_value()
        wf_label = workflow_label(normalized_workflow)
        selected_workflow_label = st.selectbox(
            "Khu vực làm việc",
            WORKFLOW_LABEL_OPTIONS,
            index=WORKFLOW_LABEL_OPTIONS.index(wf_label),
            key=WORKFLOW_WIDGET_KEY,
        )
        workflow_mode = LEGACY_WORKFLOW_LOOKUP.get(selected_workflow_label, RAG_WORKFLOW)

        framework = "pytest"
        test_technique = "Hybrid"
        if workflow_mode in {GENERATE_WORKFLOW, REVIEW_WORKFLOW}:
            framework_label = st.selectbox("Khung kiểm thử", [label for label, _ in FRAMEWORK_OPTIONS])
            framework = FRAMEWORK_LOOKUP[framework_label]
            test_technique = st.selectbox("Cách tiếp cận kiểm thử", TEST_TECHNIQUE_OPTIONS, index=0)

        _wf_desc = {
            GENERATE_WORKFLOW: "📝 Sinh mã kiểm thử tự động từ yêu cầu + source code.",
            REVIEW_WORKFLOW: "🔍 Rà soát chất lượng test code có sẵn.",
            RAG_WORKFLOW: "📂 Quản lý tài liệu RAG cho hệ thống.",
            HISTORY_WORKFLOW: "📜 Xem lịch sử các lần chạy trước.",
        }
        if _wf_desc.get(workflow_mode):
            st.caption(_wf_desc[workflow_mode])

        gemini_api_key = ""
        if selected_mode == "API key":
            gemini_api_key = st.text_input(
                "Gemini API key",
                type="password",
                key="gemini_api_key",
                placeholder="Nhập Gemini API key",
            )
            st.caption("Khóa chỉ giữ trong phiên hiện tại.")
        elif selected_mode == "OpenRouter API Key":
            gemini_api_key = st.text_input(
                "OpenRouter API key",
                type="password",
                key="openrouter_api_key",
                placeholder="sk-or-v1-...",
            )
            st.caption("Dùng 5 model miễn phí từ 5 hãng AI. Khóa chỉ giữ trong phiên hiện tại.")

        with st.expander("Model đang dùng", expanded=False):
            if selected_mode == "OpenRouter API Key":
                _render_openrouter_model_profile(profile, workflow_mode)
            elif selected_mode == "Local AI":
                _render_ollama_model_profile(profile, workflow_mode)
            else:
                _render_gemini_model_profile(profile, workflow_mode)


        
        use_preindexed_docs = False
        if workflow_mode == GENERATE_WORKFLOW:
            use_preindexed_docs = st.checkbox(
                "Sử dụng tài liệu đã RAG", 
                value=True, 
                help="Nếu bật, hệ thống sẽ tự động truy xuất tài liệu từ cơ sở dữ liệu ChromaDB. Nếu chưa có kho tài liệu, hệ thống vẫn sẽ chạy bình thường."
            )
        
    return selected_mode, workflow_mode, framework, test_technique, gemini_api_key, profile, use_preindexed_docs
