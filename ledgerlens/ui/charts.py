from __future__ import annotations

import altair as alt

from ledgerlens.ui.theme import COLORS
from ledgerlens.ui.view_models import (
    AllocationRecord,
    ComparisonRecord,
    ContributionRecord,
    HistoryRecord,
)

CHART_PALETTE = [
    COLORS["primary"],
    COLORS["secondary"],
    "#A78BFA",
    COLORS["warning"],
    "#38BDF8",
    "#FB7185",
]


def allocation_color_map(records: list[AllocationRecord]) -> dict[str, str]:
    tickers = sorted({record["ticker"] for record in records})
    return {
        ticker: CHART_PALETTE[index % len(CHART_PALETTE)]
        for index, ticker in enumerate(tickers)
    }


def _chart_base(chart: alt.Chart | alt.LayerChart) -> alt.Chart | alt.LayerChart:
    return (
        chart.configure(background="transparent")
        .configure_view(strokeOpacity=0)
        .configure_axis(
            gridColor="#263653",
            gridOpacity=0.42,
            domain=False,
            labelColor=COLORS["text_muted"],
            labelFontSize=11,
            tickColor="#263653",
            titleColor=COLORS["text_muted"],
        )
        .configure_legend(
            labelColor=COLORS["text_muted"],
            labelFontSize=11,
            symbolStrokeWidth=3,
            title=None,
        )
    )


def allocation_donut(records: list[AllocationRecord]) -> alt.Chart:
    colors = allocation_color_map(records)
    chart = (
        alt.Chart(alt.Data(values=records))
        .mark_arc(innerRadius=58, outerRadius=92, cornerRadius=5, padAngle=0.02)
        .encode(
            theta=alt.Theta("value_clp:Q", stack=True),
            color=alt.Color(
                "ticker:N",
                scale=alt.Scale(domain=list(colors), range=list(colors.values())),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("ticker:N", title="Ticker"),
                alt.Tooltip("value_clp:Q", title="Current value", format=",.0f"),
                alt.Tooltip("allocation_pct:Q", title="Allocation", format=".2f"),
            ],
        )
        .properties(height=260, description="Current portfolio allocation by ticker")
    )
    return _chart_base(chart)


def portfolio_history_chart(records: list[HistoryRecord]) -> alt.LayerChart:
    base = alt.Chart(alt.Data(values=records)).encode(
        x=alt.X(
            "date:T",
            title=None,
            axis=alt.Axis(format="%d %b", labelAngle=0, tickCount=6),
        ),
        y=alt.Y(
            "value_clp:Q",
            title="CLP",
            scale=alt.Scale(zero=False),
            axis=alt.Axis(format="~s", tickCount=5),
        ),
    )
    current_area = (
        base.transform_filter(alt.datum.series == "Current value")
        .mark_area(color=COLORS["primary"], opacity=0.1)
    )
    lines = base.mark_line(point=alt.OverlayMarkDef(size=36), strokeWidth=2.5).encode(
        color=alt.Color(
            "series:N",
            scale=alt.Scale(
                domain=["Current value", "Invested value"],
                range=[COLORS["primary"], COLORS["secondary"]],
            ),
            legend=alt.Legend(orient="bottom"),
        ),
        tooltip=[
            alt.Tooltip("date:T", title="Date", format="%Y-%m-%d"),
            alt.Tooltip("series:N", title="Series"),
            alt.Tooltip("value_clp:Q", title="Value", format=",.0f"),
        ],
    )
    return _chart_base(
        (current_area + lines).properties(
            height=260,
            description="Observable current and invested portfolio value over time",
        )
    )


def contribution_chart(
    records: list[ContributionRecord], *, description: str
) -> alt.LayerChart:
    bars = (
        alt.Chart(alt.Data(values=records))
        .mark_bar(cornerRadius=5, size=22)
        .encode(
            x=alt.X(
                "amount_clp:Q",
                title="Contribution (CLP)",
                axis=alt.Axis(format="~s", tickCount=5),
            ),
            y=alt.Y(
                "ticker:N",
                title=None,
                sort=alt.SortField(field="amount_clp", order="descending"),
            ),
            color=alt.Color(
                "direction:N",
                scale=alt.Scale(
                    domain=["Positive", "Negative", "Neutral"],
                    range=[COLORS["positive"], COLORS["negative"], COLORS["text_muted"]],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("ticker:N", title="Ticker"),
                alt.Tooltip("amount_clp:Q", title="Contribution", format=",.0f"),
                alt.Tooltip("direction:N", title="Direction"),
            ],
        )
    )
    zero = (
        alt.Chart(alt.Data(values=[{"zero": 0}]))
        .mark_rule(color=COLORS["text_muted"], opacity=0.55)
        .encode(x="zero:Q")
    )
    return _chart_base(
        (bars + zero).properties(height=210, description=description)
    )


def weekly_comparison_chart(records: list[ComparisonRecord]) -> alt.Chart:
    chart = (
        alt.Chart(alt.Data(values=records))
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=48)
        .encode(
            x=alt.X("period:N", title=None, sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y(
                "amount_clp:Q",
                title="Observable movement (CLP)",
                axis=alt.Axis(format="~s", tickCount=5),
            ),
            color=alt.Color(
                "period:N",
                scale=alt.Scale(
                    domain=["Current week", "Prior week", "Baseline average"],
                    range=[COLORS["primary"], COLORS["secondary"], "#A78BFA"],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("period:N", title="Comparison"),
                alt.Tooltip("amount_clp:Q", title="Movement", format=",.0f"),
            ],
        )
        .properties(height=245, description="Weekly movement comparison")
    )
    return _chart_base(chart)
