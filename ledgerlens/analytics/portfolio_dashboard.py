from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.domain.models import MarketPrice, Purchase

ZERO = Decimal("0")
HUNDRED = Decimal("100")


@dataclass(frozen=True, slots=True)
class PortfolioHistoryPoint:
    observation_date: date
    invested_value_clp: Decimal
    current_value_clp: Decimal


@dataclass(frozen=True, slots=True)
class PlatformAllocation:
    platform: str
    invested_value_clp: Decimal
    allocation_pct: Decimal


def build_portfolio_history(
    purchases: list[Purchase],
    prices_by_date: dict[date, dict[str, MarketPrice]],
) -> tuple[PortfolioHistoryPoint, ...]:
    """Calculate historical portfolio values from purchases eligible on each price date."""
    points: list[PortfolioHistoryPoint] = []
    for observation_date in sorted(prices_by_date):
        eligible = [
            purchase for purchase in purchases if purchase.purchase_date <= observation_date
        ]
        if not eligible:
            continue
        metrics = calculate_portfolio_metrics(eligible, prices_by_date[observation_date])
        if metrics.current_value_clp is None:
            continue
        points.append(
            PortfolioHistoryPoint(
                observation_date=observation_date,
                invested_value_clp=metrics.invested_value_clp,
                current_value_clp=metrics.current_value_clp,
            )
        )
    return tuple(points)


def calculate_platform_allocations(
    purchases: list[Purchase],
) -> tuple[PlatformAllocation, ...]:
    """Aggregate invested value by platform using confirmed purchase records."""
    invested_by_platform: dict[str, Decimal] = defaultdict(lambda: ZERO)
    for purchase in purchases:
        platform = purchase.platform.strip() or "Unspecified"
        invested_by_platform[platform] += purchase.quantity * purchase.unit_price_clp

    total = sum(invested_by_platform.values(), ZERO)
    if total == ZERO:
        return ()

    allocations = [
        PlatformAllocation(
            platform=platform,
            invested_value_clp=invested,
            allocation_pct=(invested / total * HUNDRED).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            ),
        )
        for platform, invested in invested_by_platform.items()
    ]
    return tuple(sorted(allocations, key=lambda item: (-item.invested_value_clp, item.platform)))

