from datetime import UTC, date, datetime
from decimal import Decimal

from ledgerlens.analytics.portfolio_dashboard import build_portfolio_history
from ledgerlens.analytics.portfolio_intelligence import (
    TickerContribution,
    build_weekly_context,
)
from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.ui.view_models import (
    allocation_records,
    contribution_records,
    history_records,
    weekly_comparison_records,
)
from sample_data.demo_data import demo_price_history, demo_prices, demo_purchases


def test_allocation_records_follow_deterministic_metrics() -> None:
    metrics = calculate_portfolio_metrics(demo_purchases(), demo_prices())

    records = allocation_records(metrics)

    assert [record["ticker"] for record in records] == [
        "CORD-A.SN",
        "PACIF.SN",
        "AUST.SN",
    ]
    assert round(sum(record["allocation_pct"] for record in records), 2) == 100.0


def test_history_records_only_reshape_analytics_output() -> None:
    history = build_portfolio_history(demo_purchases(), demo_price_history())

    records = history_records(history)

    assert len(records) == len(history) * 2
    assert {record["series"] for record in records} == {
        "Current value",
        "Invested value",
    }
    assert records[-1]["date"] == "2026-07-18"


def test_contribution_records_name_direction_and_sort_by_amount() -> None:
    records = contribution_records(
        (
            TickerContribution("LOSS.SN", Decimal("-25")),
            TickerContribution("GAIN.SN", Decimal("50")),
        )
    )

    assert records[0]["direction"] == "Positive"
    assert records[-1]["direction"] == "Negative"
    assert records == sorted(records, key=lambda item: (-item["amount_clp"], item["ticker"]))


def test_weekly_comparison_records_keep_analytics_values() -> None:
    context = build_weekly_context(
        demo_purchases(),
        demo_price_history(),
        report_date=date(2026, 7, 18),
        as_of=datetime(2026, 7, 18, 21, tzinfo=UTC),
    )

    records = weekly_comparison_records(context)

    assert [record["period"] for record in records] == [
        "Current week",
        "Prior week",
        "Baseline average",
    ]
    assert records[0]["amount_clp"] == float(context.current_week_change_clp)
