from __future__ import annotations

from typing import Protocol

from ledgerlens.ai.openai_client import OpenAIResponsesClient
from ledgerlens.invoices.models import FieldConfidence, InvoiceExtraction
from ledgerlens.invoices.pdf_validation import ValidatedPDF

INVOICE_EXTRACTION_INSTRUCTIONS = """
Extract only the purchase fields represented by the response schema from this brokerage invoice.
Do not calculate, infer, repair, or silently normalize monetary values. Use CLP only when the
document explicitly supports it. Report uncertainty through per-field confidence and warnings.
This extraction is a draft: a human, not the model, decides what is saved.
""".strip()


class InvoiceExtractor(Protocol):
    source_name: str

    def extract(self, pdf: ValidatedPDF) -> InvoiceExtraction: ...


class FixtureInvoiceExtractor:
    source_name = "synthetic_fixture"

    def extract(self, pdf: ValidatedPDF) -> InvoiceExtraction:
        return InvoiceExtraction(
            company="Cordillera Energía",
            ticker="CORD-A.SN",
            quantity="150",
            unit_price="920",
            purchase_date="2026-07-18",
            platform="Corredora Demo",
            currency="CLP",
            document_reference="SYNTH-BW-2026-005",
            confidence=FieldConfidence(
                company=0.99,
                ticker=0.99,
                quantity=0.99,
                unit_price=0.99,
                purchase_date=0.99,
                platform=0.99,
                currency=0.99,
                document_reference=0.99,
            ),
            warnings=["Offline demo extraction; no OpenAI request was made."],
        )


class OpenAIInvoiceExtractor:
    source_name = "openai_responses_api"

    def __init__(self, client: OpenAIResponsesClient) -> None:
        self._client = client

    def extract(self, pdf: ValidatedPDF) -> InvoiceExtraction:
        result = self._client.parse_pdf(
            pdf=pdf,
            instructions=INVOICE_EXTRACTION_INSTRUCTIONS,
            response_model=InvoiceExtraction,
        )
        return InvoiceExtraction.model_validate(result)

