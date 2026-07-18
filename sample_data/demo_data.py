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
            purchase_date=date(2026, 5, 18),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-001",
            source="synthetic",
            confirmed_at=datetime(2026, 5, 18, 15, 30, tzinfo=UTC),
        ),
        Purchase(
            id="demo-002",
            company="Cordillera Energía",
            ticker="CORD-A.SN",
            quantity=Decimal("80"),
            unit_price_clp=Decimal("875"),
            purchase_date=date(2026, 6, 16),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-002",
            source="synthetic",
            confirmed_at=datetime(2026, 6, 16, 14, 10, tzinfo=UTC),
        ),
        Purchase(
            id="demo-003",
            company="Pacífico Retail",
            ticker="PACIF.SN",
            quantity=Decimal("75"),
            unit_price_clp=Decimal("1320"),
            purchase_date=date(2026, 6, 24),
            platform="Corredora Demo",
            document_reference="SYNTH-INV-003",
            source="synthetic",
            confirmed_at=datetime(2026, 6, 24, 16, 5, tzinfo=UTC),
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


def demo_price_history() -> dict[date, dict[str, MarketPrice]]:
    values = {
        date(2026, 5, 15): ("820", "1300", "2050"),
        date(2026, 5, 22): ("830", "1290", "2060"),
        date(2026, 5, 29): ("840", "1310", "2040"),
        date(2026, 6, 5): ("855", "1305", "2070"),
        date(2026, 6, 12): ("850", "1325", "2080"),
        date(2026, 6, 19): ("870", "1340", "2090"),
        date(2026, 6, 26): ("865", "1330", "2110"),
        date(2026, 7, 3): ("880", "1315", "2105"),
        date(2026, 7, 10): ("890", "1300", "2130"),
        date(2026, 7, 13): ("895", "1295", "2140"),
        date(2026, 7, 14): ("900", "1300", "2120"),
        date(2026, 7, 15): ("905", "1290", "2150"),
        date(2026, 7, 16): ("898", "1275", "2170"),
        date(2026, 7, 17): ("902", "1280", "2190"),
        date(2026, 7, 18): ("910", "1285", "2210"),
    }
    history: dict[date, dict[str, MarketPrice]] = {}
    for price_date, (cord, pacif, aust) in values.items():
        as_of = datetime(price_date.year, price_date.month, price_date.day, 20, 0, tzinfo=UTC)
        history[price_date] = {
            "CORD-A.SN": MarketPrice("CORD-A.SN", Decimal(cord), as_of, "synthetic_fixture"),
            "PACIF.SN": MarketPrice("PACIF.SN", Decimal(pacif), as_of, "synthetic_fixture"),
            "AUST.SN": MarketPrice("AUST.SN", Decimal(aust), as_of, "synthetic_fixture"),
        }
    return history
