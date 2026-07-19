from ledgerlens.analytics.portfolio_dashboard import build_portfolio_history
from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.ui.view_models import allocation_records, history_records
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
