from __future__ import annotations

from typing import Protocol

from ledgerlens.ai.openai_client import OpenAIResponsesClient
from ledgerlens.invoices.models import FieldConfidence, InvoiceExtraction
from ledgerlens.invoices.pdf_validation import ValidatedPDF
from sample_data.invoice_catalog import invoice_spec_for_filename

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
        spec = invoice_spec_for_filename(pdf.filename)
        if spec is None:
            raise ValueError(
                "Offline fixture extraction supports only the five bundled synthetic invoice "
                "filenames. Use a bundled sample or select OpenAI Responses API."
            )
        return InvoiceExtraction(
            company=spec.company,
            ticker=spec.ticker,
            quantity=spec.quantity,
            unit_price=spec.unit_price,
            purchase_date=spec.purchase_date,
            platform=spec.platform,
            currency="CLP",
            document_reference=spec.document_reference,
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
            warnings=[
                f"Offline demo extraction for {spec.platform}; no OpenAI request was made."
            ],
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
