from __future__ import annotations

from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal

from ledgerlens.domain.models import (
    MarketPrice,
    PortfolioMetrics,
    PositionMetrics,
    Purchase,
)

ZERO = Decimal("0")
HUNDRED = Decimal("100")


def _percent(numerator: Decimal, denominator: Decimal) -> Decimal | None:
    if denominator == ZERO:
        return None
    return (numerator / denominator * HUNDRED).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )


def calculate_portfolio_metrics(
    purchases: list[Purchase], prices: dict[str, MarketPrice]
) -> PortfolioMetrics:
    grouped: dict[tuple[str, str], list[Purchase]] = defaultdict(list)
    for purchase in purchases:
        if purchase.quantity <= ZERO or purchase.unit_price_clp <= ZERO:
            raise ValueError("Purchase quantity and unit price must be positive.")
        if purchase.currency != "CLP":
            raise ValueError("The current LedgerLens scope supports CLP purchases only.")
        grouped[(purchase.ticker, purchase.company)].append(purchase)

    raw_positions: list[dict[str, object]] = []
    total_invested = ZERO
    priced_invested = ZERO
    total_current = ZERO
    missing: list[str] = []

    for (ticker, company), lots in grouped.items():
        quantity = sum((lot.quantity for lot in lots), ZERO)
        invested = sum((lot.quantity * lot.unit_price_clp for lot in lots), ZERO)
        weighted_average = invested / quantity
        market_price = prices.get(ticker)
        current_value = market_price.price_clp * quantity if market_price else None
        pnl = current_value - invested if current_value is not None else None
        return_pct = _percent(pnl, invested) if pnl is not None else None

        total_invested += invested
        if current_value is None:
            missing.append(ticker)
        else:
            priced_invested += invested
            total_current += current_value

        raw_positions.append(
            {
                "company": company,
                "ticker": ticker,
                "quantity": quantity,
                "invested": invested,
                "weighted_average": weighted_average,
                "market_price": market_price,
                "current_value": current_value,
                "pnl": pnl,
                "return_pct": return_pct,
            }
        )

    positions: list[PositionMetrics] = []
    for item in raw_positions:
        current_value = item["current_value"]
        allocation = (
            _percent(current_value, total_current)
            if isinstance(current_value, Decimal) and total_current > ZERO
            else None
        )
        market_price = item["market_price"]
        positions.append(
            PositionMetrics(
                company=str(item["company"]),
                ticker=str(item["ticker"]),
                quantity=item["quantity"],
                invested_value_clp=item["invested"],
                weighted_average_price_clp=item["weighted_average"],
                current_price_clp=market_price.price_clp if market_price else None,
                current_value_clp=current_value,
                unrealized_pnl_clp=item["pnl"],
                unrealized_return_pct=item["return_pct"],
                allocation_pct=allocation,
                price_as_of=market_price.as_of if market_price else None,
            )
        )

    has_prices = any(position.current_value_clp is not None for position in positions)
    total_pnl = total_current - priced_invested if has_prices else None
    total_return = _percent(total_pnl, priced_invested) if total_pnl is not None else None
    coverage = _percent(priced_invested, total_invested) if total_invested else HUNDRED

    return PortfolioMetrics(
        positions=tuple(sorted(positions, key=lambda position: position.ticker)),
        invested_value_clp=total_invested,
        priced_invested_value_clp=priced_invested,
        current_value_clp=total_current if has_prices else None,
        unrealized_pnl_clp=total_pnl,
        unrealized_return_pct=total_return,
        price_coverage_pct=coverage or ZERO,
        missing_price_tickers=tuple(sorted(set(missing))),
    )
