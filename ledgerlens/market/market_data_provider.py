from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from typing import Protocol

from ledgerlens.domain.models import MarketPrice


class MarketDataProvider(Protocol):
    def get_prices(self, tickers: set[str]) -> dict[str, MarketPrice]: ...


class FixtureMarketDataProvider:
    def __init__(self, prices: dict[str, MarketPrice]) -> None:
        self._prices = prices

    def get_prices(self, tickers: set[str]) -> dict[str, MarketPrice]:
        return {ticker: self._prices[ticker] for ticker in tickers if ticker in self._prices}


class YFinanceMarketDataProvider:
    """Optional live provider. Demo and tests never instantiate this adapter."""

    def get_prices(self, tickers: set[str]) -> dict[str, MarketPrice]:
        import yfinance as yf

        prices: dict[str, MarketPrice] = {}
        for ticker in sorted(tickers):
            try:
                history = yf.Ticker(ticker).history(period="5d", auto_adjust=False)
                close = history["Close"].dropna()
                if not close.empty:
                    prices[ticker] = MarketPrice(
                        ticker=ticker,
                        price_clp=Decimal(str(close.iloc[-1])),
                        as_of=datetime.now(UTC),
                        source="yfinance",
                    )
            except Exception:
                continue
        return prices

