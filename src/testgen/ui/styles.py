import streamlit as st


def apply_custom_styles():
    st.html(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
        :root {
            --bg-soft: #f3f8f6;
            --surface: #ffffff;
            --surface-2: #f8fbfa;
            --line: #dde7e3;
            --line-soft: #eef3f1;
            --text-main: #111c18;
            --text-muted: #5a6f69;
            --primary: #0d6e56;
            --primary-hover: #0b5f49;
            --primary-soft: #e4f4ef;
            --accent: #1a9b7e;
            --note-soft: #eef3ff;
            --warn-soft: #fff8ec;
            --danger-soft: #fff0f0;
            --success: #16a34a;
            --warning: #d97706;
            --danger: #dc2626;
        }

        /* ── Base ── */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        .stApp {
            background: linear-gradient(160deg, var(--bg-soft) 0%, #f7fbf9 50%, #ffffff 100%);
            color: var(--text-main);
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1360px;
        }

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: #f9fcfb;
            border-right: 1px solid var(--line);
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.9rem;
        }

        /* ── Hero banner ── */
        .app-hero {
            border: 1px solid var(--line);
            border-radius: 16px;
            background: linear-gradient(135deg, #ffffff 0%, #edf8f4 60%, #e0f4ee 100%);
            padding: 1.1rem 1.3rem 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(13, 110, 86, 0.07);
        }
        .app-hero-title {
            font-size: 1.4rem;
            font-weight: 800;
            color: #0a3d2e;
            margin-bottom: 0.25rem;
            letter-spacing: -0.3px;
        }
        .app-hero-subtitle {
            color: var(--text-muted);
            line-height: 1.5;
            font-size: 0.93rem;
        }
        .app-hero-badge {
            display: inline-block;
            background: var(--primary-soft);
            color: var(--primary);
            border: 1px solid rgba(13,110,86,0.2);
            border-radius: 999px;
            padding: 0.12rem 0.6rem;
            font-size: 0.75rem;
            font-weight: 700;
            margin-left: 0.5rem;
            vertical-align: middle;
        }

        /* ── Section note ── */
        .section-note {
            border: 1px solid #d6e4ff;
            border-radius: 10px;
            background: var(--note-soft);
            padding: 0.65rem 0.85rem;
            font-size: 0.89rem;
            color: #2d4a8a;
            margin-bottom: 0.8rem;
        }

        /* ── Flow cards ── */
        .flow-card {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--surface);
            padding: 0.95rem 1.05rem 0.9rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 2px 12px rgba(13, 110, 86, 0.05);
            transition: box-shadow 0.2s ease;
        }
        .flow-card:hover {
            box-shadow: 0 6px 22px rgba(13, 110, 86, 0.1);
        }
        .flow-title {
            font-size: 1rem;
            font-weight: 700;
            color: #0c3d2e;
            margin-bottom: 0.2rem;
        }
        .flow-desc {
            color: var(--text-muted);
            font-size: 0.88rem;
            line-height: 1.5;
            margin-bottom: 0.75rem;
        }

        /* ── Action bar ── */
        .action-bar {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: var(--surface-2);
            padding: 0.7rem 0.85rem;
            margin-top: 0.3rem;
            margin-bottom: 0.8rem;
        }
        .action-title {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.2rem;
        }
        .action-desc {
            color: var(--text-muted);
            font-size: 0.83rem;
            line-height: 1.45;
        }

        /* ── Inputs ── */
        div[data-testid="stTextArea"] textarea {
            min-height: 240px;
            line-height: 1.55;
            border-radius: 10px;
            border-color: var(--line) !important;
            font-size: 0.92rem;
        }
        div[data-testid="stFileUploaderDropzone"] {
            border-radius: 12px;
        }

        /* ── Metric ── */
        [data-testid="stMetricValue"] {
            font-size: 1.08rem;
            font-weight: 700;
            color: var(--text-main);
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.77rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* ── Status boxes (sidebar) ── */
        .status-box {
            border: 1px solid var(--line-soft);
            border-radius: 10px;
            padding: 0.55rem 0.72rem;
            background: var(--surface);
            margin-bottom: 0.48rem;
        }
        .status-label {
            color: var(--text-muted);
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 0.1rem;
        }
        .status-value {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.35;
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        /* ── Verdict badge ── */
        .verdict-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            border-radius: 10px;
            padding: 0.45rem 0.9rem;
            font-size: 0.92rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .verdict-pass   { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
        .verdict-warn   { background: #fef9c3; color: #a16207; border: 1px solid #fde047; }
        .verdict-danger { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

        /* ── Score pillar bar ── */
        .pillar-bar-wrap { margin-bottom: 0.25rem; }
        .pillar-bar-label {
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 0.18rem;
            display: flex;
            justify-content: space-between;
        }
        .pillar-bar-track {
            height: 7px;
            border-radius: 999px;
            background: var(--line-soft);
            overflow: hidden;
        }
        .pillar-bar-fill {
            height: 100%;
            border-radius: 999px;
            transition: width 0.4s ease;
        }
        .pillar-green  { background: #22c55e; }
        .pillar-yellow { background: #f59e0b; }
        .pillar-red    { background: #ef4444; }

        /* ── Role cards ── */
        .role-card {
            border-radius: 12px;
            padding: 0.75rem 0.9rem;
            margin-bottom: 0.7rem;
            border: 1px solid var(--line);
        }
        .role-card-source {
            background: var(--primary-soft);
            border-color: rgba(13, 110, 86, 0.25);
        }
        .role-card-test {
            background: var(--warn-soft);
            border-color: rgba(196, 122, 34, 0.22);
        }
        .role-card-title {
            font-size: 0.88rem;
            font-weight: 800;
            margin-bottom: 0.15rem;
            color: var(--text-main);
        }
        .role-card-body {
            font-size: 0.83rem;
            line-height: 1.5;
            color: var(--text-muted);
        }

        /* ── Compact note ── */
        .compact-note {
            color: var(--text-muted);
            font-size: 0.88rem;
            line-height: 1.5;
        }

        /* ── Dataframe ── */
        div[data-testid="stDataFrame"] {
            border-radius: 10px;
            overflow: hidden;
        }

        /* ── Tabs ── */
        button[data-baseweb="tab"] {
            font-weight: 600;
            font-size: 0.88rem;
        }

        /* ── Expander ── */
        details summary {
            font-weight: 600;
            font-size: 0.9rem;
        }
        </style>
        """
    )


def verdict_badge_html(verdict: str) -> str:
    """Render một badge HTML cho verdict."""
    cls_map = {
        "Đạt": "verdict-pass",
        "Hoàn hảo": "verdict-pass",
        "Cần sửa": "verdict-warn",
        "Cần cải thiện": "verdict-warn",
        "Rủi ro cao": "verdict-danger",
        "Cần xem log": "verdict-warn",
    }
    icon_map = {
        "Đạt": "✅",
        "Hoàn hảo": "✅",
        "Cần sửa": "⚠️",
        "Cần cải thiện": "⚠️",
        "Rủi ro cao": "❌",
        "Cần xem log": "⚠️",
    }
    css_cls = cls_map.get(verdict, "verdict-warn")
    icon = icon_map.get(verdict, "❓")
    from html import escape
    return f'<span class="verdict-badge {css_cls}">{icon} {escape(verdict)}</span>'


def pillar_bar_html(label: str, score: int, max_score: int) -> str:
    """Render 1 thanh mini-progress cho 1 Pillar."""
    pct = int(score / max_score * 100) if max_score else 0
    if pct >= 75:
        color_cls = "pillar-green"
    elif pct >= 40:
        color_cls = "pillar-yellow"
    else:
        color_cls = "pillar-red"
    from html import escape
    return (
        '<div class="pillar-bar-wrap">'
        f'<div class="pillar-bar-label"><span>{escape(label)}</span><span>{score}/{max_score}</span></div>'
        '<div class="pillar-bar-track">'
        f'<div class="pillar-bar-fill {color_cls}" style="width:{pct}%"></div>'
        '</div></div>'
    )
