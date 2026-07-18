from datetime import UTC, date, datetime

from ledgerlens.analysts.daily import build_daily_report
from ledgerlens.analysts.weekly import build_weekly_report
from ledgerlens.analytics.portfolio_intelligence import (
    build_daily_context,
    build_weekly_context,
)
from sample_data.demo_data import demo_price_history, demo_purchases

REPORT_DATE = date(2026, 7, 18)
AS_OF = datetime(2026, 7, 18, 21, 0, tzinfo=UTC)


class StaticNarrator:
    def __init__(self, text: str) -> None:
        self.text = text

    def generate(self, *, instructions: str, context: str, max_output_tokens: int) -> str:
        assert instructions
        assert context
        assert max_output_tokens > 0
        return self.text


def contexts():
    purchases = demo_purchases()
    history = demo_price_history()
    return (
        build_daily_context(purchases, history, report_date=REPORT_DATE, as_of=AS_OF),
        build_weekly_context(purchases, history, report_date=REPORT_DATE, as_of=AS_OF),
    )


def test_offline_reports_are_factual_and_within_word_limits() -> None:
    daily, weekly = contexts()
    daily_report = build_daily_report(daily)
    weekly_report = build_weekly_report(weekly)

    assert daily_report.source == "deterministic_offline"
    assert weekly_report.source == "deterministic_offline"
    assert len(daily_report.text.split()) <= 100
    assert len(weekly_report.text.split()) <= 120
    assert "unrealized" in daily_report.text.lower()


def test_guardrail_failure_uses_explicit_deterministic_fallback() -> None:
    daily, _ = contexts()
    report = build_daily_report(daily, StaticNarrator("You should buy and hold this ticker."))

    assert report.source == "deterministic_fallback"
    assert report.warning is not None
    assert "should buy" not in report.text.lower()


def test_valid_generated_narrative_is_accepted() -> None:
    _, weekly = contexts()
    text = "Weekly observable movement was positive. Price coverage was complete."
    report = build_weekly_report(weekly, StaticNarrator(text))

    assert report.source == "openai_responses_api"
    assert report.text == text
    assert report.warning is None
