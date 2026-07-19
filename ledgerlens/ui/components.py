from __future__ import annotations

from base64 import b64encode
from html import escape
from pathlib import Path
from re import fullmatch
from typing import Literal

import streamlit as st

Tone = Literal["neutral", "primary", "positive", "negative"]


def app_header_html(
    *,
    subtitle: str,
    badge: str = "Synthetic demo",
    logo_data_uri: str | None = None,
) -> str:
    if logo_data_uri:
        brand_identity = (
            '<img class="ll-brand-lockup" '
            f'src="{escape(logo_data_uri, quote=True)}" alt="LedgerLens" />'
        )
    else:
        brand_identity = (
            '<div class="ll-brand-mark" aria-hidden="true">LL</div>'
            '<div class="ll-brand-name" role="heading" aria-level="1">LedgerLens</div>'
        )
    return f"""
<header class="ll-app-header">
  <div class="ll-brand">
    <div class="ll-brand-identity">
      {brand_identity}
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
    return (
        f'<div class="ll-section-heading" role="heading" aria-level="2">'
        f"{escape(title)}</div>{copy}"
    )


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


def position_card_html(
    *,
    company: str,
    ticker: str,
    quantity: str,
    average_price: str,
    current_price: str,
    current_value: str,
    pnl: str,
    return_pct: str,
    allocation: str,
    movement: str,
    tone: Tone = "neutral",
) -> str:
    if tone not in {"neutral", "primary", "positive", "negative"}:
        raise ValueError(f"Unsupported position tone: {tone}")
    return f"""
<article class="ll-position-card" data-tone="{tone}" aria-label="{escape(ticker)} position">
  <div class="ll-position-topline">
    <div>
      <div class="ll-position-company">{escape(company)}</div>
      <div class="ll-position-ticker">{escape(ticker)}</div>
    </div>
    <span class="ll-position-allocation">{escape(allocation)}</span>
  </div>
  <div class="ll-position-value">{escape(current_value)}</div>
  <div class="ll-position-return">{escape(return_pct)} · {escape(movement)}</div>
  <dl class="ll-position-details">
    <div><dt>Quantity</dt><dd>{escape(quantity)}</dd></div>
    <div><dt>Avg. price</dt><dd>{escape(average_price)}</dd></div>
    <div><dt>Latest price</dt><dd>{escape(current_price)}</dd></div>
    <div><dt>Unrealized P/L</dt><dd>{escape(pnl)}</dd></div>
  </dl>
</article>
"""


def platform_allocation_html(
    *, platform: str, invested_value: str, allocation: str, bar_width: float
) -> str:
    safe_width = min(max(bar_width, 0.0), 100.0)
    return f"""
<div class="ll-platform-row">
  <div class="ll-platform-labels">
    <span>{escape(platform)}</span>
    <span>{escape(invested_value)} · {escape(allocation)}</span>
  </div>
  <div class="ll-platform-track" aria-label="{escape(platform)} allocation {escape(allocation)}">
    <div class="ll-platform-fill" style="width: {safe_width:.2f}%"></div>
  </div>
</div>
"""


def chart_legend_html(items: list[tuple[str, str]]) -> str:
    entries = "".join(
        (
            '<span class="ll-chart-legend-item">'
            f'<span class="ll-chart-legend-dot" style="background: '
            f'{color if fullmatch(r"#[0-9A-Fa-f]{6}", color) else "#94A3B8"}"></span>'
            f"{escape(label)}</span>"
        )
        for label, color in items
    )
    return f'<div class="ll-chart-legend" aria-label="Chart legend">{entries}</div>'


def quality_summary_html(
    *,
    quality: str,
    coverage: str,
    missing_tickers: tuple[str, ...],
    stale_tickers: tuple[str, ...],
) -> str:
    if quality not in {"good", "partial", "insufficient"}:
        raise ValueError(f"Unsupported context quality: {quality}")
    quality_label = {
        "good": "Good context",
        "partial": "Partial context",
        "insufficient": "Insufficient context",
    }[quality]
    missing = ", ".join(missing_tickers) or "None"
    stale = ", ".join(stale_tickers) or "None"
    return f"""
<div class="ll-quality-panel" data-quality="{quality}" role="status">
  <div class="ll-quality-topline">
    <span class="ll-quality-label">Data quality</span>
    <span class="ll-quality-status">{quality_label}</span>
  </div>
  <div class="ll-quality-grid">
    <div><span>Price coverage</span><strong>{escape(coverage)}</strong></div>
    <div><span>Missing prices</span><strong>{escape(missing)}</strong></div>
    <div><span>Stale prices</span><strong>{escape(stale)}</strong></div>
  </div>
</div>
"""


def workflow_steps_html(current_step: str) -> str:
    steps = ("Upload", "Extract", "Review", "Confirm")
    if current_step not in {step.lower() for step in steps}:
        raise ValueError(f"Unsupported workflow step: {current_step}")
    current_index = [step.lower() for step in steps].index(current_step)
    items = []
    for index, step in enumerate(steps):
        state = (
            "completed"
            if index < current_index
            else "active"
            if index == current_index
            else "pending"
        )
        marker = "✓" if state == "completed" else str(index + 1)
        items.append(
            f'<div class="ll-workflow-step" data-state="{state}">'
            f'<span class="ll-workflow-marker">{marker}</span>'
            f'<span class="ll-workflow-label">{step}</span></div>'
        )
    return (
        '<div class="ll-workflow" aria-label="Invoice import progress">'
        + "".join(items)
        + "</div>"
    )


def document_policy_html() -> str:
    return """
<div class="ll-policy-card" role="note">
  <div class="ll-policy-icon" aria-hidden="true">PDF</div>
  <div>
    <div class="ll-policy-title">Private by design</div>
    <p>The PDF is validated and processed in memory. It is never stored by LedgerLens.</p>
    <p>Only confirmed fields and the document SHA-256 are retained for traceability.</p>
  </div>
</div>
"""


def source_metadata_html(*, source: str, size_bytes: int, sha256_prefix: str) -> str:
    is_ai = "openai" in source.lower()
    source_kind = "ai" if is_ai else "offline"
    source_label = "OpenAI extraction" if is_ai else "Offline fixture"
    return f"""
<div class="ll-source-metadata">
  <span class="ll-source-badge" data-source="{source_kind}">{source_label}</span>
  <span>{size_bytes:,} bytes</span>
  <span>SHA-256 {escape(sha256_prefix)}…</span>
</div>
"""


def confidence_grid_html(confidence: dict[str, float]) -> str:
    items = []
    for field, raw_value in confidence.items():
        value = min(max(float(raw_value), 0.0), 1.0)
        label = field.replace("_", " ").title()
        items.append(
            '<div class="ll-confidence-item">'
            f'<div><span>{escape(label)}</span><strong>{value:.0%}</strong></div>'
            '<div class="ll-confidence-track" '
            f'aria-label="{escape(label)} confidence {value:.0%}">'
            f'<div class="ll-confidence-fill" style="width: {value * 100:.2f}%"></div>'
            "</div></div>"
        )
    return '<div class="ll-confidence-grid">' + "".join(items) + "</div>"


def render_app_header(
    *,
    subtitle: str,
    badge: str = "Synthetic demo",
    logo_path: str | Path | None = None,
) -> None:
    logo_data_uri = None
    if logo_path is not None:
        path = Path(logo_path)
        if path.suffix.lower() != ".png":
            raise ValueError("The application header logo must be a PNG asset.")
        logo_data_uri = f"data:image/png;base64,{b64encode(path.read_bytes()).decode('ascii')}"
    st.markdown(
        app_header_html(
            subtitle=subtitle,
            badge=badge,
            logo_data_uri=logo_data_uri,
        ),
        unsafe_allow_html=True,
    )


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


def render_position_card(
    *,
    company: str,
    ticker: str,
    quantity: str,
    average_price: str,
    current_price: str,
    current_value: str,
    pnl: str,
    return_pct: str,
    allocation: str,
    movement: str,
    tone: Tone = "neutral",
) -> None:
    st.markdown(
        position_card_html(
            company=company,
            ticker=ticker,
            quantity=quantity,
            average_price=average_price,
            current_price=current_price,
            current_value=current_value,
            pnl=pnl,
            return_pct=return_pct,
            allocation=allocation,
            movement=movement,
            tone=tone,
        ),
        unsafe_allow_html=True,
    )


def render_platform_allocation(
    *, platform: str, invested_value: str, allocation: str, bar_width: float
) -> None:
    st.markdown(
        platform_allocation_html(
            platform=platform,
            invested_value=invested_value,
            allocation=allocation,
            bar_width=bar_width,
        ),
        unsafe_allow_html=True,
    )


def render_chart_legend(items: list[tuple[str, str]]) -> None:
    st.markdown(chart_legend_html(items), unsafe_allow_html=True)


def render_quality_summary(
    *,
    quality: str,
    coverage: str,
    missing_tickers: tuple[str, ...],
    stale_tickers: tuple[str, ...],
) -> None:
    st.markdown(
        quality_summary_html(
            quality=quality,
            coverage=coverage,
            missing_tickers=missing_tickers,
            stale_tickers=stale_tickers,
        ),
        unsafe_allow_html=True,
    )


def render_workflow_steps(current_step: str) -> None:
    st.markdown(workflow_steps_html(current_step), unsafe_allow_html=True)


def render_document_policy() -> None:
    st.markdown(document_policy_html(), unsafe_allow_html=True)


def render_source_metadata(*, source: str, size_bytes: int, sha256_prefix: str) -> None:
    st.markdown(
        source_metadata_html(
            source=source,
            size_bytes=size_bytes,
            sha256_prefix=sha256_prefix,
        ),
        unsafe_allow_html=True,
    )


def render_confidence_grid(confidence: dict[str, float]) -> None:
    st.markdown(confidence_grid_html(confidence), unsafe_allow_html=True)
