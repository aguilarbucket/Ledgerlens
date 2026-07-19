from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from sample_data.invoice_catalog import (
    DEFAULT_SYNTHETIC_INVOICE,
    SYNTHETIC_INVOICES,
    SyntheticInvoiceSpec,
)

OUTPUT_DIRECTORY = Path("output/pdf")
OUTPUT_PATH = OUTPUT_DIRECTORY / DEFAULT_SYNTHETIC_INVOICE.filename


def _clp(value: int) -> str:
    return f"${value:,}".replace(",", ".") + " CLP"


def generate_invoice(
    spec: SyntheticInvoiceSpec = DEFAULT_SYNTHETIC_INVOICE,
    output_path: Path | None = None,
) -> Path:
    output_path = output_path or OUTPUT_DIRECTORY / spec.filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "InvoiceTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#102A43"),
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    right = ParagraphStyle("Right", parent=styles["BodyText"], alignment=TA_RIGHT)
    small = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#52606D"),
    )

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"Synthetic Brokerage Invoice - {spec.platform}",
        author="LedgerLens Build Week Demo",
    )

    story = [
        Paragraph(spec.platform.upper(), title),
        Paragraph("Synthetic brokerage purchase invoice", styles["Heading2"]),
        Spacer(1, 5 * mm),
    ]
    meta = Table(
        [
            ["Document reference", Paragraph(spec.document_reference, right)],
            ["Trade date", Paragraph(spec.purchase_date.isoformat(), right)],
            ["Settlement currency", Paragraph(spec.currency, right)],
            ["Client", Paragraph(spec.client, right)],
        ],
        colWidths=[65 * mm, 80 * mm],
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2F8")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9FB3C8")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BCCCDC")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.extend([meta, Spacer(1, 8 * mm), Paragraph("Purchase detail", styles["Heading2"])])

    detail = Table(
        [
            ["Company", "Ticker", "Quantity", "Unit price", "Gross amount"],
            [
                spec.company,
                spec.ticker,
                str(spec.quantity),
                _clp(spec.unit_price),
                _clp(spec.gross_amount),
            ],
        ],
        colWidths=[45 * mm, 28 * mm, 24 * mm, 30 * mm, 34 * mm],
    )
    detail.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102A43")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#9FB3C8")),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#BCCCDC")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.extend(
        [
            detail,
            Spacer(1, 12 * mm),
            Paragraph(f"Total purchase: <b>{_clp(spec.gross_amount)}</b>", right),
            Spacer(1, 18 * mm),
            Paragraph(
                "SYNTHETIC DOCUMENT - Generated exclusively for LedgerLens Build Week "
                "demonstration and automated tests. It does not represent a real broker, "
                "company, account, transaction, or financial instrument.",
                small,
            ),
            Spacer(1, 4 * mm),
            Paragraph(
                "This document is not financial advice and has no commercial or tax validity.",
                small,
            ),
        ]
    )
    document.build(story)
    return output_path


def generate_all_invoices() -> list[Path]:
    return [generate_invoice(spec) for spec in SYNTHETIC_INVOICES]


if __name__ == "__main__":
    for spec, generated in zip(SYNTHETIC_INVOICES, generate_all_invoices(), strict=True):
        reader = PdfReader(str(generated))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        normalized_text = text.replace(".", "").replace(",", "")
        required_text = {
            spec.platform.upper(),
            spec.document_reference,
            spec.ticker,
            spec.currency,
            "SYNTHETIC DOCUMENT",
        }
        required_numbers = {str(spec.quantity), str(spec.unit_price)}
        missing = sorted(value for value in required_text if value not in text)
        missing.extend(
            sorted(value for value in required_numbers if value not in normalized_text)
        )
        if missing:
            raise RuntimeError(
                f"Generated PDF {generated} is missing required synthetic fields: {missing}"
            )
        if len(reader.pages) != 1:
            raise RuntimeError(f"Generated PDF {generated} must contain exactly one page.")
        print(f"Generated and verified {generated} ({len(reader.pages)} page)")
