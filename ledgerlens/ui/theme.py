from __future__ import annotations

from types import MappingProxyType

import streamlit as st

COLORS = MappingProxyType(
    {
        "background": "#08111F",
        "surface": "#111B2E",
        "surface_elevated": "#16233A",
        "border": "#263653",
        "primary": "#4F8CFF",
        "secondary": "#2DD4BF",
        "positive": "#22C55E",
        "negative": "#F87171",
        "warning": "#F5B942",
        "text": "#F8FAFC",
        "text_muted": "#94A3B8",
    }
)


def stylesheet() -> str:
    """Return the offline-first application stylesheet."""
    return f"""
<style>
    :root {{
        --ll-background: {COLORS["background"]};
        --ll-surface: {COLORS["surface"]};
        --ll-surface-elevated: {COLORS["surface_elevated"]};
        --ll-border: {COLORS["border"]};
        --ll-primary: {COLORS["primary"]};
        --ll-secondary: {COLORS["secondary"]};
        --ll-positive: {COLORS["positive"]};
        --ll-negative: {COLORS["negative"]};
        --ll-warning: {COLORS["warning"]};
        --ll-text: {COLORS["text"]};
        --ll-text-muted: {COLORS["text_muted"]};
        --ll-radius-sm: 10px;
        --ll-radius-md: 16px;
        --ll-radius-lg: 22px;
        --ll-shadow: 0 18px 45px rgba(0, 0, 0, 0.2);
    }}

    .stApp {{
        color: var(--ll-text);
        background:
            radial-gradient(circle at 75% -10%, rgba(79, 140, 255, 0.16), transparent 34rem),
            radial-gradient(circle at -10% 35%, rgba(45, 212, 191, 0.08), transparent 30rem),
            var(--ll-background);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
            "Segoe UI", sans-serif;
    }}

    [data-testid="stHeader"] {{ background: transparent; }}
    [data-testid="stToolbar"] {{ right: 1rem; }}

    .block-container {{
        max-width: 1440px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }}

    h1, h2, h3, h4, p, label {{ color: var(--ll-text); }}

    [data-baseweb="tab-list"] {{
        gap: 0.35rem;
        padding: 0.35rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 14px;
        background: rgba(17, 27, 46, 0.78);
        backdrop-filter: blur(16px);
    }}

    [data-baseweb="tab"] {{
        min-height: 2.75rem;
        padding: 0.55rem 1rem;
        border-radius: 10px;
    }}

    [aria-selected="true"][data-baseweb="tab"] {{
        background: rgba(79, 140, 255, 0.14);
    }}

    [data-baseweb="tab-highlight"] {{ background-color: var(--ll-primary); }}

    [data-testid="stDataFrame"], [data-testid="stFileUploader"],
    [data-testid="stExpander"], [data-testid="stForm"] {{
        border-color: rgba(148, 163, 184, 0.18);
        border-radius: var(--ll-radius-md);
        overflow: hidden;
    }}

    .stButton > button[kind="primary"],
    .stDownloadButton > button {{
        min-height: 2.75rem;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: var(--ll-radius-sm);
        background: linear-gradient(135deg, var(--ll-primary), #366FD9);
        color: #FFFFFF;
        font-weight: 700;
        box-shadow: 0 10px 24px rgba(79, 140, 255, 0.2);
    }}

    .stButton > button:focus-visible,
    .stDownloadButton > button:focus-visible {{
        outline: 3px solid rgba(45, 212, 191, 0.6);
        outline-offset: 2px;
    }}

    .ll-app-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1.15rem;
    }}

    .ll-brand {{ display: flex; align-items: center; gap: 0.9rem; }}

    .ll-brand-mark {{
        display: grid;
        width: 2.8rem;
        height: 2.8rem;
        place-items: center;
        border: 1px solid rgba(79, 140, 255, 0.5);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(79, 140, 255, 0.3), rgba(45, 212, 191, 0.12));
        color: #FFFFFF;
        font-size: 0.83rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        box-shadow: 0 12px 28px rgba(79, 140, 255, 0.16);
    }}

    .ll-brand-name {{
        margin: 0;
        color: var(--ll-text);
        font-size: clamp(1.45rem, 3vw, 2rem);
        font-weight: 760;
        letter-spacing: -0.035em;
        line-height: 1.05;
    }}

    .ll-brand-copy {{
        margin: 0.28rem 0 0;
        color: var(--ll-text-muted);
        font-size: 0.9rem;
    }}

    .ll-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        min-height: 2rem;
        padding: 0.38rem 0.7rem;
        border: 1px solid rgba(45, 212, 191, 0.3);
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.09);
        color: #99F6E4;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.055em;
        text-transform: uppercase;
        white-space: nowrap;
    }}

    .ll-badge-dot {{
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 999px;
        background: var(--ll-secondary);
        box-shadow: 0 0 0 4px rgba(45, 212, 191, 0.12);
    }}

    .ll-notice {{
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
        margin: 0.25rem 0 1.1rem;
        padding: 0.85rem 1rem;
        border: 1px solid rgba(79, 140, 255, 0.24);
        border-radius: var(--ll-radius-md);
        background: linear-gradient(90deg, rgba(79, 140, 255, 0.11), rgba(17, 27, 46, 0.68));
        color: #CBD5E1;
        font-size: 0.88rem;
        line-height: 1.5;
    }}

    .ll-notice-icon {{ color: var(--ll-primary); font-weight: 800; }}

    .ll-section-heading {{
        margin: 0 0 0.25rem;
        color: var(--ll-text);
        font-size: 1.18rem;
        font-weight: 730;
        letter-spacing: -0.02em;
    }}

    .ll-section-copy {{
        margin: 0 0 1rem;
        color: var(--ll-text-muted);
        font-size: 0.88rem;
    }}

    .ll-kpi-card {{
        min-height: 8.25rem;
        padding: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: var(--ll-radius-md);
        background: linear-gradient(145deg, rgba(22, 35, 58, 0.96), rgba(17, 27, 46, 0.9));
        box-shadow: var(--ll-shadow);
    }}

    .ll-kpi-card[data-tone="positive"] {{ border-top-color: rgba(34, 197, 94, 0.72); }}
    .ll-kpi-card[data-tone="negative"] {{ border-top-color: rgba(248, 113, 113, 0.72); }}
    .ll-kpi-card[data-tone="primary"] {{ border-top-color: rgba(79, 140, 255, 0.72); }}

    .ll-kpi-label {{
        color: var(--ll-text-muted);
        font-size: 0.77rem;
        font-weight: 680;
        letter-spacing: 0.055em;
        text-transform: uppercase;
    }}

    .ll-kpi-value {{
        margin-top: 0.55rem;
        color: var(--ll-text);
        font-size: clamp(1.25rem, 2vw, 1.75rem);
        font-variant-numeric: tabular-nums;
        font-weight: 760;
        letter-spacing: -0.035em;
    }}

    .ll-kpi-delta {{
        margin-top: 0.35rem;
        color: var(--ll-text-muted);
        font-size: 0.82rem;
        font-variant-numeric: tabular-nums;
    }}

    .ll-kpi-card[data-tone="positive"] .ll-kpi-delta {{ color: #86EFAC; }}
    .ll-kpi-card[data-tone="negative"] .ll-kpi-delta {{ color: #FCA5A5; }}
    .ll-kpi-card[data-tone="primary"] .ll-kpi-delta {{ color: #93C5FD; }}

    @media (max-width: 768px) {{
        .block-container {{ padding: 1rem 1rem 3rem; }}
        .ll-app-header {{ align-items: flex-start; }}
        .ll-brand-copy {{ max-width: 28rem; }}
        [data-baseweb="tab-list"] {{ overflow-x: auto; scrollbar-width: thin; }}
        [data-baseweb="tab"] {{ flex: 0 0 auto; }}
    }}

    @media (max-width: 480px) {{
        .ll-app-header {{ flex-direction: column; }}
        .ll-brand-mark {{ width: 2.5rem; height: 2.5rem; }}
        .ll-notice {{ padding: 0.75rem; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
            animation-duration: 0.01ms !important;
        }}
    }}
</style>
"""


def apply_theme() -> None:
    """Inject LedgerLens theme tokens and responsive application styles."""
    st.markdown(stylesheet(), unsafe_allow_html=True)

