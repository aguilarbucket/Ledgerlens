from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Purchase:
    id: str
    company: str
    ticker: str
    quantity: Decimal
    unit_price_clp: Decimal
    purchase_date: date
    platform: str
    currency: str = "CLP"
    document_reference: str | None = None
    document_sha256: str | None = None
    source: str = "manual"
    confirmed_at: datetime | None = None
    status: str = "active"
    voided_at: datetime | None = None
    void_reason: str | None = None


@dataclass(frozen=True, slots=True)
class MarketPrice:
    ticker: str
    price_clp: Decimal
    as_of: datetime
    source: str


@dataclass(frozen=True, slots=True)
class PositionMetrics:
    company: str
    ticker: str
    quantity: Decimal
    invested_value_clp: Decimal
    weighted_average_price_clp: Decimal
    current_price_clp: Decimal | None
    current_value_clp: Decimal | None
    unrealized_pnl_clp: Decimal | None
    unrealized_return_pct: Decimal | None
    allocation_pct: Decimal | None
    price_as_of: datetime | None


@dataclass(frozen=True, slots=True)
class PortfolioMetrics:
    positions: tuple[PositionMetrics, ...]
    invested_value_clp: Decimal
    priced_invested_value_clp: Decimal
    current_value_clp: Decimal | None
    unrealized_pnl_clp: Decimal | None
    unrealized_return_pct: Decimal | None
    price_coverage_pct: Decimal
    missing_price_tickers: tuple[str, ...]
