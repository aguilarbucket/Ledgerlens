from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True, slots=True)
class SyntheticInvoiceSpec:
    filename: str
    label: str
    platform: str
    company: str
    ticker: str
    quantity: int
    unit_price: int
    purchase_date: date
    document_reference: str
    currency: str = "CLP"
    client: str = "Demo Investor 001"

    @property
    def gross_amount(self) -> int:
        return self.quantity * self.unit_price


SYNTHETIC_INVOICES = (
    SyntheticInvoiceSpec(
        filename="ledgerlens_synthetic_invoice.pdf",
        label="Corredora Demo - Cordillera Energia",
        platform="Corredora Demo",
        company="Cordillera Energía",
        ticker="CORD-A.SN",
        quantity=150,
        unit_price=920,
        purchase_date=date(2026, 7, 18),
        document_reference="SYNTH-BW-2026-005",
    ),
    SyntheticInvoiceSpec(
        filename="ledgerlens_synthetic_invoice_pacifico_valores.pdf",
        label="Pacifico Valores Demo - Pacifico Retail",
        platform="Pacífico Valores Demo",
        company="Pacífico Retail",
        ticker="PACIF.SN",
        quantity=75,
        unit_price=1320,
        purchase_date=date(2026, 6, 24),
        document_reference="SYNTH-BW-2026-006",
    ),
    SyntheticInvoiceSpec(
        filename="ledgerlens_synthetic_invoice_austral_corredores.pdf",
        label="Austral Corredores Demo - Austral Telecom",
        platform="Austral Corredores Demo",
        company="Austral Telecom",
        ticker="AUST.SN",
        quantity=40,
        unit_price=2140,
        purchase_date=date(2026, 7, 17),
        document_reference="SYNTH-BW-2026-007",
    ),
    SyntheticInvoiceSpec(
        filename="ledgerlens_synthetic_invoice_mercado_norte.pdf",
        label="Mercado Norte Demo - Bosques del Sur",
        platform="Mercado Norte Demo",
        company="Bosques del Sur",
        ticker="BOSQ.SN",
        quantity=90,
        unit_price=760,
        purchase_date=date(2026, 7, 12),
        document_reference="SYNTH-BW-2026-008",
    ),
    SyntheticInvoiceSpec(
        filename="ledgerlens_synthetic_invoice_valle_inversiones.pdf",
        label="Valle Inversiones Demo - Litoral Logistica",
        platform="Valle Inversiones Demo",
        company="Litoral Logística",
        ticker="LITOR.SN",
        quantity=55,
        unit_price=1860,
        purchase_date=date(2026, 7, 18),
        document_reference="SYNTH-BW-2026-009",
    ),
)

DEFAULT_SYNTHETIC_INVOICE = SYNTHETIC_INVOICES[0]


def invoice_spec_for_filename(filename: str) -> SyntheticInvoiceSpec | None:
    safe_name = Path(filename).name.casefold()
    return next(
        (spec for spec in SYNTHETIC_INVOICES if spec.filename.casefold() == safe_name),
        None,
    )
