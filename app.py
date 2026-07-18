from __future__ import annotations

import os
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

import streamlit as st

from ledgerlens.ai.invoice_extractor import FixtureInvoiceExtractor, OpenAIInvoiceExtractor
from ledgerlens.ai.openai_client import OpenAIConfigurationError, OpenAIResponsesClient
from ledgerlens.analysts.daily import build_daily_report
from ledgerlens.analysts.narrator import OpenAINarrativeProvider
from ledgerlens.analysts.weekly import build_weekly_report
from ledgerlens.analytics.portfolio_intelligence import (
    build_daily_context,
    build_weekly_context,
)
from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.config import load_project_environment
from ledgerlens.data.portfolio_repository import SQLitePortfolioRepository
from ledgerlens.invoices.confirmation import confirm_extraction
from ledgerlens.invoices.models import InvoiceExtraction
from ledgerlens.invoices.pdf_validation import PDFValidationError, validate_pdf
from ledgerlens.market.market_data_provider import FixtureMarketDataProvider
from sample_data.demo_data import demo_price_history, demo_prices, demo_purchases

load_project_environment()


def clp(value: Decimal | None) -> str:
    if value is None:
        return "Not available"
    return f"${value:,.0f} CLP".replace(",", ".")


def percent(value: Decimal | None) -> str:
    return "Not available" if value is None else f"{value:.2f}%"


st.set_page_config(page_title="LedgerLens", page_icon="🔎", layout="wide")
st.title("LedgerLens")
st.caption("A verified portfolio ledger with deterministic analytics and synthetic demo data.")

demo_mode = os.getenv("LEDGERLENS_DEMO_MODE", "true").lower() in {"1", "true", "yes"}
if not demo_mode:
    st.error("Only synthetic demo mode is enabled in this first Build Week slice.")
    st.stop()

database_path = Path(os.getenv("LEDGERLENS_DATABASE_PATH", "runtime/ledgerlens.db"))
repository = SQLitePortfolioRepository(database_path)
repository.sync_synthetic_seed(demo_purchases())
purchases = repository.list_purchases()
provider = FixtureMarketDataProvider(demo_prices())
prices = provider.get_prices({purchase.ticker for purchase in purchases})
metrics = calculate_portfolio_metrics(purchases, prices)

st.info(
    "Demo mode: all purchases, companies, document references, and prices are synthetic. "
    "This is descriptive software, not financial advice."
)

portfolio_tab, import_tab, history_tab, insights_tab, about_tab = st.tabs(
    ["Portfolio", "Import purchase", "Purchase history", "AI Insights", "About"]
)

with portfolio_tab:
    first, second, third, fourth = st.columns(4)
    first.metric("Invested value", clp(metrics.invested_value_clp))
    second.metric("Current value", clp(metrics.current_value_clp))
    third.metric("Unrealized P/L", clp(metrics.unrealized_pnl_clp))
    fourth.metric("Price coverage", percent(metrics.price_coverage_pct))

    st.subheader("Positions")
    st.dataframe(
        [
            {
                "Company": position.company,
                "Ticker": position.ticker,
                "Quantity": float(position.quantity),
                "Weighted average": clp(position.weighted_average_price_clp),
                "Current price": clp(position.current_price_clp),
                "Current value": clp(position.current_value_clp),
                "Unrealized P/L": clp(position.unrealized_pnl_clp),
                "Unrealized return": percent(position.unrealized_return_pct),
                "Allocation": percent(position.allocation_pct),
            }
            for position in metrics.positions
        ],
        hide_index=True,
        width="stretch",
    )

    if metrics.missing_price_tickers:
        st.warning("Missing prices: " + ", ".join(metrics.missing_price_tickers))

with import_tab:
    st.subheader("Import a brokerage invoice")
    st.write(
        "The PDF is validated and processed in memory. Nothing is saved until you review the "
        "extracted fields and explicitly confirm the purchase."
    )

    sample_pdf_path = Path("output/pdf/ledgerlens_synthetic_invoice.pdf")
    if sample_pdf_path.exists():
        st.download_button(
            "Download synthetic demo invoice",
            data=sample_pdf_path.read_bytes(),
            file_name=sample_pdf_path.name,
            mime="application/pdf",
        )

    extraction_mode = st.radio(
        "Extraction mode",
        ["Offline fixture", "OpenAI Responses API"],
        horizontal=True,
        help="Offline fixture makes no external request. OpenAI mode requires OPENAI_API_KEY.",
    )
    uploaded_invoice = st.file_uploader(
        "Brokerage invoice (PDF)", type=["pdf"], accept_multiple_files=False
    )
    if st.button("Validate and extract", type="primary", disabled=uploaded_invoice is None):
        try:
            pdf = validate_pdf(
                filename=uploaded_invoice.name,
                mime_type=uploaded_invoice.type,
                content=uploaded_invoice.getvalue(),
                max_size_mb=int(os.getenv("LEDGERLENS_MAX_PDF_MB", "10")),
            )
            if extraction_mode == "Offline fixture":
                extractor = FixtureInvoiceExtractor()
            else:
                extractor = OpenAIInvoiceExtractor(OpenAIResponsesClient())
            extraction = extractor.extract(pdf)
            st.session_state["invoice_preview"] = {
                "extraction": extraction.model_dump(mode="json"),
                "document_sha256": pdf.sha256,
                "source": extractor.source_name,
                "size_bytes": pdf.size_bytes,
            }
            st.success("PDF validated. Review every extracted field before saving.")
        except (PDFValidationError, OpenAIConfigurationError, ValueError) as exc:
            st.error(str(exc))
        except Exception:
            st.error("Invoice extraction failed. No purchase or PDF was saved.")

    preview_state = st.session_state.get("invoice_preview")
    if preview_state:
        preview = InvoiceExtraction.model_validate(preview_state["extraction"])
        st.markdown("### Human review")
        st.caption(
            f"Source: {preview_state['source']} · "
            f"PDF size: {preview_state['size_bytes']:,} bytes · "
            f"SHA-256: {preview_state['document_sha256'][:12]}…"
        )
        if preview.warnings:
            for warning in preview.warnings:
                st.warning(warning)

        with st.form("invoice_confirmation_form"):
            company = st.text_input("Company", value=preview.company)
            ticker = st.text_input("Ticker", value=preview.ticker)
            quantity = st.number_input("Quantity", min_value=1, value=preview.quantity, step=1)
            unit_price = st.number_input(
                "Unit price (CLP)", min_value=1, value=preview.unit_price, step=1
            )
            purchase_date: date = st.date_input("Purchase date", value=preview.purchase_date)
            platform = st.text_input("Platform", value=preview.platform)
            currency = st.selectbox("Currency", ["CLP"], index=0)
            document_reference = st.text_input(
                "Document reference", value=preview.document_reference or ""
            )
            reviewed = st.checkbox(
                "I reviewed these fields and explicitly confirm this purchase record."
            )
            save_purchase = st.form_submit_button("Confirm and save purchase", type="primary")

        with st.expander("Field confidence"):
            st.json(preview.confidence.model_dump())

        if save_purchase:
            try:
                edited = InvoiceExtraction(
                    company=company,
                    ticker=ticker,
                    quantity=int(quantity),
                    unit_price=int(unit_price),
                    purchase_date=purchase_date,
                    platform=platform,
                    currency=currency,
                    document_reference=document_reference or None,
                    confidence=preview.confidence,
                    warnings=preview.warnings,
                )
                purchase = confirm_extraction(
                    edited,
                    reviewed_and_confirmed=reviewed,
                    document_sha256=preview_state["document_sha256"],
                    source=preview_state["source"],
                )
                repository.add_purchase(purchase)
                del st.session_state["invoice_preview"]
                st.session_state["purchase_saved_message"] = (
                    "Purchase saved after explicit human confirmation. The uploaded PDF was not "
                    "persisted; only its SHA-256 was retained for traceability."
                )
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

    if message := st.session_state.pop("purchase_saved_message", None):
        st.success(message)

with history_tab:
    st.dataframe(
        [
            {
                "Date": purchase.purchase_date.isoformat(),
                "Company": purchase.company,
                "Ticker": purchase.ticker,
                "Quantity": float(purchase.quantity),
                "Unit price": clp(purchase.unit_price_clp),
                "Platform": purchase.platform,
                "Document": purchase.document_reference,
                "Document hash": (
                    f"{purchase.document_sha256[:12]}…" if purchase.document_sha256 else "—"
                ),
                "Source": purchase.source,
            }
            for purchase in purchases
        ],
        hide_index=True,
        width="stretch",
    )

with insights_tab:
    st.subheader("Portfolio intelligence")
    st.caption(
        "Reproducible analysis date: 2026-07-18. All KPIs are calculated in Python from "
        "synthetic price history."
    )
    narrative_mode = st.radio(
        "Narrative mode",
        ["Deterministic offline", "OpenAI Responses API"],
        horizontal=True,
        key="analyst_narrative_mode",
    )
    narrator = None
    configuration_warning = None
    if narrative_mode == "OpenAI Responses API":
        try:
            narrator = OpenAINarrativeProvider(OpenAIResponsesClient())
        except OpenAIConfigurationError as exc:
            configuration_warning = str(exc)
    if configuration_warning:
        st.warning(
            configuration_warning
            + " Deterministic reports are shown; no external request was attempted."
        )

    intelligence_date = date(2026, 7, 18)
    intelligence_as_of = datetime(2026, 7, 18, 21, 0, tzinfo=UTC)
    history = demo_price_history()
    daily_context = build_daily_context(
        purchases,
        history,
        report_date=intelligence_date,
        as_of=intelligence_as_of,
    )
    weekly_context = build_weekly_context(
        purchases,
        history,
        report_date=intelligence_date,
        as_of=intelligence_as_of,
    )
    daily_report = build_daily_report(daily_context, narrator)
    weekly_report = build_weekly_report(weekly_context, narrator)

    daily_tab, weekly_tab = st.tabs(["Daily Lens", "Weekly Lens"])
    with daily_tab:
        daily_one, daily_two, daily_three, daily_four = st.columns(4)
        daily_one.metric("Portfolio value", clp(daily_context.current_value_clp))
        daily_two.metric(
            "Daily observable movement",
            clp(daily_context.daily_change_clp),
            percent(daily_context.daily_change_pct),
        )
        daily_three.metric("Unrealized P/L", clp(daily_context.unrealized_pnl_clp))
        daily_four.metric("Price coverage", percent(daily_context.price_coverage_pct))
        st.markdown(daily_report.text)
        st.caption(f"Narrative source: {daily_report.source}")
        if daily_report.warning:
            st.warning(daily_report.warning)
        st.dataframe(
            [
                {"Ticker": item.ticker, "Daily contribution": clp(item.amount_clp)}
                for item in daily_context.contributions
            ],
            hide_index=True,
            width="stretch",
        )
        if daily_context.missing_price_tickers:
            st.warning("Missing prices: " + ", ".join(daily_context.missing_price_tickers))
        if daily_context.stale_price_tickers:
            st.warning("Stale prices: " + ", ".join(daily_context.stale_price_tickers))

    with weekly_tab:
        weekly_one, weekly_two, weekly_three, weekly_four = st.columns(4)
        weekly_one.metric(
            "Weekly observable movement",
            clp(weekly_context.current_week_change_clp),
            percent(weekly_context.current_week_change_pct),
        )
        weekly_two.metric(
            "Difference vs prior week",
            clp(weekly_context.difference_vs_previous_week_clp),
        )
        weekly_three.metric(
            "Baseline average",
            clp(weekly_context.baseline_average_change_clp),
            f"{weekly_context.baseline_weeks} observed weeks",
        )
        weekly_four.metric("Price coverage", percent(weekly_context.price_coverage_pct))
        st.markdown(weekly_report.text)
        st.caption(f"Narrative source: {weekly_report.source}")
        if weekly_report.warning:
            st.warning(weekly_report.warning)
        st.dataframe(
            [
                {"Ticker": item.ticker, "Weekly contribution": clp(item.amount_clp)}
                for item in weekly_context.contributions
            ],
            hide_index=True,
            width="stretch",
        )
        details_left, details_right = st.columns(2)
        details_left.write(
            "Positions added: " + (", ".join(weekly_context.positions_added) or "None")
        )
        details_left.write(f"Missing invoices: {weekly_context.missing_invoices}")
        details_left.write(f"Incomplete records: {weekly_context.incomplete_records}")
        details_right.write(
            "Best observable day: "
            + (
                f"{weekly_context.best_day.movement_date}: "
                f"{clp(weekly_context.best_day.amount_clp)}"
                if weekly_context.best_day
                else "Not available"
            )
        )
        details_right.write(
            "Worst observable day: "
            + (
                f"{weekly_context.worst_day.movement_date}: "
                f"{clp(weekly_context.worst_day.amount_clp)}"
                if weekly_context.worst_day
                else "Not available"
            )
        )

with about_tab:
    st.markdown(
        """
        LedgerLens provides an offline, deterministic path from synthetic purchases to a calculated
        portfolio. Invoice extraction produces an editable draft and saving requires explicit human
        confirmation. The Daily/Weekly Lens will be added as separate modules. No model is asked to
        calculate financial metrics.
        """
    )
