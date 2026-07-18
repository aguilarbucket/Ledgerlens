from __future__ import annotations

import os
from decimal import Decimal
from pathlib import Path

import streamlit as st

from ledgerlens.analytics.portfolio_metrics import calculate_portfolio_metrics
from ledgerlens.data.portfolio_repository import SQLitePortfolioRepository
from ledgerlens.market.market_data_provider import FixtureMarketDataProvider
from sample_data.demo_data import demo_prices, demo_purchases


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
repository.seed_if_empty(demo_purchases())
purchases = repository.list_purchases()
provider = FixtureMarketDataProvider(demo_prices())
prices = provider.get_prices({purchase.ticker for purchase in purchases})
metrics = calculate_portfolio_metrics(purchases, prices)

st.info(
    "Demo mode: all purchases, companies, document references, and prices are synthetic. "
    "This is descriptive software, not financial advice."
)

portfolio_tab, history_tab, about_tab = st.tabs(["Portfolio", "Purchase history", "About"])

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
                "Source": purchase.source,
            }
            for purchase in purchases
        ],
        hide_index=True,
        width="stretch",
    )

with about_tab:
    st.markdown(
        """
        This first Build Week slice proves an offline, deterministic path from synthetic purchases
        to a calculated portfolio. OpenAI invoice extraction and the Daily/Weekly Lens will be added
        as separate modules. No model is asked to calculate financial metrics.
        """
    )

