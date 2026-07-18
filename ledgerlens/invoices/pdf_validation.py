from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

PDF_MIME_TYPES = {"application/pdf", "application/x-pdf", "application/octet-stream"}


class PDFValidationError(ValueError):
    """Raised when an uploaded document is not an acceptable PDF."""


@dataclass(frozen=True, slots=True)
class ValidatedPDF:
    filename: str
    mime_type: str
    content: bytes
    size_bytes: int
    sha256: str


def validate_pdf(
    *, filename: str, mime_type: str | None, content: bytes, max_size_mb: int = 10
) -> ValidatedPDF:
    safe_filename = Path(filename).name
    if not safe_filename or Path(safe_filename).suffix.lower() != ".pdf":
        raise PDFValidationError("The uploaded file must use the .pdf extension.")
    if mime_type and mime_type.lower() not in PDF_MIME_TYPES:
        raise PDFValidationError("The uploaded file does not report a PDF MIME type.")
    if not content:
        raise PDFValidationError("The uploaded PDF is empty.")
    if len(content) > max_size_mb * 1024 * 1024:
        raise PDFValidationError(f"The uploaded PDF exceeds the {max_size_mb} MB limit.")
    if not content.startswith(b"%PDF-"):
        raise PDFValidationError("The file header is not a valid PDF signature.")
    if b"%%EOF" not in content[-2048:]:
        raise PDFValidationError("The PDF does not contain a valid end-of-file marker.")

    normalized_mime = mime_type.lower() if mime_type else "application/pdf"
    return ValidatedPDF(
        filename=safe_filename,
        mime_type=normalized_mime,
        content=content,
        size_bytes=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
    )
