import streamlit as st
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

st.set_page_config(page_title="PictureBook Engine", layout="centered")

st.title("📘 PictureBook Engine (MVP)")
st.write("Upload your DOCX manuscript to generate a KDP-compliant PDF.")

# Sidebar for settings
st.sidebar.header("Book Settings")
trim_size = st.sidebar.selectbox("Trim Size", ["8.5 x 8.5", "6 x 9", "8.5 x 11"])
bleed = st.sidebar.checkbox("Apply KDP Bleed (0.125\")", value=True)

# Math for KDP
dims = {"8.5 x 8.5": (8.5, 8.5), "6 x 9": (6, 9), "8.5 x 11": (8.5, 11)}
w, h = dims[trim_size]
if bleed:
    w += 0.125
    h += 0.25

uploaded_file = st.file_uploader("Upload your DOCX file", type="docx")

if uploaded_file:
    if st.button("Generate Print-Ready PDF"):
        st.info("Rebuilding layout... please wait.")
        
        # This is the 'Engine' processing
        doc = Document(uploaded_file)
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesizes=(w * inch, h * inch))
        
        # Simple Logic: Each paragraph becomes a page (MVP version)
        for para in doc.paragraphs:
            if para.text.strip():
                c.setFont("Helvetica", 12)
                # Text Safe Zone Margins
                text_object = c.beginText(0.5 * inch, (h - 0.5) * inch)
                text_object.textLines(para.text)
                c.drawText(text_object)
                c.showPage()
        
        c.save()
        pdf_buffer.seek(0)
        
        st.success("🎉 Done!")
        st.download_button(
            label="Download KDP PDF",
            data=pdf_buffer,
            file_name="KDP_Print_Ready.pdf",
            mime="application/pdf"
        )
