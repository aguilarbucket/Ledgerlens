from __future__ import annotations

from decimal import Decimal

import streamlit as st

from ledgerlens.analytics.portfolio_dashboard import (
    PlatformAllocation,
    PortfolioHistoryPoint,
)
from ledgerlens.domain.models import PortfolioMetrics
from ledgerlens.ui.charts import (
    allocation_color_map,
    allocation_donut,
    portfolio_history_chart,
)
from ledgerlens.ui.components import (
    Tone,
    render_chart_legend,
    render_kpi_card,
    render_platform_allocation,
    render_position_card,
    render_section_header,
)
from ledgerlens.ui.formatters import clp, percent, semantic_movement, signed_percent
from ledgerlens.ui.view_models import allocation_records, history_records


def _movement_tone(value: Decimal | None) -> Tone:
    if value is None:
        return "neutral"
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "neutral"


def render_portfolio_dashboard(
    metrics: PortfolioMetrics,
    history: tuple[PortfolioHistoryPoint, ...],
    platforms: tuple[PlatformAllocation, ...],
) -> None:
    render_section_header(
        "Portfolio overview",
        "Confirmed synthetic purchases valued with the latest fixture prices.",
    )

    invested, current, pnl, coverage = st.columns(4)
    with invested:
        render_kpi_card(
            label="Invested value",
            value=clp(metrics.invested_value_clp),
            delta="Confirmed purchase cost",
        )
    with current:
        render_kpi_card(
            label="Current value",
            value=clp(metrics.current_value_clp),
            delta="Latest observable prices",
            tone="primary",
        )
    with pnl:
        movement = semantic_movement(metrics.unrealized_pnl_clp)
        render_kpi_card(
            label="Unrealized P/L",
            value=clp(metrics.unrealized_pnl_clp),
            delta=f"{signed_percent(metrics.unrealized_return_pct)} · {movement}",
            tone=_movement_tone(metrics.unrealized_pnl_clp),
        )
    with coverage:
        coverage_delta = (
            "All positions priced"
            if not metrics.missing_price_tickers
            else f"{len(metrics.missing_price_tickers)} ticker(s) missing"
        )
        render_kpi_card(
            label="Price coverage",
            value=percent(metrics.price_coverage_pct),
            delta=coverage_delta,
            tone="positive" if not metrics.missing_price_tickers else "neutral",
        )

    st.write("")
    allocation_column, history_column = st.columns([0.82, 1.48])
    with allocation_column:
        with st.container(border=True):
            render_section_header(
                "Allocation",
                "Current priced value by ticker.",
            )
            allocation = allocation_records(metrics)
            if allocation:
                st.altair_chart(allocation_donut(allocation), width="stretch", theme=None)
                colors = allocation_color_map(allocation)
                render_chart_legend(list(colors.items()))
            else:
                st.info("Allocation is unavailable until at least one position has a price.")

    with history_column:
        with st.container(border=True):
            render_section_header(
                "Observable value",
                "Current value and confirmed invested value; cash flows are not market movement.",
            )
            observations = history_records(history)
            if observations:
                st.altair_chart(
                    portfolio_history_chart(observations), width="stretch", theme=None
                )
            else:
                st.info("Historical values are unavailable for the current price coverage.")

    st.write("")
    render_section_header(
        "Positions",
        "Compact view of every priced holding. Full precision remains available below.",
    )
    for start in range(0, len(metrics.positions), 3):
        row = st.columns(3)
        for column, position in zip(row, metrics.positions[start : start + 3], strict=False):
            with column:
                movement = semantic_movement(position.unrealized_pnl_clp)
                render_position_card(
                    company=position.company,
                    ticker=position.ticker,
                    quantity=f"{position.quantity:,.0f}".replace(",", "."),
                    average_price=clp(position.weighted_average_price_clp),
                    current_price=clp(position.current_price_clp),
                    current_value=clp(position.current_value_clp),
                    pnl=clp(position.unrealized_pnl_clp),
                    return_pct=signed_percent(position.unrealized_return_pct),
                    allocation=percent(position.allocation_pct),
                    movement=movement,
                    tone=_movement_tone(position.unrealized_pnl_clp),
                )

    st.write("")
    with st.container(border=True):
        render_section_header(
            "Platform distribution",
            "Invested value grouped by the platform recorded on each confirmed purchase.",
        )
        if platforms:
            for platform in platforms:
                render_platform_allocation(
                    platform=platform.platform,
                    invested_value=clp(platform.invested_value_clp),
                    allocation=percent(platform.allocation_pct),
                    bar_width=float(platform.allocation_pct),
                )
        else:
            st.info("No confirmed platform records are available.")

    with st.expander("View detailed position table"):
        st.dataframe(
            [
                {
                    "Company": position.company,
                    "Ticker": position.ticker,
                    "Quantity": float(position.quantity),
                    "Weighted average": clp(position.weighted_average_price_clp),
                    "Current price": clp(position.current_price_clp),
                    "Current value": clp(position.current_value_clp),
                    "Unrealized P/L": clp(position.unrealized_pnl_clp),
                    "Unrealized return": percent(position.unrealized_return_pct),
                    "Allocation": percent(position.allocation_pct),
                }
                for position in metrics.positions
            ],
            hide_index=True,
            width="stretch",
        )

    if metrics.missing_price_tickers:
        st.warning("Missing prices: " + ", ".join(metrics.missing_price_tickers))
