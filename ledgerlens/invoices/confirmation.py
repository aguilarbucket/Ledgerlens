from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from ledgerlens.domain.models import Purchase
from ledgerlens.invoices.models import InvoiceExtraction


class ConfirmationRequiredError(ValueError):
    """Raised when an extraction is saved without explicit human review."""


def confirm_extraction(
    extraction: InvoiceExtraction,
    *,
    reviewed_and_confirmed: bool,
    document_sha256: str,
    source: str,
) -> Purchase:
    if not reviewed_and_confirmed:
        raise ConfirmationRequiredError("Human review and confirmation are required before saving.")
    if len(document_sha256) != 64:
        raise ValueError("A valid document SHA-256 is required for traceability.")

    return Purchase(
        id=str(uuid4()),
        company=extraction.company,
        ticker=extraction.ticker,
        quantity=Decimal(extraction.quantity),
        unit_price_clp=Decimal(extraction.unit_price),
        purchase_date=extraction.purchase_date,
        platform=extraction.platform,
        currency=extraction.currency,
        document_reference=extraction.document_reference,
        document_sha256=document_sha256,
        source=source,
        confirmed_at=datetime.now(UTC),
    )
