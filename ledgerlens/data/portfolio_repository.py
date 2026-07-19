from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Protocol

from ledgerlens.domain.models import Purchase


class PortfolioRepository(Protocol):
    def list_purchases(self, *, include_voided: bool = False) -> list[Purchase]: ...

    def add_purchase(self, purchase: Purchase) -> None: ...

    def void_purchases(
        self,
        purchase_ids: Sequence[str],
        reason: str,
        *,
        voided_at: datetime | None = None,
    ) -> int: ...

    def restore_purchases(self, purchase_ids: Sequence[str]) -> int: ...


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
                confirmed_at TEXT,
                status TEXT NOT NULL DEFAULT 'active',
                voided_at TEXT,
                void_reason TEXT
            )
            """
        )
        columns = {
            row["name"] for row in self._connection.execute("PRAGMA table_info(purchases)")
        }
        if "document_sha256" not in columns:
            self._connection.execute("ALTER TABLE purchases ADD COLUMN document_sha256 TEXT")
        if "status" not in columns:
            self._connection.execute(
                "ALTER TABLE purchases ADD COLUMN status TEXT NOT NULL DEFAULT 'active'"
            )
        if "voided_at" not in columns:
            self._connection.execute("ALTER TABLE purchases ADD COLUMN voided_at TEXT")
        if "void_reason" not in columns:
            self._connection.execute("ALTER TABLE purchases ADD COLUMN void_reason TEXT")
        self._connection.commit()

    def list_purchases(self, *, include_voided: bool = False) -> list[Purchase]:
        where_clause = "" if include_voided else "WHERE status = 'active'"
        rows = self._connection.execute(
            f"SELECT * FROM purchases {where_clause} ORDER BY purchase_date, id"
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
                status=row["status"],
                voided_at=(
                    datetime.fromisoformat(row["voided_at"]) if row["voided_at"] else None
                ),
                void_reason=row["void_reason"],
            )
            for row in rows
        ]

    def add_purchase(self, purchase: Purchase) -> None:
        if purchase.status not in {"active", "voided"}:
            raise ValueError("Purchase status must be active or voided.")
        self._connection.execute(
            """
            INSERT INTO purchases (
                id, company, ticker, quantity, unit_price_clp, purchase_date,
                platform, currency, document_reference, source, confirmed_at
                , document_sha256, status, voided_at, void_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                purchase.status,
                purchase.voided_at.isoformat() if purchase.voided_at else None,
                purchase.void_reason,
            ),
        )
        self._connection.commit()

    @staticmethod
    def _normalized_ids(purchase_ids: Sequence[str]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(item.strip() for item in purchase_ids if item.strip()))

    def void_purchases(
        self,
        purchase_ids: Sequence[str],
        reason: str,
        *,
        voided_at: datetime | None = None,
    ) -> int:
        normalized_ids = self._normalized_ids(purchase_ids)
        normalized_reason = " ".join(reason.split())
        if not normalized_ids:
            return 0
        if len(normalized_reason) < 3:
            raise ValueError("A correction reason of at least 3 characters is required.")
        if len(normalized_reason) > 240:
            raise ValueError("The correction reason must be 240 characters or fewer.")

        placeholders = ", ".join("?" for _ in normalized_ids)
        effective_time = voided_at or datetime.now(UTC)
        cursor = self._connection.execute(
            f"""
            UPDATE purchases
            SET status = 'voided', voided_at = ?, void_reason = ?
            WHERE status = 'active' AND id IN ({placeholders})
            """,
            (effective_time.isoformat(), normalized_reason, *normalized_ids),
        )
        self._connection.commit()
        return cursor.rowcount

    def restore_purchases(self, purchase_ids: Sequence[str]) -> int:
        normalized_ids = self._normalized_ids(purchase_ids)
        if not normalized_ids:
            return 0

        placeholders = ", ".join("?" for _ in normalized_ids)
        cursor = self._connection.execute(
            f"""
            UPDATE purchases
            SET status = 'active', voided_at = NULL, void_reason = NULL
            WHERE status = 'voided' AND id IN ({placeholders})
            """,
            normalized_ids,
        )
        self._connection.commit()
        return cursor.rowcount

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
