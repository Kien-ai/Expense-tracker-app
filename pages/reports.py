import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

st.header("📄 Reports & Export")

# -----------------------------
# Check data
# -----------------------------
if 'df' not in st.session_state or st.session_state['df'].empty:
    st.warning("No data available. Please upload or add expenses first.")
    st.stop()

df = st.session_state['df'].copy()

# -----------------------------
# Download CSV
# -----------------------------
st.subheader("💾 Download CSV")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", data=csv, file_name="expenses_report.csv", mime="text/csv")

# -----------------------------
# Download PDF
# -----------------------------
st.subheader("📄 Download PDF Report")

def create_pdf_bytes(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Expense Report", ln=True, align="C")
    pdf.ln(10)
    
    # Table header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 8, "Date", 1)
    pdf.cell(60, 8, "Category", 1)
    pdf.cell(60, 8, "Amount ($)", 1)
    pdf.ln()
    
    pdf.set_font("Arial", '', 12)
    for idx, row in df.iterrows():
        pdf.cell(60, 8, str(row['Date'].date()), 1)
        pdf.cell(60, 8, str(row['Category']), 1)
        pdf.cell(60, 8, f"{row['Amount']:.2f}", 1)
        pdf.ln()
    
    # Get PDF content as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

pdf_bytes = create_pdf_bytes(df)
st.download_button(
    "Download PDF",
    data=pdf_bytes,
    file_name="expenses_report.pdf",
    mime="application/pdf"
)
