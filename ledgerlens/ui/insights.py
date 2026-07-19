from __future__ import annotations

from decimal import Decimal

import streamlit as st

from ledgerlens.analysts.guardrails import AnalystReport
from ledgerlens.analytics.portfolio_intelligence import (
    DailyContext,
    TickerContribution,
    WeeklyContext,
)
from ledgerlens.ui.charts import contribution_chart, weekly_comparison_chart
from ledgerlens.ui.components import (
    Tone,
    render_kpi_card,
    render_quality_summary,
    render_section_header,
)
from ledgerlens.ui.formatters import (
    clp,
    percent,
    percentage_points,
    semantic_movement,
    signed_clp,
    signed_percent,
)
from ledgerlens.ui.view_models import contribution_records, weekly_comparison_records


def _movement_tone(value: Decimal | None) -> Tone:
    if value is None or value == 0:
        return "neutral"
    return "positive" if value > 0 else "negative"


def _contributor_value(item: TickerContribution | None) -> str:
    return "Not available" if item is None else signed_clp(item.amount_clp)


def _contributor_label(item: TickerContribution | None) -> str:
    return "No observable contributor" if item is None else item.ticker


def _source_label(source: str) -> str:
    return {
        "deterministic_offline": "Deterministic offline",
        "deterministic_fallback": "Deterministic fallback",
        "openai_responses_api": "OpenAI Responses API",
    }.get(source, source.replace("_", " ").title())


def _render_narrative(report: AnalystReport) -> None:
    with st.container(border=True):
        render_section_header(
            "Analyst narrative",
            "Descriptive text generated only from the deterministic context shown here.",
        )
        st.markdown(report.text)
        st.caption(f"Narrative source: {_source_label(report.source)}")
        if report.warning:
            st.warning(report.warning)


def _render_contribution_table(
    records: list[dict[str, object]], *, label: str
) -> None:
    with st.expander(f"View {label.lower()} contribution data"):
        st.dataframe(records, hide_index=True, width="stretch")


def _contribution_table_records(
    contributions: tuple[TickerContribution, ...],
) -> list[dict[str, object]]:
    ordered = sorted(contributions, key=lambda item: (-item.amount_clp, item.ticker))
    return [
        {
            "Ticker": item.ticker,
            "Contribution": signed_clp(item.amount_clp),
            "Direction": semantic_movement(item.amount_clp),
        }
        for item in ordered
    ]


def render_daily_lens(context: DailyContext, report: AnalystReport) -> None:
    render_section_header(
        "Daily Lens",
        f"Observable comparison for {context.report_date.isoformat()}; cash flows are excluded.",
    )

    value, movement, pnl, coverage = st.columns(4)
    with value:
        render_kpi_card(
            label="Portfolio value",
            value=clp(context.current_value_clp),
            delta="Latest observable snapshot",
            tone="primary",
        )
    with movement:
        render_kpi_card(
            label="Daily movement",
            value=signed_clp(context.daily_change_clp),
            delta=(
                f"{signed_percent(context.daily_change_pct)} · "
                f"{semantic_movement(context.daily_change_clp)}"
            ),
            tone=_movement_tone(context.daily_change_clp),
        )
    with pnl:
        render_kpi_card(
            label="Unrealized P/L",
            value=clp(context.unrealized_pnl_clp),
            delta=semantic_movement(context.unrealized_pnl_clp),
            tone=_movement_tone(context.unrealized_pnl_clp),
        )
    with coverage:
        render_kpi_card(
            label="Price coverage",
            value=percent(context.price_coverage_pct),
            delta=f"Context quality: {context.context_quality}",
            tone="positive" if context.context_quality == "good" else "neutral",
        )

    st.write("")
    chart_column, narrative_column = st.columns([1.15, 0.85])
    contribution_data = contribution_records(context.contributions)
    with chart_column:
        with st.container(border=True):
            render_section_header(
                "Daily contribution",
                "Each ticker's deterministic component of observable movement.",
            )
            if contribution_data:
                st.altair_chart(
                    contribution_chart(
                        contribution_data,
                        description="Daily observable contribution by ticker",
                    ),
                    width="stretch",
                    theme=None,
                )
            else:
                st.info("Comparable prices are insufficient for daily contributions.")
    with narrative_column:
        _render_narrative(report)
        st.write("")
        render_quality_summary(
            quality=context.context_quality,
            coverage=percent(context.price_coverage_pct),
            missing_tickers=context.missing_price_tickers,
            stale_tickers=context.stale_price_tickers,
        )

    st.write("")
    render_section_header("Daily observations")
    positive, negative, concentration, purchases = st.columns(4)
    with positive:
        render_kpi_card(
            label="Top positive",
            value=_contributor_label(context.top_positive),
            delta=_contributor_value(context.top_positive),
            tone="positive" if context.top_positive else "neutral",
        )
    with negative:
        render_kpi_card(
            label="Top negative",
            value=_contributor_label(context.top_negative),
            delta=_contributor_value(context.top_negative),
            tone="negative" if context.top_negative else "neutral",
        )
    with concentration:
        render_kpi_card(
            label="Top-three concentration",
            value=percent(context.top_three_concentration_pct),
            delta="Current priced portfolio",
        )
    with purchases:
        render_kpi_card(
            label="Records today",
            value=str(context.purchases_today),
            delta=f"{context.invoices_today} invoice(s)",
            tone="primary",
        )

    _render_contribution_table(
        _contribution_table_records(context.contributions),
        label="Daily",
    )


def render_weekly_lens(context: WeeklyContext, report: AnalystReport) -> None:
    render_section_header(
        "Weekly Lens",
        f"Week beginning {context.week_start.isoformat()} compared with prior observations.",
    )

    movement, difference, baseline, coverage = st.columns(4)
    with movement:
        render_kpi_card(
            label="Weekly movement",
            value=signed_clp(context.current_week_change_clp),
            delta=(
                f"{signed_percent(context.current_week_change_pct)} · "
                f"{semantic_movement(context.current_week_change_clp)}"
            ),
            tone=_movement_tone(context.current_week_change_clp),
        )
    with difference:
        render_kpi_card(
            label="Vs prior week",
            value=signed_clp(context.difference_vs_previous_week_clp),
            delta=semantic_movement(context.difference_vs_previous_week_clp),
            tone=_movement_tone(context.difference_vs_previous_week_clp),
        )
    with baseline:
        render_kpi_card(
            label="Baseline average",
            value=signed_clp(context.baseline_average_change_clp),
            delta=f"{context.baseline_weeks} observed week(s)",
            tone="primary",
        )
    with coverage:
        render_kpi_card(
            label="Price coverage",
            value=percent(context.price_coverage_pct),
            delta=f"Context quality: {context.context_quality}",
            tone="positive" if context.context_quality == "good" else "neutral",
        )

    st.write("")
    comparison_column, narrative_column = st.columns([1.05, 0.95])
    comparison_data = weekly_comparison_records(context)
    with comparison_column:
        with st.container(border=True):
            render_section_header(
                "Weekly comparison",
                "Current observable movement, prior week, and historical baseline.",
            )
            if comparison_data:
                st.altair_chart(
                    weekly_comparison_chart(comparison_data), width="stretch", theme=None
                )
            else:
                st.info("A weekly comparison is not available for this context.")
    with narrative_column:
        _render_narrative(report)
        st.write("")
        render_quality_summary(
            quality=context.context_quality,
            coverage=percent(context.price_coverage_pct),
            missing_tickers=context.missing_price_tickers,
            stale_tickers=context.stale_price_tickers,
        )

    st.write("")
    contribution_data = contribution_records(context.contributions)
    with st.container(border=True):
        render_section_header(
            "Weekly contribution",
            "Ticker contributions to the current observable weekly movement.",
        )
        if contribution_data:
            st.altair_chart(
                contribution_chart(
                    contribution_data,
                    description="Weekly observable contribution by ticker",
                ),
                width="stretch",
                theme=None,
            )
        else:
            st.info("Comparable prices are insufficient for weekly contributions.")

    st.write("")
    render_section_header("Weekly observations")
    positive, negative, shift, positions = st.columns(4)
    with positive:
        render_kpi_card(
            label="Top positive",
            value=_contributor_label(context.top_positive),
            delta=_contributor_value(context.top_positive),
            tone="positive" if context.top_positive else "neutral",
        )
    with negative:
        render_kpi_card(
            label="Top negative",
            value=_contributor_label(context.top_negative),
            delta=_contributor_value(context.top_negative),
            tone="negative" if context.top_negative else "neutral",
        )
    with shift:
        render_kpi_card(
            label="Allocation shift",
            value=percentage_points(context.distribution_change_pct_points),
            delta="Percentage points",
        )
    with positions:
        render_kpi_card(
            label="Positions added",
            value=str(len(context.positions_added)),
            delta=", ".join(context.positions_added) or "None",
            tone="primary",
        )

    details_left, details_right = st.columns(2)
    with details_left:
        with st.container(border=True):
            render_section_header("Record integrity")
            st.write(f"Missing invoices: **{context.missing_invoices}**")
            st.write(f"Incomplete records: **{context.incomplete_records}**")
            st.write(
                "Concentration change: "
                f"**{percentage_points(context.concentration_change_pct_points)}**"
            )
    with details_right:
        with st.container(border=True):
            render_section_header("Observable days")
            best = (
                f"{context.best_day.movement_date}: {signed_clp(context.best_day.amount_clp)}"
                if context.best_day
                else "Not available"
            )
            worst = (
                f"{context.worst_day.movement_date}: {signed_clp(context.worst_day.amount_clp)}"
                if context.worst_day
                else "Not available"
            )
            st.write(f"Best day: **{best}**")
            st.write(f"Worst day: **{worst}**")

    _render_contribution_table(
        _contribution_table_records(context.contributions),
        label="Weekly",
    )


def render_intelligence_dashboard(
    daily_context: DailyContext,
    daily_report: AnalystReport,
    weekly_context: WeeklyContext,
    weekly_report: AnalystReport,
) -> None:
    daily_tab, weekly_tab = st.tabs(["Daily Lens", "Weekly Lens"])
    with daily_tab:
        render_daily_lens(daily_context, daily_report)
    with weekly_tab:
        render_weekly_lens(weekly_context, weekly_report)
