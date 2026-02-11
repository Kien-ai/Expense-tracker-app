from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(month, total, insights):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf)
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"<b>Expense Report – {month}</b>", styles["Title"]),
        Paragraph(f"Total spending: ${total:,.2f}", styles["Normal"]),
    ]

    for i in insights:
        content.append(Paragraph("- " + i, styles["Normal"]))

    doc.build(content)
    buf.seek(0)
    return buf
