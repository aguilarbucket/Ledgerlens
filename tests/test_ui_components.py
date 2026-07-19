from decimal import Decimal

import pytest

from ledgerlens.ui.components import (
    app_header_html,
    chart_legend_html,
    confidence_grid_html,
    document_policy_html,
    kpi_card_html,
    notice_html,
    platform_allocation_html,
    position_card_html,
    quality_summary_html,
    source_metadata_html,
    workflow_steps_html,
)
from ledgerlens.ui.formatters import (
    clp,
    percentage_points,
    semantic_movement,
    signed_percent,
)
from ledgerlens.ui.theme import COLORS, stylesheet


def test_fintech_palette_keeps_positive_color_semantic() -> None:
    assert COLORS["primary"] == "#4F8CFF"
    assert COLORS["positive"] == "#22C55E"
    assert COLORS["primary"] != COLORS["positive"]
    assert COLORS["background"] == "#08111F"
    assert COLORS["lavender"] == "#9B87F5"


def test_stylesheet_is_offline_and_responsive() -> None:
    css = stylesheet()

    assert "https://" not in css
    assert "@media (max-width: 768px)" in css
    assert "@media (prefers-reduced-motion: reduce)" in css
    assert "--ll-primary: #4F8CFF" in css


def test_component_content_is_html_escaped() -> None:
    html = app_header_html(subtitle='<script>alert("x")</script>', badge="Demo & safe")
    notice = notice_html("Synthetic <only>")

    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "Demo &amp; safe" in html
    assert "Synthetic &lt;only&gt;" in notice


def test_app_header_can_render_an_accessible_brand_lockup() -> None:
    html = app_header_html(
        subtitle="Verified portfolio",
        logo_data_uri="data:image/png;base64,c2FmZQ==",
    )

    assert 'class="ll-brand-lockup"' in html
    assert 'alt="LedgerLens"' in html
    assert "data:image/png;base64,c2FmZQ==" in html
    assert 'class="ll-brand-mark"' not in html


def test_kpi_card_exposes_text_and_non_color_tone() -> None:
    html = kpi_card_html(
        label="Unrealized P/L",
        value="$12.000 CLP",
        delta="+3.20% positive",
        tone="positive",
    )

    assert 'data-tone="positive"' in html
    assert "+3.20% positive" in html


def test_kpi_card_rejects_unknown_tone() -> None:
    with pytest.raises(ValueError, match="Unsupported KPI tone"):
        kpi_card_html(label="Value", value="1", tone="warning")  # type: ignore[arg-type]


def test_position_card_escapes_content_and_names_movement() -> None:
    html = position_card_html(
        company="Demo <script>",
        ticker="SAFE.SN",
        quantity="10",
        average_price="$100 CLP",
        current_price="$110 CLP",
        current_value="$1.100 CLP",
        pnl="$100 CLP",
        return_pct="+10.00%",
        allocation="25.00%",
        movement="Positive",
        tone="positive",
    )

    assert "<script>" not in html
    assert "Demo &lt;script&gt;" in html
    assert "+10.00% · Positive" in html
    assert 'aria-label="SAFE.SN position"' in html


def test_platform_bar_width_is_clamped() -> None:
    html = platform_allocation_html(
        platform="Demo Broker",
        invested_value="$1.000 CLP",
        allocation="120.00%",
        bar_width=120,
    )

    assert "width: 100.00%" in html


def test_financial_formatters_make_direction_explicit() -> None:
    assert clp(Decimal("10775")) == "$10.775 CLP"
    assert clp(Decimal("-2625")) == "-$2.625 CLP"
    assert signed_percent(Decimal("3.25")) == "+3.25%"
    assert semantic_movement(Decimal("-1")) == "Negative"
    assert percentage_points(Decimal("24.1")) == "+24.10 pp"


def test_chart_legend_escapes_labels() -> None:
    html = chart_legend_html([("SAFE<script>", "#4F8CFF")])

    assert "SAFE&lt;script&gt;" in html
    assert "SAFE<script>" not in html


def test_quality_summary_names_status_and_escapes_tickers() -> None:
    html = quality_summary_html(
        quality="partial",
        coverage="90.00%",
        missing_tickers=("MISS<script>",),
        stale_tickers=("OLD.SN",),
    )

    assert 'data-quality="partial"' in html
    assert "Partial context" in html
    assert "MISS&lt;script&gt;" in html


def test_quality_summary_rejects_unknown_status() -> None:
    with pytest.raises(ValueError, match="Unsupported context quality"):
        quality_summary_html(
            quality="unknown",
            coverage="0%",
            missing_tickers=(),
            stale_tickers=(),
        )


def test_workflow_steps_expose_completed_active_and_pending_states() -> None:
    html = workflow_steps_html("review")

    assert html.count('data-state="completed"') == 2
    assert html.count('data-state="active"') == 1
    assert html.count('data-state="pending"') == 1
    assert "Invoice import progress" in html


def test_workflow_steps_reject_unknown_stage() -> None:
    with pytest.raises(ValueError, match="Unsupported workflow step"):
        workflow_steps_html("saved")


def test_source_metadata_labels_ai_and_escapes_hash() -> None:
    html = source_metadata_html(
        source="openai_responses_api",
        size_bytes=2048,
        sha256_prefix="safe<script>",
    )

    assert 'data-source="ai"' in html
    assert "OpenAI extraction" in html
    assert "safe&lt;script&gt;" in html


def test_confidence_grid_clamps_visual_width() -> None:
    html = confidence_grid_html({"unit_price": 1.2, "ticker": -0.1})

    assert "Unit Price" in html
    assert "width: 100.00%" in html
    assert "width: 0.00%" in html
    assert "Private by design" in document_policy_html()
