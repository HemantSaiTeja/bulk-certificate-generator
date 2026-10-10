
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_certificate(recipient_id, name, title):
    file_path = OUTPUT_DIR / f"certificate_{recipient_id}.pdf"

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=landscape(A4)
    )

    width, height = landscape(A4)

    # Certificate border
    pdf.setStrokeColor(colors.darkblue)
    pdf.setLineWidth(3)
    pdf.rect(25, 25, width - 50, height - 50)

    # Certificate content
    pdf.setFillColor(colors.darkblue)
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 120,
        "CERTIFICATE OF ACHIEVEMENT"
    )

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 190,
        "This certificate is proudly presented to"
    )

    pdf.setFillColor(colors.darkred)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawCentredString(
        width / 2,
        height - 245,
        name
    )

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        width / 2,
        height - 295,
        f"For successfully completing: {title}"
    )

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        width / 2,
        75,
        f"Certificate ID: {recipient_id}"
    )

    pdf.save()

    return str(file_path)
