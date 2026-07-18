from __future__ import annotations

import sqlite3
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Protocol

from ledgerlens.domain.models import Purchase


class PortfolioRepository(Protocol):
    def list_purchases(self) -> list[Purchase]: ...

    def add_purchase(self, purchase: Purchase) -> None: ...


class SQLitePortfolioRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS purchases (
                id TEXT PRIMARY KEY,
                company TEXT NOT NULL,
                ticker TEXT NOT NULL,
                quantity TEXT NOT NULL,
                unit_price_clp TEXT NOT NULL,
                purchase_date TEXT NOT NULL,
                platform TEXT NOT NULL,
                currency TEXT NOT NULL,
                document_reference TEXT,
                document_sha256 TEXT,
                source TEXT NOT NULL,
                confirmed_at TEXT
            )
            """
        )
        columns = {
            row["name"] for row in self._connection.execute("PRAGMA table_info(purchases)")
        }
        if "document_sha256" not in columns:
            self._connection.execute("ALTER TABLE purchases ADD COLUMN document_sha256 TEXT")
        self._connection.commit()

    def list_purchases(self) -> list[Purchase]:
        rows = self._connection.execute(
            "SELECT * FROM purchases ORDER BY purchase_date, id"
        ).fetchall()
        return [
            Purchase(
                id=row["id"],
                company=row["company"],
                ticker=row["ticker"],
                quantity=Decimal(row["quantity"]),
                unit_price_clp=Decimal(row["unit_price_clp"]),
                purchase_date=date.fromisoformat(row["purchase_date"]),
                platform=row["platform"],
                currency=row["currency"],
                document_reference=row["document_reference"],
                document_sha256=row["document_sha256"],
                source=row["source"],
                confirmed_at=(
                    datetime.fromisoformat(row["confirmed_at"])
                    if row["confirmed_at"]
                    else None
                ),
            )
            for row in rows
        ]

    def add_purchase(self, purchase: Purchase) -> None:
        self._connection.execute(
            """
            INSERT INTO purchases (
                id, company, ticker, quantity, unit_price_clp, purchase_date,
                platform, currency, document_reference, source, confirmed_at
                , document_sha256
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                purchase.id,
                purchase.company,
                purchase.ticker,
                str(purchase.quantity),
                str(purchase.unit_price_clp),
                purchase.purchase_date.isoformat(),
                purchase.platform,
                purchase.currency,
                purchase.document_reference,
                purchase.source,
                purchase.confirmed_at.isoformat() if purchase.confirmed_at else None,
                purchase.document_sha256,
            ),
        )
        self._connection.commit()

    def seed_if_empty(self, purchases: list[Purchase]) -> None:
        existing = self._connection.execute("SELECT COUNT(*) FROM purchases").fetchone()[0]
        if existing == 0:
            for purchase in purchases:
                self.add_purchase(purchase)

    def sync_synthetic_seed(self, purchases: list[Purchase]) -> None:
        for purchase in purchases:
            if purchase.source != "synthetic":
                raise ValueError("Only synthetic seed records may be synchronized.")
            self._connection.execute(
                """
                INSERT INTO purchases (
                    id, company, ticker, quantity, unit_price_clp, purchase_date,
                    platform, currency, document_reference, source, confirmed_at,
                    document_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    company=excluded.company,
                    ticker=excluded.ticker,
                    quantity=excluded.quantity,
                    unit_price_clp=excluded.unit_price_clp,
                    purchase_date=excluded.purchase_date,
                    platform=excluded.platform,
                    currency=excluded.currency,
                    document_reference=excluded.document_reference,
                    confirmed_at=excluded.confirmed_at,
                    document_sha256=excluded.document_sha256
                WHERE purchases.source = 'synthetic'
                """,
                (
                    purchase.id,
                    purchase.company,
                    purchase.ticker,
                    str(purchase.quantity),
                    str(purchase.unit_price_clp),
                    purchase.purchase_date.isoformat(),
                    purchase.platform,
                    purchase.currency,
                    purchase.document_reference,
                    purchase.source,
                    purchase.confirmed_at.isoformat() if purchase.confirmed_at else None,
                    purchase.document_sha256,
                ),
            )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()
