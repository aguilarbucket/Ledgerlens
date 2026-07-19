import pytest

from ledgerlens.ui.components import app_header_html, kpi_card_html, notice_html
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
