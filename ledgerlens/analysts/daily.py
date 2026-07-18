from __future__ import annotations

import json
from dataclasses import asdict
from decimal import Decimal

from ledgerlens.analysts.guardrails import (
    AnalystReport,
    NarrativeProvider,
    validate_narrative,
)
from ledgerlens.analytics.portfolio_intelligence import DailyContext, TickerContribution

DAILY_INSTRUCTIONS = """
Write an executive, factual portfolio summary in at most 100 words. Use only the supplied Python
metrics. Do not calculate, recommend, predict, invent causes, or imply that unrealized P/L is a
realized gain. Distinguish missing prices from zero movement and state when context is insufficient.
""".strip()


def _clp(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:+,.0f} CLP"


def _clp_level(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:,.0f} CLP"


def _pct(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:+.2f}%"


def _pct_level(value: Decimal | None) -> str:
    return "unavailable" if value is None else f"{value:.2f}%"


def _contributor(item: TickerContribution | None) -> str:
    return "none observable" if item is None else f"{item.ticker} ({_clp(item.amount_clp)})"


def deterministic_daily_narrative(context: DailyContext) -> str:
    movement = (
        f"Observable market movement was {_clp(context.daily_change_clp)} "
        f"({_pct(context.daily_change_pct)})"
        if context.daily_change_clp is not None
        else "Daily movement is unavailable; comparable prices are insufficient"
    )
    text = (
        f"Portfolio value is {_clp_level(context.current_value_clp)}. {movement}. "
        f"Top positive contributor: {_contributor(context.top_positive)}; "
        f"top negative contributor: {_contributor(context.top_negative)}. "
        f"Unrealized P/L is {_clp(context.unrealized_pnl_clp)}. "
        f"Top-three concentration is {_pct_level(context.top_three_concentration_pct)}. "
        f"Price coverage is {_pct_level(context.price_coverage_pct)}. "
        f"{context.purchases_today} purchase "
        f"record(s) and {context.invoices_today} invoice(s) were added today. "
        f"Context quality: {context.context_quality}."
    )
    validate_narrative(text, max_words=100)
    return text


def _json_default(value):
    if isinstance(value, Decimal):
        return str(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    raise TypeError


def build_daily_report(
    context: DailyContext, narrator: NarrativeProvider | None = None
) -> AnalystReport:
    fallback = deterministic_daily_narrative(context)
    if narrator is None:
        return AnalystReport(fallback, "deterministic_offline")
    try:
        generated = narrator.generate(
            instructions=DAILY_INSTRUCTIONS,
            context=json.dumps(asdict(context), default=_json_default, sort_keys=True),
            max_output_tokens=180,
        )
        validate_narrative(generated, max_words=100)
        return AnalystReport(generated, "openai_responses_api")
    except Exception:
        return AnalystReport(
            fallback,
            "deterministic_fallback",
            "OpenAI narrative was unavailable or failed guardrails; deterministic text is shown.",
        )
