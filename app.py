from __future__ import annotations

import os
from datetime import UTC, date, datetime
from pathlib import Path

import streamlit as st

from ledgerlens.ai.invoice_extractor import FixtureInvoiceExtractor, OpenAIInvoiceExtractor
from ledgerlens.ai.openai_client import OpenAIConfigurationError, OpenAIResponsesClient
from ledgerlens.analysts.daily import build_daily_report
from ledgerlens.analysts.narrator import OpenAINarrativeProvider
from ledgerlens.analysts.weekly import build_weekly_report
from ledgerlens.analytics.portfolio_dashboard import (
    build_portfolio_history,
    calculate_platform_allocations,
)
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
from ledgerlens.ui.components import (
    render_app_header,
    render_confidence_grid,
    render_document_policy,
    render_notice,
    render_section_header,
    render_source_metadata,
    render_workflow_steps,
)
from ledgerlens.ui.history import render_purchase_history
from ledgerlens.ui.insights import render_intelligence_dashboard
from ledgerlens.ui.portfolio import render_portfolio_dashboard
from ledgerlens.ui.theme import apply_theme
from sample_data.demo_data import demo_price_history, demo_prices, demo_purchases

load_project_environment()

st.set_page_config(page_title="LedgerLens", page_icon="LL", layout="wide")
apply_theme()
render_app_header(
    subtitle="Verified portfolio intelligence with deterministic analytics.",
)

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
price_history = demo_price_history()
portfolio_history = build_portfolio_history(purchases, price_history)
platform_allocations = calculate_platform_allocations(purchases)

render_notice(
    "Demo mode: all purchases, companies, document references, and prices are synthetic. "
    "This is descriptive software, not financial advice."
)

portfolio_tab, import_tab, history_tab, insights_tab, about_tab = st.tabs(
    ["Portfolio", "Import purchase", "Purchase history", "AI Insights", "About"]
)

with portfolio_tab:
    render_portfolio_dashboard(metrics, portfolio_history, platform_allocations)

with import_tab:
    saved_message = st.session_state.pop("purchase_saved_message", None)
    extraction_message = st.session_state.pop("invoice_extraction_message", None)
    preview_state = st.session_state.get("invoice_preview")
    uploader_state = st.session_state.get("invoice_uploader")
    current_step = (
        "confirm"
        if saved_message
        else "review"
        if preview_state
        else "extract"
        if uploader_state
        else "upload"
    )
    render_section_header(
        "Import a brokerage invoice",
        "Validate, extract, review, and explicitly confirm one synthetic purchase record.",
    )
    render_workflow_steps(current_step)
    if extraction_message:
        st.success(extraction_message)
    if saved_message:
        st.success(saved_message)

    controls_column, policy_column = st.columns([1.15, 0.85])
    with controls_column:
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
            "Brokerage invoice (PDF)",
            type=["pdf"],
            accept_multiple_files=False,
            key="invoice_uploader",
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
                st.session_state["invoice_extraction_message"] = (
                    "PDF validated and extracted. Review every field before confirmation."
                )
                st.rerun()
            except (PDFValidationError, OpenAIConfigurationError, ValueError) as exc:
                st.error(str(exc))
            except Exception:
                st.error("Invoice extraction failed. No purchase or PDF was saved.")
    with policy_column:
        render_document_policy()

    if preview_state:
        preview = InvoiceExtraction.model_validate(preview_state["extraction"])
        st.write("")
        render_section_header(
            "Human review",
            "Extracted values remain an editable draft until the confirmation checkbox "
            "is selected.",
        )
        render_source_metadata(
            source=preview_state["source"],
            size_bytes=preview_state["size_bytes"],
            sha256_prefix=preview_state["document_sha256"][:12],
        )
        if preview.warnings:
            for warning in preview.warnings:
                st.warning(warning)

        with st.form("invoice_confirmation_form"):
            form_left, form_right = st.columns(2)
            with form_left:
                company = st.text_input("Company", value=preview.company)
                ticker = st.text_input("Ticker", value=preview.ticker)
                quantity = st.number_input(
                    "Quantity", min_value=1, value=preview.quantity, step=1
                )
                unit_price = st.number_input(
                    "Unit price (CLP)", min_value=1, value=preview.unit_price, step=1
                )
            with form_right:
                purchase_date: date = st.date_input(
                    "Purchase date", value=preview.purchase_date
                )
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
            render_confidence_grid(preview.confidence.model_dump())

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

with history_tab:
    render_purchase_history(purchases)

with insights_tab:
    render_section_header(
        "Portfolio intelligence",
        "Reproducible analysis date: 2026-07-18. All KPIs are calculated in Python from "
        "synthetic price history.",
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
    daily_context = build_daily_context(
        purchases,
        price_history,
        report_date=intelligence_date,
        as_of=intelligence_as_of,
    )
    weekly_context = build_weekly_context(
        purchases,
        price_history,
        report_date=intelligence_date,
        as_of=intelligence_as_of,
    )
    daily_report = build_daily_report(daily_context, narrator)
    weekly_report = build_weekly_report(weekly_context, narrator)

    render_intelligence_dashboard(
        daily_context,
        daily_report,
        weekly_context,
        weekly_report,
    )

with about_tab:
    st.markdown(
        """
        LedgerLens provides an offline, deterministic path from synthetic purchases to a calculated
        portfolio. Invoice extraction produces an editable draft and saving requires explicit human
        confirmation. Daily and Weekly Lens provide descriptive context from deterministic Python
        metrics. No model is asked to calculate financial metrics.
        """
    )
