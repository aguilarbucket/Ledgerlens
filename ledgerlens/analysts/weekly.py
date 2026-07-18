from __future__ import annotations

import json
from dataclasses import asdict
from decimal import Decimal

from ledgerlens.analysts.guardrails import (
    AnalystReport,
    NarrativeProvider,
    validate_narrative,
)
from ledgerlens.analytics.portfolio_intelligence import TickerContribution, WeeklyContext

WEEKLY_INSTRUCTIONS = """
Write an executive, factual portfolio comparison in at most 120 words. Use only the supplied Python
metrics. Do not calculate, recommend, predict, invent causes, or present unrealized movement as a
realized gain. State when historical baseline or price context is insufficient.
""".strip()


def _clp(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:+,.0f} CLP"


def _pct(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:+.2f}%"


def _pct_level(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:.2f}%"


def _points(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:+.2f} percentage points"


def _contributor(item: TickerContribution | None) -> str:
    return "none observable" if item is None else f"{item.ticker} ({_clp(item.amount_clp)})"


def deterministic_weekly_narrative(context: WeeklyContext) -> str:
    baseline = (
        f"The {context.baseline_weeks}-week observable baseline averaged "
        f"{_clp(context.baseline_average_change_clp)}"
        if context.baseline_average_change_clp is not None
        else "Historical baseline is insufficient"
    )
    text = (
        f"Weekly observable movement was {_clp(context.current_week_change_clp)} "
        f"({_pct(context.current_week_change_pct)}), a "
        f"{_clp(context.difference_vs_previous_week_clp)} "
        f"difference from the prior week. {baseline}. Top positive contributor: "
        f"{_contributor(context.top_positive)}; top negative contributor: "
        f"{_contributor(context.top_negative)}. Concentration changed "
        f"{_points(context.concentration_change_pct_points)} and allocation shift was "
        f"{_points(context.distribution_change_pct_points)}. "
        f"{len(context.positions_added)} position(s) "
        f"were added; {context.missing_invoices} invoice(s) are missing. Price coverage is "
        f"{_pct_level(context.price_coverage_pct)}. Context quality: {context.context_quality}."
    )
    validate_narrative(text, max_words=120)
    return text


def _json_default(value):
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    raise TypeError


def build_weekly_report(
    context: WeeklyContext, narrator: NarrativeProvider | None = None
) -> AnalystReport:
    fallback = deterministic_weekly_narrative(context)
    if narrator is None:
        return AnalystReport(fallback, "deterministic_offline")
    try:
        generated = narrator.generate(
            instructions=WEEKLY_INSTRUCTIONS,
            context=json.dumps(asdict(context), default=_json_default, sort_keys=True),
            max_output_tokens=220,
        )
        validate_narrative(generated, max_words=120)
        return AnalystReport(generated, "openai_responses_api")
    except Exception:
        return AnalystReport(
            fallback,
            "deterministic_fallback",
            "OpenAI narrative was unavailable or failed guardrails; deterministic text is shown.",
        )
