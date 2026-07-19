from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal

import streamlit as st

from ledgerlens.domain.models import Purchase
from ledgerlens.ui.components import render_kpi_card, render_section_header
from ledgerlens.ui.formatters import clp


@dataclass(frozen=True, slots=True)
class PurchaseHistoryAction:
    kind: Literal["void", "restore"]
    purchase_ids: tuple[str, ...]
    reason: str | None = None


def source_label(source: str) -> str:
    return {
        "synthetic": "Synthetic seed",
        "offline_fixture": "Offline fixture",
        "openai_responses_api": "OpenAI extraction",
        "manual": "Manual",
    }.get(source, source.replace("_", " ").title())


def status_label(status: str) -> str:
    return {"active": "Active", "voided": "Voided"}.get(status, status.title())


def filter_purchases(
    purchases: list[Purchase],
    *,
    tickers: list[str],
    platforms: list[str],
    sources: list[str],
    start_date: date,
    end_date: date,
    statuses: list[str] | None = None,
) -> list[Purchase]:
    return [
        purchase
        for purchase in purchases
        if (not tickers or purchase.ticker in tickers)
        and (not platforms or purchase.platform in platforms)
        and (not sources or purchase.source in sources)
        and (not statuses or purchase.status in statuses)
        and start_date <= purchase.purchase_date <= end_date
    ]


def purchase_option_label(purchase: Purchase) -> str:
    reference = purchase.document_reference or purchase.id
    return (
        f"{purchase.purchase_date.isoformat()} | {purchase.ticker} | "
        f"{purchase.platform} | {reference}"
    )


def void_target_ids(
    purchases: list[Purchase], selected_id: str, *, all_ticker_records: bool
) -> tuple[str, ...]:
    selected = next(
        (
            purchase
            for purchase in purchases
            if purchase.id == selected_id and purchase.status == "active"
        ),
        None,
    )
    if selected is None:
        return ()
    if not all_ticker_records:
        return (selected.id,)
    return tuple(
        purchase.id
        for purchase in purchases
        if purchase.status == "active" and purchase.ticker == selected.ticker
    )


def _render_record_management(
    purchases: list[Purchase],
) -> PurchaseHistoryAction | None:
    active = [purchase for purchase in purchases if purchase.status == "active"]
    voided = [purchase for purchase in purchases if purchase.status == "voided"]

    with st.expander("Manage ledger records"):
        st.caption(
            "Void errors or duplicates without erasing the audit trail. A void is not a sale and "
            "does not calculate realized profit or loss."
        )
        action_options = ["Void active records"]
        if voided:
            action_options.append("Restore a voided record")
        selected_action = st.radio(
            "Action",
            action_options,
            horizontal=True,
            key="history_management_action",
        )

        if selected_action == "Restore a voided record":
            voided_by_id = {purchase.id: purchase for purchase in voided}
            selected_id = st.selectbox(
                "Voided record",
                list(voided_by_id),
                format_func=lambda item: purchase_option_label(voided_by_id[item]),
                key="history_restore_record",
            )
            selected = voided_by_id[selected_id]
            st.info(f"Correction reason: {selected.void_reason or 'Not recorded'}")
            confirmed = st.checkbox(
                "I reviewed this record and want to return it to the active portfolio.",
                key="history_restore_confirmation",
            )
            if st.button(
                "Restore record",
                type="secondary",
                key="history_restore_button",
            ):
                if not confirmed:
                    st.error("Confirm the restoration before continuing.")
                    return None
                return PurchaseHistoryAction("restore", (selected_id,))
            return None

        if not active:
            st.info("No active records are available to void.")
            return None

        active_by_id = {purchase.id: purchase for purchase in active}
        selected_id = st.selectbox(
            "Active record",
            list(active_by_id),
            format_func=lambda item: purchase_option_label(active_by_id[item]),
            key="history_void_record",
        )
        selected = active_by_id[selected_id]
        ticker_records = [
            purchase for purchase in active if purchase.ticker == selected.ticker
        ]
        scope_options = ["Selected record only"]
        if len(ticker_records) > 1:
            scope_options.append(
                f"All {len(ticker_records)} active {selected.ticker} records"
            )
        selected_scope = st.radio(
            "Scope",
            scope_options,
            key="history_void_scope",
        )
        all_ticker_records = selected_scope != "Selected record only"
        target_ids = void_target_ids(
            purchases,
            selected_id,
            all_ticker_records=all_ticker_records,
        )
        target_records = [purchase for purchase in active if purchase.id in target_ids]
        invested_cost = sum(
            (purchase.quantity * purchase.unit_price_clp for purchase in target_records),
            start=Decimal("0"),
        )
        st.warning(
            f"This will remove {len(target_ids)} active record(s) from portfolio calculations "
            f"with an invested cost of {clp(invested_cost)}. The records remain auditable."
        )

        reason_category = st.selectbox(
            "Correction reason",
            ["Entry error", "Duplicate record", "Incorrect document", "Other correction"],
            key="history_void_reason",
        )
        reason_detail = st.text_input(
            "Optional detail",
            max_chars=160,
            placeholder="Add concise context for the audit trail",
            key="history_void_reason_detail",
        )
        confirmed = st.checkbox(
            "I understand this is a correction, not a sale transaction.",
            key="history_void_confirmation",
        )
        if st.button(
            f"Void {len(target_ids)} record{'s' if len(target_ids) != 1 else ''}",
            type="secondary",
            key="history_void_button",
        ):
            if not confirmed:
                st.error("Confirm the correction before continuing.")
                return None
            if reason_category == "Other correction" and len(reason_detail.strip()) < 3:
                st.error("Add at least 3 characters of detail for an other correction.")
                return None
            reason = reason_category
            if reason_detail.strip():
                reason = f"{reason_category}: {reason_detail.strip()}"
            return PurchaseHistoryAction("void", target_ids, reason)
    return None


def render_purchase_history(purchases: list[Purchase]) -> PurchaseHistoryAction | None:
    render_section_header(
        "Purchase history",
        "Auditable ledger of active and corrected records. Filters never alter stored data.",
    )
    if not purchases:
        st.info("No confirmed purchases are available.")
        return None

    ticker_options = sorted({purchase.ticker for purchase in purchases})
    platform_options = sorted({purchase.platform for purchase in purchases})
    source_options = sorted({purchase.source for purchase in purchases})
    status_options = [
        status
        for status in ("active", "voided")
        if any(purchase.status == status for purchase in purchases)
    ]
    minimum_date = min(purchase.purchase_date for purchase in purchases)
    maximum_date = max(purchase.purchase_date for purchase in purchases)

    with st.container(border=True):
        render_section_header("Filters", "Leave a selector empty to include every value.")
        ticker_column, platform_column, source_column, status_column = st.columns(4)
        with ticker_column:
            selected_tickers = st.multiselect(
                "Ticker", ticker_options, key="history_ticker_filter"
            )
        with platform_column:
            selected_platforms = st.multiselect(
                "Platform", platform_options, key="history_platform_filter"
            )
        with source_column:
            selected_sources = st.multiselect(
                "Source",
                source_options,
                format_func=source_label,
                key="history_source_filter",
            )
        with status_column:
            selected_statuses = st.multiselect(
                "Status",
                status_options,
                default=["active"] if "active" in status_options else status_options,
                format_func=status_label,
                key="history_status_filter",
            )
        selected_dates = st.date_input(
            "Purchase date range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
            key="history_date_filter",
        )

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
    elif isinstance(selected_dates, tuple) and len(selected_dates) == 1:
        start_date = end_date = selected_dates[0]
    else:
        start_date = end_date = selected_dates

    filtered = filter_purchases(
        purchases,
        tickers=selected_tickers,
        platforms=selected_platforms,
        sources=selected_sources,
        start_date=start_date,
        end_date=end_date,
        statuses=selected_statuses,
    )

    st.write("")
    records, tickers, platforms, sources = st.columns(4)
    with records:
        render_kpi_card(
            label="Visible records",
            value=str(len(filtered)),
            delta=f"of {len(purchases)} ledger entries",
            tone="primary",
        )
    with tickers:
        render_kpi_card(
            label="Visible tickers",
            value=str(len({purchase.ticker for purchase in filtered})),
            delta="Distinct positions",
        )
    with platforms:
        render_kpi_card(
            label="Visible platforms",
            value=str(len({purchase.platform for purchase in filtered})),
            delta="Recorded brokers",
        )
    with sources:
        render_kpi_card(
            label="Visible sources",
            value=str(len({purchase.source for purchase in filtered})),
            delta="Traceable origins",
        )

    st.write("")
    if not filtered:
        st.info("No purchases match the selected filters.")
    else:
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
                        f"{purchase.document_sha256[:12]}..."
                        if purchase.document_sha256
                        else "—"
                    ),
                    "Source": source_label(purchase.source),
                    "Status": status_label(purchase.status),
                    "Correction": purchase.void_reason or "—",
                }
                for purchase in filtered
            ],
            hide_index=True,
            width="stretch",
        )

    st.write("")
    return _render_record_management(purchases)
