from decimal import Decimal

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
