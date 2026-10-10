
from pathlib import Path
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#142B4A")
GOLD = colors.HexColor("#C49A45")
LIGHT_GOLD = colors.HexColor("#E8D7AE")
TEXT = colors.HexColor("#333D4B")
MUTED = colors.HexColor("#657184")


def generate_certificate(recipient_id, name, title):
    file_path = OUTPUT_DIR / f"certificate_{recipient_id}.pdf"

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=landscape(A4)
    )

    width, height = landscape(A4)
    center = width / 2

    # White background
    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Outer and inner decorative borders
    pdf.setStrokeColor(NAVY)
    pdf.setLineWidth(4)
    pdf.rect(24, 24, width - 48, height - 48)

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(1.5)
    pdf.rect(33, 33, width - 66, height - 66)

    # Decorative corner accents
    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    corner = 22
    inset = 43

    for x, direction in [(inset, 1), (width - inset, -1)]:
        for y, vertical in [(inset, 1), (height - inset, -1)]:
            pdf.line(x, y, x + corner * direction, y)
            pdf.line(x, y, x, y + corner * vertical)

    # Top label
    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(center, height - 78, "CERTIFICATE OF COMPLETION")

    # Main heading
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        center, height - 125, "CERTIFICATE"
    )

    pdf.setStrokeColor(GOLD)
    pdf.setLineWidth(2)
    pdf.line(center - 105, height - 143, center + 105, height - 143)

    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        center, height - 180,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 27)
    pdf.drawCentredString(
        center, height - 226, name
    )

    # Gold underline beneath recipient name
    pdf.setStrokeColor(LIGHT_GOLD)
    pdf.setLineWidth(1.5)
    pdf.line(center - 130, height - 240, center + 130, height - 240)

    # Course title
    pdf.setFillColor(TEXT)
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        center, height - 278,
        "For successfully completing"
    )

    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(
        center, height - 307, title
    )

    # Completion date
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        center, 91, f"Issued on {date.today().strftime('%d %B %Y')}"
    )

    # Footer separator
    pdf.setStrokeColor(LIGHT_GOLD)
    pdf.setLineWidth(1)
    pdf.line(center - 90, 77, center + 90, 77)

    # Certificate identifier
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(
        center, 59, f"CERTIFICATE ID: {recipient_id}"
    )

    pdf.save()
    return str(file_path)
