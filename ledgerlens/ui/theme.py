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
        "lavender": "#9B87F5",
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
        --ll-lavender: {COLORS["lavender"]};
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

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: rgba(148, 163, 184, 0.16) !important;
        border-radius: var(--ll-radius-md) !important;
        background: linear-gradient(145deg, rgba(17, 27, 46, 0.78), rgba(8, 17, 31, 0.72));
        box-shadow: 0 16px 38px rgba(0, 0, 0, 0.14);
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

    .ll-brand-identity {{ display: flex; flex-direction: column; align-items: flex-start; }}

    .ll-brand-lockup {{
        display: block;
        width: min(18.25rem, 52vw);
        height: auto;
    }}

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

    .ll-project-flow {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.75rem;
        margin: 0.8rem 0 1.4rem;
    }}

    .ll-project-step {{
        min-height: 8.7rem;
        padding: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: var(--ll-radius-md);
        background: linear-gradient(145deg, rgba(17, 27, 46, 0.9), rgba(8, 17, 31, 0.7));
    }}

    .ll-project-step span {{
        display: inline-grid;
        width: 1.8rem;
        height: 1.8rem;
        place-items: center;
        margin-bottom: 0.75rem;
        border-radius: 999px;
        background: rgba(79, 140, 255, 0.14);
        color: #BFDBFE;
        font-size: 0.72rem;
        font-weight: 800;
    }}

    .ll-project-step:nth-child(2) span {{
        background: rgba(155, 135, 245, 0.14);
        color: #DDD6FE;
    }}

    .ll-project-step:nth-child(3) span,
    .ll-project-step:nth-child(4) span {{
        background: rgba(45, 212, 191, 0.12);
        color: #99F6E4;
    }}

    .ll-project-step strong {{ display: block; color: var(--ll-text); font-size: 0.9rem; }}
    .ll-project-step p {{
        margin: 0.35rem 0 0;
        color: var(--ll-text-muted);
        font-size: 0.78rem;
        line-height: 1.45;
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

    .ll-position-card {{
        min-height: 18.5rem;
        padding: 1.05rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: var(--ll-radius-md);
        background: linear-gradient(155deg, rgba(22, 35, 58, 0.96), rgba(12, 23, 40, 0.96));
        box-shadow: var(--ll-shadow);
    }}

    .ll-position-card[data-tone="positive"] {{ border-top-color: rgba(34, 197, 94, 0.72); }}
    .ll-position-card[data-tone="negative"] {{ border-top-color: rgba(248, 113, 113, 0.72); }}

    .ll-position-topline {{
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.75rem;
    }}

    .ll-position-company {{
        color: var(--ll-text);
        font-size: 0.94rem;
        font-weight: 720;
    }}

    .ll-position-ticker {{
        margin-top: 0.18rem;
        color: var(--ll-text-muted);
        font-size: 0.74rem;
        font-weight: 650;
        letter-spacing: 0.045em;
    }}

    .ll-position-allocation {{
        padding: 0.25rem 0.48rem;
        border: 1px solid rgba(79, 140, 255, 0.25);
        border-radius: 999px;
        background: rgba(79, 140, 255, 0.1);
        color: #BFDBFE;
        font-size: 0.72rem;
        font-weight: 700;
    }}

    .ll-position-value {{
        margin-top: 1.15rem;
        color: var(--ll-text);
        font-size: clamp(1.2rem, 2vw, 1.55rem);
        font-variant-numeric: tabular-nums;
        font-weight: 760;
        letter-spacing: -0.03em;
    }}

    .ll-position-return {{
        margin-top: 0.32rem;
        color: var(--ll-text-muted);
        font-size: 0.82rem;
        font-weight: 650;
    }}

    .ll-position-card[data-tone="positive"] .ll-position-return {{ color: #86EFAC; }}
    .ll-position-card[data-tone="negative"] .ll-position-return {{ color: #FCA5A5; }}

    .ll-position-details {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.85rem 0.7rem;
        margin: 1.15rem 0 0;
        padding-top: 1rem;
        border-top: 1px solid rgba(148, 163, 184, 0.13);
    }}

    .ll-position-details div {{ min-width: 0; }}
    .ll-position-details dt {{ color: var(--ll-text-muted); font-size: 0.69rem; }}
    .ll-position-details dd {{
        margin: 0.2rem 0 0;
        overflow-wrap: anywhere;
        color: #E2E8F0;
        font-size: 0.77rem;
        font-variant-numeric: tabular-nums;
        font-weight: 630;
    }}

    .ll-platform-row + .ll-platform-row {{ margin-top: 0.9rem; }}

    .ll-platform-labels {{
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.42rem;
        color: #E2E8F0;
        font-size: 0.82rem;
        font-weight: 650;
    }}

    .ll-platform-labels span:last-child {{
        color: var(--ll-text-muted);
        font-variant-numeric: tabular-nums;
        font-weight: 560;
    }}

    .ll-platform-track {{
        height: 0.46rem;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.12);
    }}

    .ll-platform-fill {{
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--ll-primary), var(--ll-secondary));
    }}

    .ll-chart-legend {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.55rem 0.9rem;
        margin: -0.25rem 0 0.35rem;
    }}

    .ll-chart-legend-item {{
        display: inline-flex;
        align-items: center;
        gap: 0.36rem;
        color: var(--ll-text-muted);
        font-size: 0.72rem;
        font-weight: 620;
    }}

    .ll-chart-legend-dot {{
        width: 0.52rem;
        height: 0.52rem;
        border-radius: 999px;
    }}

    .ll-quality-panel {{
        padding: 1rem;
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: var(--ll-radius-md);
        background: rgba(8, 17, 31, 0.5);
    }}

    .ll-quality-panel[data-quality="good"] {{ border-left-color: var(--ll-positive); }}
    .ll-quality-panel[data-quality="partial"] {{ border-left-color: var(--ll-warning); }}
    .ll-quality-panel[data-quality="insufficient"] {{ border-left-color: var(--ll-negative); }}

    .ll-quality-topline {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.9rem;
    }}

    .ll-quality-label {{
        color: var(--ll-text);
        font-size: 0.86rem;
        font-weight: 720;
    }}

    .ll-quality-status {{
        padding: 0.25rem 0.52rem;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.1);
        color: var(--ll-text-muted);
        font-size: 0.7rem;
        font-weight: 720;
        letter-spacing: 0.035em;
        text-transform: uppercase;
    }}

    .ll-quality-panel[data-quality="good"] .ll-quality-status {{
        background: rgba(34, 197, 94, 0.1); color: #86EFAC;
    }}
    .ll-quality-panel[data-quality="partial"] .ll-quality-status {{
        background: rgba(245, 185, 66, 0.1); color: #FCD34D;
    }}
    .ll-quality-panel[data-quality="insufficient"] .ll-quality-status {{
        background: rgba(248, 113, 113, 0.1); color: #FCA5A5;
    }}

    .ll-quality-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; }}
    .ll-quality-grid div {{ min-width: 0; }}
    .ll-quality-grid span {{ display: block; color: var(--ll-text-muted); font-size: 0.68rem; }}
    .ll-quality-grid strong {{
        display: block;
        margin-top: 0.24rem;
        overflow-wrap: anywhere;
        color: #E2E8F0;
        font-size: 0.77rem;
        font-weight: 650;
    }}

    .ll-workflow {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.5rem;
        margin: 0.5rem 0 1.25rem;
    }}

    .ll-workflow-step {{
        position: relative;
        display: flex;
        align-items: center;
        gap: 0.55rem;
        min-width: 0;
        padding: 0.65rem 0.72rem;
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: var(--ll-radius-sm);
        background: rgba(17, 27, 46, 0.55);
    }}

    .ll-workflow-step[data-state="active"] {{
        border-color: rgba(79, 140, 255, 0.58);
        background: rgba(79, 140, 255, 0.1);
    }}

    .ll-workflow-step[data-state="completed"] {{ border-color: rgba(45, 212, 191, 0.28); }}

    .ll-workflow-marker {{
        display: grid;
        flex: 0 0 auto;
        width: 1.55rem;
        height: 1.55rem;
        place-items: center;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.12);
        color: var(--ll-text-muted);
        font-size: 0.7rem;
        font-weight: 750;
    }}

    .ll-workflow-step[data-state="active"] .ll-workflow-marker {{
        background: var(--ll-primary); color: #FFFFFF;
    }}
    .ll-workflow-step[data-state="completed"] .ll-workflow-marker {{
        background: rgba(45, 212, 191, 0.14); color: #5EEAD4;
    }}

    .ll-workflow-label {{
        overflow: hidden;
        color: var(--ll-text-muted);
        font-size: 0.77rem;
        font-weight: 680;
        text-overflow: ellipsis;
    }}
    .ll-workflow-step[data-state="active"] .ll-workflow-label {{ color: #DBEAFE; }}

    .ll-policy-card {{
        display: flex;
        gap: 0.9rem;
        min-height: 10rem;
        padding: 1rem;
        border: 1px solid rgba(45, 212, 191, 0.2);
        border-radius: var(--ll-radius-md);
        background: linear-gradient(145deg, rgba(45, 212, 191, 0.07), rgba(17, 27, 46, 0.62));
    }}

    .ll-policy-icon {{
        display: grid;
        flex: 0 0 auto;
        width: 2.5rem;
        height: 2.5rem;
        place-items: center;
        border-radius: 12px;
        background: rgba(45, 212, 191, 0.12);
        color: #5EEAD4;
        font-size: 0.68rem;
        font-weight: 800;
    }}

    .ll-policy-title {{ color: var(--ll-text); font-size: 0.9rem; font-weight: 720; }}
    .ll-policy-card p {{
        margin: 0.45rem 0 0;
        color: var(--ll-text-muted);
        font-size: 0.78rem;
        line-height: 1.45;
    }}

    .ll-source-metadata {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.55rem 0.8rem;
        margin: 0.35rem 0 1rem;
        color: var(--ll-text-muted);
        font-size: 0.72rem;
        font-variant-numeric: tabular-nums;
    }}

    .ll-source-badge {{
        padding: 0.3rem 0.55rem;
        border-radius: 999px;
        background: rgba(45, 212, 191, 0.1);
        color: #99F6E4;
        font-weight: 720;
    }}
    .ll-source-badge[data-source="ai"] {{ background: rgba(79, 140, 255, 0.12); color: #BFDBFE; }}

    .ll-confidence-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.9rem 1rem;
    }}
    .ll-confidence-item > div:first-child {{
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }}
    .ll-confidence-item span {{ color: var(--ll-text-muted); font-size: 0.73rem; }}
    .ll-confidence-item strong {{
        color: #E2E8F0;
        font-size: 0.73rem;
        font-variant-numeric: tabular-nums;
    }}
    .ll-confidence-track {{
        height: 0.38rem;
        margin-top: 0.35rem;
        overflow: hidden;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.12);
    }}
    .ll-confidence-fill {{
        height: 100%;
        border-radius: inherit;
        background: linear-gradient(90deg, var(--ll-primary), var(--ll-secondary));
    }}

    @media (max-width: 768px) {{
        .block-container {{ padding: 1rem 1rem 3rem; }}
        .ll-app-header {{ align-items: flex-start; }}
        .ll-brand-copy {{ max-width: 28rem; }}
        [data-baseweb="tab-list"] {{ overflow-x: auto; scrollbar-width: thin; }}
        [data-baseweb="tab"] {{ flex: 0 0 auto; }}
        .ll-workflow {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .ll-project-flow {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}

    @media (max-width: 480px) {{
        .ll-app-header {{ flex-direction: column; }}
        .ll-brand-mark {{ width: 2.5rem; height: 2.5rem; }}
        .ll-brand-lockup {{ width: min(16rem, 78vw); }}
        .ll-notice {{ padding: 0.75rem; }}
        .ll-kpi-card {{ min-height: auto; }}
        .ll-position-card {{ min-height: auto; }}
        .ll-platform-labels {{ align-items: flex-start; flex-direction: column; gap: 0.2rem; }}
        .ll-quality-grid {{ grid-template-columns: 1fr; }}
        .ll-confidence-grid {{ grid-template-columns: 1fr; }}
        .ll-project-flow {{ grid-template-columns: 1fr; }}
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
