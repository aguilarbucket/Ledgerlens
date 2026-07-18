from __future__ import annotations

import argparse
import logging
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from ledgerlens.ai.invoice_extractor import OpenAIInvoiceExtractor
from ledgerlens.ai.openai_client import OpenAIResponsesClient
from ledgerlens.analysts.daily import build_daily_report
from ledgerlens.analysts.narrator import OpenAINarrativeProvider
from ledgerlens.analysts.weekly import build_weekly_report
from ledgerlens.analytics.portfolio_intelligence import (
    build_daily_context,
    build_weekly_context,
)
from ledgerlens.invoices.pdf_validation import validate_pdf
from sample_data.demo_data import demo_price_history, demo_purchases

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYNTHETIC_PDF = PROJECT_ROOT / "output" / "pdf" / "ledgerlens_synthetic_invoice.pdf"
REPORT_DATE = date(2026, 7, 18)
AS_OF = datetime(2026, 7, 18, 21, 0, tzinfo=UTC)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run exactly three controlled OpenAI checks against synthetic data."
    )
    parser.add_argument(
        "--confirm-live",
        action="store_true",
        help="Acknowledge that this command makes three billable API requests.",
    )
    return parser.parse_args()


def _invoice_matches_expected(extraction) -> bool:
    return (
        extraction.ticker == "CORD-A.SN"
        and extraction.quantity == 150
        and extraction.unit_price == 920
        and extraction.purchase_date == REPORT_DATE
        and extraction.currency == "CLP"
        and extraction.document_reference == "SYNTH-BW-2026-005"
    )


def main() -> int:
    args = _parse_args()
    if not args.confirm_live:
        print("ABORTED: add --confirm-live to authorize exactly three API requests.")
        return 2

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    client = OpenAIResponsesClient(timeout_seconds=90, max_retries=0)
    print(f"MODEL={client.model}")
    print("MAX_API_REQUESTS=3")

    content = SYNTHETIC_PDF.read_bytes()
    pdf = validate_pdf(
        filename=SYNTHETIC_PDF.name,
        mime_type="application/pdf",
        content=content,
    )
    extraction = OpenAIInvoiceExtractor(client).extract(pdf)
    invoice_ok = _invoice_matches_expected(extraction)
    print(f"INVOICE_STRUCTURED_EXTRACTION={'PASS' if invoice_ok else 'FAIL'}")

    purchases = demo_purchases()
    history = demo_price_history()
    narrator = OpenAINarrativeProvider(client)
    daily = build_daily_context(purchases, history, report_date=REPORT_DATE, as_of=AS_OF)
    weekly = build_weekly_context(purchases, history, report_date=REPORT_DATE, as_of=AS_OF)
    daily_report = build_daily_report(daily, narrator)
    weekly_report = build_weekly_report(weekly, narrator)
    daily_ok = daily_report.source == "openai_responses_api"
    weekly_ok = weekly_report.source == "openai_responses_api"
    print(f"DAILY_NARRATIVE_GUARDRAILS={'PASS' if daily_ok else 'FAIL'}")
    print(f"WEEKLY_NARRATIVE_GUARDRAILS={'PASS' if weekly_ok else 'FAIL'}")

    all_ok = invoice_ok and daily_ok and weekly_ok
    print(f"LIVE_VALIDATION={'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
