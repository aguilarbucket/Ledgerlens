from dataclasses import replace
from datetime import date

from ledgerlens.ui.history import (
    filter_purchases,
    source_label,
    status_label,
    void_target_ids,
)
from sample_data.demo_data import demo_purchases


def test_history_filters_are_read_only_and_composable() -> None:
    purchases = demo_purchases()

    filtered = filter_purchases(
        purchases,
        tickers=["CORD-A.SN"],
        platforms=["Corredora Demo"],
        sources=["synthetic"],
        start_date=date(2026, 6, 1),
        end_date=date(2026, 6, 30),
    )

    assert [purchase.id for purchase in filtered] == ["demo-002"]
    assert len(purchases) == 4


def test_empty_filter_selections_include_full_date_range() -> None:
    purchases = demo_purchases()

    filtered = filter_purchases(
        purchases,
        tickers=[],
        platforms=[],
        sources=[],
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
    )

    assert filtered == purchases
    assert len({purchase.platform for purchase in purchases}) == 4


def test_source_labels_are_judge_facing() -> None:
    assert source_label("synthetic") == "Synthetic seed"
    assert source_label("openai_responses_api") == "OpenAI extraction"


def test_history_can_filter_active_and_voided_records() -> None:
    purchases = demo_purchases()
    purchases[0] = replace(
        purchases[0], status="voided", void_reason="Duplicate record"
    )

    filtered = filter_purchases(
        purchases,
        tickers=[],
        platforms=[],
        sources=[],
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
        statuses=["voided"],
    )

    assert [purchase.id for purchase in filtered] == ["demo-001"]
    assert status_label(filtered[0].status) == "Voided"


def test_void_scope_can_target_one_record_or_all_active_ticker_lots() -> None:
    purchases = demo_purchases()

    assert void_target_ids(
        purchases, "demo-001", all_ticker_records=False
    ) == ("demo-001",)
    assert void_target_ids(
        purchases, "demo-001", all_ticker_records=True
    ) == ("demo-001", "demo-002")

    purchases[1] = replace(purchases[1], status="voided")
    assert void_target_ids(
        purchases, "demo-001", all_ticker_records=True
    ) == ("demo-001",)
