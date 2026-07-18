from datetime import UTC, date, datetime
from decimal import Decimal

import pytest

from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.domain.models import MarketPrice, Purchase


def purchase(identifier: str, ticker: str, quantity: str, price: str) -> Purchase:
    return Purchase(
        id=identifier,
        company=ticker,
        ticker=ticker,
        quantity=Decimal(quantity),
        unit_price_clp=Decimal(price),
        purchase_date=date(2026, 7, 14),
        platform="Synthetic Broker",
    )


def market_price(ticker: str, price: str) -> MarketPrice:
    return MarketPrice(
        ticker=ticker,
        price_clp=Decimal(price),
        as_of=datetime(2026, 7, 18, tzinfo=UTC),
        source="fixture",
    )


def test_weighted_average_and_unrealized_pnl() -> None:
    purchases = [
        purchase("1", "DEMO.SN", "10", "100"),
        purchase("2", "DEMO.SN", "20", "130"),
    ]
    metrics = calculate_portfolio_metrics(
        purchases, {"DEMO.SN": market_price("DEMO.SN", "150")}
    )

    position = metrics.positions[0]
    assert position.quantity == Decimal("30")
    assert position.invested_value_clp == Decimal("3600")
    assert position.weighted_average_price_clp == Decimal("120")
    assert position.current_value_clp == Decimal("4500")
    assert position.unrealized_pnl_clp == Decimal("900")
    assert position.unrealized_return_pct == Decimal("25.00")


def test_missing_price_is_not_reported_as_zero_movement() -> None:
    metrics = calculate_portfolio_metrics([purchase("1", "MISS.SN", "5", "200")], {})

    assert metrics.current_value_clp is None
    assert metrics.unrealized_pnl_clp is None
    assert metrics.price_coverage_pct == Decimal("0.00")
    assert metrics.missing_price_tickers == ("MISS.SN",)


def test_partial_price_coverage_uses_invested_value() -> None:
    purchases = [
        purchase("1", "A.SN", "10", "100"),
        purchase("2", "B.SN", "10", "300"),
    ]
    metrics = calculate_portfolio_metrics(purchases, {"A.SN": market_price("A.SN", "110")})

    assert metrics.price_coverage_pct == Decimal("25.00")
    assert metrics.current_value_clp == Decimal("1100")
    assert metrics.unrealized_pnl_clp == Decimal("100")


def test_empty_portfolio_is_valid() -> None:
    metrics = calculate_portfolio_metrics([], {})

    assert metrics.positions == ()
    assert metrics.invested_value_clp == Decimal("0")
    assert metrics.price_coverage_pct == Decimal("100")
    assert metrics.current_value_clp is None


def test_rejects_non_positive_purchase() -> None:
    with pytest.raises(ValueError, match="positive"):
        calculate_portfolio_metrics([purchase("1", "BAD.SN", "0", "100")], {})

