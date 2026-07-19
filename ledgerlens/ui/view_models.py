from __future__ import annotations

from typing import TypedDict

from ledgerlens.analytics.portfolio_dashboard import PortfolioHistoryPoint
from ledgerlens.analytics.portfolio_intelligence import TickerContribution, WeeklyContext
from ledgerlens.domain.models import PortfolioMetrics


class AllocationRecord(TypedDict):
    ticker: str
    value_clp: float
    allocation_pct: float


class HistoryRecord(TypedDict):
    date: str
    series: str
    value_clp: float


class ContributionRecord(TypedDict):
    ticker: str
    amount_clp: float
    direction: str


class ComparisonRecord(TypedDict):
    period: str
    amount_clp: float


def allocation_records(metrics: PortfolioMetrics) -> list[AllocationRecord]:
    records = [
        AllocationRecord(
            ticker=position.ticker,
            value_clp=float(position.current_value_clp),
            allocation_pct=float(position.allocation_pct),
        )
        for position in metrics.positions
        if position.current_value_clp is not None and position.allocation_pct is not None
    ]
    return sorted(records, key=lambda record: (-record["value_clp"], record["ticker"]))


def history_records(history: tuple[PortfolioHistoryPoint, ...]) -> list[HistoryRecord]:
    records: list[HistoryRecord] = []
    for point in history:
        observation_date = point.observation_date.isoformat()
        records.extend(
            [
                HistoryRecord(
                    date=observation_date,
                    series="Current value",
                    value_clp=float(point.current_value_clp),
                ),
                HistoryRecord(
                    date=observation_date,
                    series="Invested value",
                    value_clp=float(point.invested_value_clp),
                ),
            ]
        )
    return records


def contribution_records(
    contributions: tuple[TickerContribution, ...],
) -> list[ContributionRecord]:
    records = [
        ContributionRecord(
            ticker=item.ticker,
            amount_clp=float(item.amount_clp),
            direction=(
                "Positive"
                if item.amount_clp > 0
                else "Negative"
                if item.amount_clp < 0
                else "Neutral"
            ),
        )
        for item in contributions
    ]
    return sorted(records, key=lambda record: (-record["amount_clp"], record["ticker"]))


def weekly_comparison_records(context: WeeklyContext) -> list[ComparisonRecord]:
    candidates = (
        ("Current week", context.current_week_change_clp),
        ("Prior week", context.previous_week_change_clp),
        ("Baseline average", context.baseline_average_change_clp),
    )
    return [
        ComparisonRecord(period=label, amount_clp=float(value))
        for label, value in candidates
        if value is not None
    ]
