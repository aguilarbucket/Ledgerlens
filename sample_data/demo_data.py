from datetime import UTC, date, datetime
from decimal import Decimal

from ledgerlens.domain.models import MarketPrice, Purchase


def demo_purchases() -> list[Purchase]:
    return [
        Purchase(
            id="demo-001",
            company="Cordillera Energía",
            ticker="CORD-A.SN",
            quantity=Decimal("120"),
            unit_price_clp=Decimal("845"),
            purchase_date=date(2026, 7, 14),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-001",
            source="synthetic",
            confirmed_at=datetime(2026, 7, 14, 15, 30, tzinfo=UTC),
        ),
        Purchase(
            id="demo-002",
            company="Cordillera Energía",
            ticker="CORD-A.SN",
            quantity=Decimal("80"),
            unit_price_clp=Decimal("875"),
            purchase_date=date(2026, 7, 16),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-002",
            source="synthetic",
            confirmed_at=datetime(2026, 7, 16, 14, 10, tzinfo=UTC),
        ),
        Purchase(
            id="demo-003",
            company="Pacífico Retail",
            ticker="PACIF.SN",
            quantity=Decimal("75"),
            unit_price_clp=Decimal("1320"),
            purchase_date=date(2026, 7, 15),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-003",
            source="synthetic",
            confirmed_at=datetime(2026, 7, 15, 16, 5, tzinfo=UTC),
        ),
        Purchase(
            id="demo-004",
            company="Austral Telecom",
            ticker="AUST.SN",
            quantity=Decimal("40"),
            unit_price_clp=Decimal("2140"),
            purchase_date=date(2026, 7, 17),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-004",
            source="synthetic",
            confirmed_at=datetime(2026, 7, 17, 18, 20, tzinfo=UTC),
        ),
    ]


def demo_prices() -> dict[str, MarketPrice]:
    as_of = datetime(2026, 7, 18, 20, 0, tzinfo=UTC)
    return {
        "CORD-A.SN": MarketPrice("CORD-A.SN", Decimal("910"), as_of, "synthetic_fixture"),
        "PACIF.SN": MarketPrice("PACIF.SN", Decimal("1285"), as_of, "synthetic_fixture"),
        "AUST.SN": MarketPrice("AUST.SN", Decimal("2210"), as_of, "synthetic_fixture"),
    }

