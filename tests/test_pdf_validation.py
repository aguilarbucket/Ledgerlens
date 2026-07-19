from pathlib import Path

import pytest

from ledgerlens.invoices.pdf_validation import PDFValidationError, validate_pdf
from sample_data.invoice_catalog import SYNTHETIC_INVOICES

VALID_PDF = b"%PDF-1.4\nsynthetic content\n%%EOF\n"


def test_accepts_pdf_signature_and_returns_hash() -> None:
    result = validate_pdf(
        filename="invoice.pdf", mime_type="application/pdf", content=VALID_PDF, max_size_mb=1
    )

    assert result.filename == "invoice.pdf"
    assert len(result.sha256) == 64
    assert result.content == VALID_PDF


@pytest.mark.parametrize(
    ("filename", "mime_type", "content", "message"),
    [
        ("invoice.txt", "application/pdf", VALID_PDF, ".pdf extension"),
        ("invoice.pdf", "text/plain", VALID_PDF, "MIME"),
        ("invoice.pdf", "application/pdf", b"not a pdf", "header"),
        ("invoice.pdf", "application/pdf", b"%PDF-1.4\nmissing eof", "end-of-file"),
    ],
)
def test_rejects_invalid_pdf(
    filename: str, mime_type: str, content: bytes, message: str
) -> None:
    with pytest.raises(PDFValidationError, match=message):
        validate_pdf(filename=filename, mime_type=mime_type, content=content, max_size_mb=1)


def test_rejects_oversized_pdf() -> None:
    with pytest.raises(PDFValidationError, match="exceeds"):
        validate_pdf(
            filename="invoice.pdf",
            mime_type="application/pdf",
            content=b"%PDF-" + (b"0" * 1024) + b"%%EOF",
            max_size_mb=0,
        )


@pytest.mark.parametrize("spec", SYNTHETIC_INVOICES)
def test_bundled_synthetic_invoices_are_valid_pdfs(spec) -> None:
    path = Path("output/pdf") / spec.filename
    result = validate_pdf(
        filename=path.name,
        mime_type="application/pdf",
        content=path.read_bytes(),
        max_size_mb=1,
    )

    assert result.size_bytes > 1_000
    assert result.sha256
