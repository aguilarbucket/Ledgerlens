from __future__ import annotations

from typing import TypedDict

from ledgerlens.analytics.portfolio_dashboard import PortfolioHistoryPoint
from ledgerlens.domain.models import PortfolioMetrics


class AllocationRecord(TypedDict):
    ticker: str
    value_clp: float
    allocation_pct: float


class HistoryRecord(TypedDict):
    date: str
    series: str
    value_clp: float


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

