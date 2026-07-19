from __future__ import annotations

from datetime import date

import streamlit as st

from ledgerlens.domain.models import Purchase
from ledgerlens.ui.components import render_kpi_card, render_section_header
from ledgerlens.ui.formatters import clp


def source_label(source: str) -> str:
    return {
        "synthetic": "Synthetic seed",
        "offline_fixture": "Offline fixture",
        "openai_responses_api": "OpenAI extraction",
        "manual": "Manual",
    }.get(source, source.replace("_", " ").title())


def filter_purchases(
    purchases: list[Purchase],
    *,
    tickers: list[str],
    platforms: list[str],
    sources: list[str],
    start_date: date,
    end_date: date,
) -> list[Purchase]:
    return [
        purchase
        for purchase in purchases
        if (not tickers or purchase.ticker in tickers)
        and (not platforms or purchase.platform in platforms)
        and (not sources or purchase.source in sources)
        and start_date <= purchase.purchase_date <= end_date
    ]


def render_purchase_history(purchases: list[Purchase]) -> None:
    render_section_header(
        "Purchase history",
        "Read-only ledger of confirmed records. Filters never alter stored purchases.",
    )
    if not purchases:
        st.info("No confirmed purchases are available.")
        return

    ticker_options = sorted({purchase.ticker for purchase in purchases})
    platform_options = sorted({purchase.platform for purchase in purchases})
    source_options = sorted({purchase.source for purchase in purchases})
    minimum_date = min(purchase.purchase_date for purchase in purchases)
    maximum_date = max(purchase.purchase_date for purchase in purchases)

    with st.container(border=True):
        render_section_header("Filters", "Leave a selector empty to include every value.")
        ticker_column, platform_column, source_column = st.columns(3)
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
    )

    st.write("")
    records, tickers, platforms, sources = st.columns(4)
    with records:
        render_kpi_card(
            label="Visible records",
            value=str(len(filtered)),
            delta=f"of {len(purchases)} confirmed",
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
        return

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
                    f"{purchase.document_sha256[:12]}…"
                    if purchase.document_sha256
                    else "—"
                ),
                "Source": source_label(purchase.source),
            }
            for purchase in filtered
        ],
        hide_index=True,
        width="stretch",
    )
