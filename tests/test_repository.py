import sqlite3
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from ledgerlens.data.portfolio_repository import SQLitePortfolioRepository
from sample_data.demo_data import demo_purchases


def test_sqlite_repository_round_trip() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    original = demo_purchases()[0]

    repository.add_purchase(original)
    stored = repository.list_purchases()

    assert stored == [original]
    assert stored[0].quantity == Decimal("120")
    repository.close()


def test_seed_is_idempotent() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    purchases = demo_purchases()

    repository.seed_if_empty(purchases)
    repository.seed_if_empty(purchases)

    assert len(repository.list_purchases()) == len(purchases)
    repository.close()


def test_sync_synthetic_seed_updates_only_demo_records() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    original = demo_purchases()
    repository.seed_if_empty(original)
    updated = demo_purchases()

    repository.sync_synthetic_seed(updated)

    assert repository.list_purchases() == updated
    repository.close()


def test_void_and_restore_purchase_preserve_audit_fields() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    purchases = demo_purchases()
    repository.seed_if_empty(purchases)
    voided_at = datetime(2026, 7, 19, 18, 30, tzinfo=UTC)

    changed = repository.void_purchases(
        [purchases[0].id], "Duplicate record", voided_at=voided_at
    )

    assert changed == 1
    assert purchases[0].id not in {item.id for item in repository.list_purchases()}
    stored = {
        item.id: item for item in repository.list_purchases(include_voided=True)
    }[purchases[0].id]
    assert stored.status == "voided"
    assert stored.voided_at == voided_at
    assert stored.void_reason == "Duplicate record"

    assert repository.restore_purchases([purchases[0].id]) == 1
    restored = {item.id: item for item in repository.list_purchases()}[purchases[0].id]
    assert restored.status == "active"
    assert restored.voided_at is None
    assert restored.void_reason is None
    repository.close()


def test_void_multiple_ticker_lots_is_atomic_and_idempotent() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    purchases = demo_purchases()
    repository.seed_if_empty(purchases)
    cordillera_ids = [item.id for item in purchases if item.ticker == "CORD-A.SN"]

    assert repository.void_purchases(cordillera_ids, "Entry error") == 2
    assert repository.void_purchases(cordillera_ids, "Entry error") == 0
    assert {item.ticker for item in repository.list_purchases()} == {"PACIF.SN", "AUST.SN"}
    repository.close()


def test_synthetic_sync_does_not_reactivate_voided_record() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    purchases = demo_purchases()
    repository.sync_synthetic_seed(purchases)
    repository.void_purchases([purchases[0].id], "Incorrect document")

    repository.sync_synthetic_seed(demo_purchases())

    stored = {
        item.id: item for item in repository.list_purchases(include_voided=True)
    }[purchases[0].id]
    assert stored.status == "voided"
    assert stored.void_reason == "Incorrect document"
    repository.close()


def test_void_requires_audit_reason() -> None:
    repository = SQLitePortfolioRepository(":memory:")
    purchase = demo_purchases()[0]
    repository.add_purchase(purchase)

    with pytest.raises(ValueError, match="at least 3 characters"):
        repository.void_purchases([purchase.id], "  ")

    assert repository.list_purchases() == [purchase]
    repository.close()


def test_existing_database_is_migrated_for_void_audit_fields(tmp_path: Path) -> None:
    database_path = tmp_path / "legacy.db"
    connection = sqlite3.connect(database_path)
    connection.execute(
        """
        CREATE TABLE purchases (
            id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            ticker TEXT NOT NULL,
            quantity TEXT NOT NULL,
            unit_price_clp TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            platform TEXT NOT NULL,
            currency TEXT NOT NULL,
            document_reference TEXT,
            source TEXT NOT NULL,
            confirmed_at TEXT
        )
        """
    )
    connection.commit()
    connection.close()

    repository = SQLitePortfolioRepository(database_path)
    purchase = demo_purchases()[0]
    repository.add_purchase(purchase)
    assert repository.void_purchases([purchase.id], "Entry error") == 1

    stored = repository.list_purchases(include_voided=True)[0]
    assert stored.status == "voided"
    assert stored.document_sha256 is None
    assert stored.voided_at is not None
    repository.close()
