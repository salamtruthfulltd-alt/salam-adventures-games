import streamlit as st
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

# --- APP INTERFACE ---
st.set_page_config(page_title="PictureBook Engine", page_icon="📘")
st.title("📘 PictureBook Engine (MVP)")
st.write("Upload your DOCX to generate a KDP-compliant PDF.")

# Sidebar Settings
st.sidebar.header("Book Settings")
size_choice = st.sidebar.selectbox("Trim Size", ["8.5 x 8.5", "6 x 9", "8.5 x 11"])
bleed = st.sidebar.checkbox("Apply KDP Bleed (0.125\")", value=True)

# Math for Sizes
dims = {"8.5 x 8.5": (8.5, 8.5), "6 x 9": (6, 9), "8.5 x 11": (8.5, 11)}
base_w, base_h = dims[size_choice]

if bleed:
    final_w = base_w + 0.125
    final_h = base_h + 0.25
else:
    final_w, final_h = base_w, base_h

# --- UPLOAD LOGIC ---
uploaded_file = st.file_uploader("Choose your DOCX manuscript", type="docx")

if uploaded_file:
    if st.button("Generate KDP PDF"):
        # Process DOCX
        doc = Document(uploaded_file)
        pdf_buffer = io.BytesIO()
        
        # Create PDF
        c = canvas.Canvas(pdf_buffer, pagesizes=(final_w * inch, final_h * inch))
        
        # Simple Loop through paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                # Draw Text Page
                c.setFont("Helvetica", 12)
                c.drawString(1 * inch, (final_h - 1) * inch, para.text[:100] + "...")
                c.showPage()
        
        c.save()
        pdf_buffer.seek(0)
        
        st.success("🎉 Book Rebuilt Successfully!")
        st.download_button(
            label="Download Print-Ready PDF",
            data=pdf_buffer,
            file_name="KDP_Ready_Book.pdf",
            mime="application/pdf"
        )
