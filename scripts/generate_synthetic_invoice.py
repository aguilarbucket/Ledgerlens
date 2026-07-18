from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

OUTPUT_PATH = Path("output/pdf/ledgerlens_synthetic_invoice.pdf")


def generate_invoice(output_path: Path = OUTPUT_PATH) -> Path:
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
        title="Synthetic Brokerage Invoice - LedgerLens",
        author="LedgerLens Build Week Demo",
    )

    story = [
        Paragraph("CORREDORA DEMO", title),
        Paragraph("Synthetic brokerage purchase invoice", styles["Heading2"]),
        Spacer(1, 5 * mm),
    ]
    meta = Table(
        [
            ["Document reference", Paragraph("SYNTH-BW-2026-005", right)],
            ["Trade date", Paragraph("2026-07-18", right)],
            ["Settlement currency", Paragraph("CLP", right)],
            ["Client", Paragraph("Demo Investor 001", right)],
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
            ["Cordillera Energía", "CORD-A.SN", "150", "$920 CLP", "$138.000 CLP"],
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
            Paragraph("Total purchase: <b>$138.000 CLP</b>", right),
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


if __name__ == "__main__":
    generated = generate_invoice()
    reader = PdfReader(str(generated))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    required = {"SYNTH-BW-2026-005", "CORD-A.SN", "150", "920", "CLP", "SYNTHETIC DOCUMENT"}
    missing = sorted(value for value in required if value not in text)
    if missing:
        raise RuntimeError(f"Generated PDF is missing required synthetic fields: {missing}")
    print(f"Generated and verified {generated} ({len(reader.pages)} page)")
