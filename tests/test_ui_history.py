from datetime import date

from ledgerlens.ui.history import filter_purchases, source_label
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


def test_source_labels_are_judge_facing() -> None:
    assert source_label("synthetic") == "Synthetic seed"
    assert source_label("openai_responses_api") == "OpenAI extraction"
