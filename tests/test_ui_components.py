from decimal import Decimal

import pytest

from ledgerlens.ui.components import (
    app_header_html,
    chart_legend_html,
    kpi_card_html,
    notice_html,
    platform_allocation_html,
    position_card_html,
)
from ledgerlens.ui.formatters import clp, semantic_movement, signed_percent
from ledgerlens.ui.theme import COLORS, stylesheet


def test_fintech_palette_keeps_positive_color_semantic() -> None:
    assert COLORS["primary"] == "#4F8CFF"
    assert COLORS["positive"] == "#22C55E"
    assert COLORS["primary"] != COLORS["positive"]
    assert COLORS["background"] == "#08111F"


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


def test_chart_legend_escapes_labels() -> None:
    html = chart_legend_html([("SAFE<script>", "#4F8CFF")])

    assert "SAFE&lt;script&gt;" in html
    assert "SAFE<script>" not in html
