from datetime import UTC, date, datetime
from decimal import Decimal

from ledgerlens.analytics.portfolio_dashboard import (
    build_portfolio_history,
    calculate_platform_allocations,
)
from ledgerlens.domain.models import MarketPrice, Purchase


def _purchase(
    identifier: str,
    ticker: str,
    quantity: str,
    price: str,
    purchase_date: date,
    platform: str,
) -> Purchase:
    return Purchase(
        id=identifier,
        company=ticker,
        ticker=ticker,
        quantity=Decimal(quantity),
        unit_price_clp=Decimal(price),
        purchase_date=purchase_date,
        platform=platform,
    )


def _price(ticker: str, price: str, observation_date: date) -> MarketPrice:
    return MarketPrice(
        ticker=ticker,
        price_clp=Decimal(price),
        as_of=datetime(
            observation_date.year,
            observation_date.month,
            observation_date.day,
            tzinfo=UTC,
        ),
        source="fixture",
    )


def test_portfolio_history_only_includes_purchases_owned_on_each_date() -> None:
    first_date = date(2026, 7, 10)
    second_date = date(2026, 7, 18)
    purchases = [
        _purchase("1", "A.SN", "10", "100", first_date, "Broker A"),
        _purchase("2", "B.SN", "5", "200", second_date, "Broker B"),
    ]
    prices = {
        first_date: {
            "A.SN": _price("A.SN", "110", first_date),
            "B.SN": _price("B.SN", "210", first_date),
        },
        second_date: {
            "A.SN": _price("A.SN", "120", second_date),
            "B.SN": _price("B.SN", "220", second_date),
        },
    }

    history = build_portfolio_history(purchases, prices)

    assert history[0].invested_value_clp == Decimal("1000")
    assert history[0].current_value_clp == Decimal("1100")
    assert history[1].invested_value_clp == Decimal("2000")
    assert history[1].current_value_clp == Decimal("2300")


def test_portfolio_history_omits_dates_before_first_purchase() -> None:
    price_date = date(2026, 7, 10)
    purchases = [
        _purchase("1", "A.SN", "10", "100", date(2026, 7, 11), "Broker A")
    ]

    assert build_portfolio_history(
        purchases, {price_date: {"A.SN": _price("A.SN", "110", price_date)}}
    ) == ()


def test_platform_allocations_use_invested_value() -> None:
    purchases = [
        _purchase("1", "A.SN", "10", "100", date(2026, 7, 10), "Broker A"),
        _purchase("2", "B.SN", "5", "200", date(2026, 7, 10), "Broker B"),
        _purchase("3", "C.SN", "1", "1000", date(2026, 7, 10), "Broker B"),
    ]

    allocations = calculate_platform_allocations(purchases)

    assert allocations[0].platform == "Broker B"
    assert allocations[0].invested_value_clp == Decimal("2000")
    assert allocations[0].allocation_pct == Decimal("66.67")
    assert allocations[1].allocation_pct == Decimal("33.33")


def test_platform_allocations_are_empty_without_purchases() -> None:
    assert calculate_platform_allocations([]) == ()

