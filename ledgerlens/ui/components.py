from __future__ import annotations

from html import escape
from typing import Literal

import streamlit as st

Tone = Literal["neutral", "primary", "positive", "negative"]


def app_header_html(*, subtitle: str, badge: str = "Synthetic demo") -> str:
    return f"""
<header class="ll-app-header">
  <div class="ll-brand">
    <div class="ll-brand-mark" aria-hidden="true">LL</div>
    <div>
      <div class="ll-brand-name" role="heading" aria-level="1">LedgerLens</div>
      <p class="ll-brand-copy">{escape(subtitle)}</p>
    </div>
  </div>
  <span class="ll-badge"><span class="ll-badge-dot" aria-hidden="true"></span>{escape(badge)}</span>
</header>
"""


def notice_html(message: str) -> str:
    return f"""
<div class="ll-notice" role="note">
  <span class="ll-notice-icon" aria-hidden="true">i</span>
  <span>{escape(message)}</span>
</div>
"""


def section_header_html(title: str, description: str | None = None) -> str:
    copy = f'<p class="ll-section-copy">{escape(description)}</p>' if description else ""
    return f'<h2 class="ll-section-heading">{escape(title)}</h2>{copy}'


def kpi_card_html(
    *,
    label: str,
    value: str,
    delta: str | None = None,
    tone: Tone = "neutral",
) -> str:
    if tone not in {"neutral", "primary", "positive", "negative"}:
        raise ValueError(f"Unsupported KPI tone: {tone}")
    delta_html = f'<div class="ll-kpi-delta">{escape(delta)}</div>' if delta else ""
    return f"""
<div class="ll-kpi-card" data-tone="{tone}">
  <div class="ll-kpi-label">{escape(label)}</div>
  <div class="ll-kpi-value">{escape(value)}</div>
  {delta_html}
</div>
"""


def render_app_header(*, subtitle: str, badge: str = "Synthetic demo") -> None:
    st.markdown(app_header_html(subtitle=subtitle, badge=badge), unsafe_allow_html=True)


def render_notice(message: str) -> None:
    st.markdown(notice_html(message), unsafe_allow_html=True)


def render_section_header(title: str, description: str | None = None) -> None:
    st.markdown(section_header_html(title, description), unsafe_allow_html=True)


def render_kpi_card(
    *,
    label: str,
    value: str,
    delta: str | None = None,
    tone: Tone = "neutral",
) -> None:
    st.markdown(
        kpi_card_html(label=label, value=value, delta=delta, tone=tone),
        unsafe_allow_html=True,
    )
