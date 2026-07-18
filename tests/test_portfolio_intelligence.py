from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from ledgerlens.analytics.portfolio_intelligence import (
    build_daily_context,
    build_weekly_context,
)
from ledgerlens.domain.models import MarketPrice
from sample_data.demo_data import demo_price_history, demo_purchases

REPORT_DATE = date(2026, 7, 18)
AS_OF = datetime(2026, 7, 18, 21, 0, tzinfo=UTC)


def test_daily_context_uses_python_contributions_and_quality() -> None:
    context = build_daily_context(
        demo_purchases(), demo_price_history(), report_date=REPORT_DATE, as_of=AS_OF
    )

    assert context.current_value_clp == Decimal("366775")
    assert context.daily_change_clp == Decimal("2775")
    assert context.daily_change_pct == Decimal("0.76")
    assert context.unrealized_pnl_clp == Decimal("10775")
    assert context.top_positive.ticker == "CORD-A.SN"
    assert context.top_negative is None
    assert context.top_three_concentration_pct == Decimal("100.00")
    assert context.price_coverage_pct == Decimal("100.00")
    assert context.context_quality == "good"


def test_daily_context_reports_missing_and_stale_prices() -> None:
    history = demo_price_history()
    current = history[REPORT_DATE].copy()
    current.pop("PACIF.SN")
    aust = current["AUST.SN"]
    current["AUST.SN"] = MarketPrice(
        aust.ticker,
        aust.price_clp,
        AS_OF - timedelta(hours=72),
        aust.source,
    )
    history[REPORT_DATE] = current

    context = build_daily_context(demo_purchases(), history, report_date=REPORT_DATE, as_of=AS_OF)

    assert context.missing_price_tickers == ("PACIF.SN",)
    assert context.stale_price_tickers == ("AUST.SN",)
    assert context.daily_change_clp == Decimal("2400")
    assert context.context_quality == "insufficient"


def test_weekly_context_compares_prior_week_and_baseline() -> None:
    context = build_weekly_context(
        demo_purchases(), demo_price_history(), report_date=REPORT_DATE, as_of=AS_OF
    )

    assert context.current_week_change_clp == Decimal("2875")
    assert context.current_week_change_pct == Decimal("1.04")
    assert context.previous_week_change_clp == Decimal("875")
    assert context.difference_vs_previous_week_clp == Decimal("2000")
    assert context.baseline_weeks == 7
    assert context.baseline_average_change_clp.quantize(Decimal("0.01")) == Decimal("935.71")
    assert context.top_positive.ticker == "CORD-A.SN"
    assert context.top_negative.ticker == "PACIF.SN"
    assert context.concentration_change_pct_points == Decimal("0.00")
    assert context.distribution_change_pct_points == Decimal("24.10")
    assert context.best_day.movement_date == REPORT_DATE
    assert context.best_day.amount_clp == Decimal("2775")
    assert context.worst_day.movement_date == date(2026, 7, 16)
    assert context.worst_day.amount_clp == Decimal("-2525")
    assert context.positions_added == ("AUST.SN",)
    assert context.missing_invoices == 0
    assert context.context_quality == "good"
