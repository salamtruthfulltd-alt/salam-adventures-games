import streamlit as st
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

st.set_page_config(page_title="PictureBook Engine", layout="wide")

st.title("📘 PictureBook Engine v1.0")
st.write("Convert your manuscript into a KDP-ready print file.")

# --- SIDEBAR OPTIONS (The Layout Settings) ---
st.sidebar.header("1. Choose Trim Size")
size_choice = st.sidebar.selectbox(
    "Select Size", 
    ["8.5 x 8.5", "6 x 9", "8.5 x 11", "5.5 x 8.5"]
)

st.sidebar.header("2. Formatting")
bleed = st.sidebar.checkbox("Add KDP Bleed (0.125\")", value=True)
font_size = st.sidebar.slider("Font Size", 10, 24, 14)

# Math for Sizing
dims = {"8.5 x 8.5": (8.5, 8.5), "6 x 9": (6, 9), "8.5 x 11": (8.5, 11), "5.5 x 8.5": (5.5, 8.5)}
base_w, base_h = dims[size_choice]

if bleed:
    final_w, final_h = (base_w + 0.125), (base_h + 0.25)
else:
    final_w, final_h = base_w, base_h

# --- UPLOADER ---
uploaded_file = st.file_uploader("Upload your DOCX manuscript", type="docx")

if uploaded_file:
    st.success("File Uploaded!")
    
    if st.button("Generate My PDF"):
        doc = Document(uploaded_file)
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesizes=(final_w * inch, final_h * inch))
        
        page_count = 0
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                # Create a new page for every paragraph found
                c.setFont("Helvetica", font_size)
                
                # Draw text inside a safe margin
                text_obj = c.beginText(0.75 * inch, (final_h - 1) * inch)
                text_obj.textLines(text)
                c.drawText(text_obj)
                
                c.showPage()
                page_count += 1
        
        if page_count > 0:
            c.save()
            pdf_buffer.seek(0)
            st.success(f"Successfully created {page_count} pages!")
            st.download_button(
                "Download KDP-Ready PDF",
                data=pdf_buffer,
                file_name=f"PictureBook_{size_choice.replace(' ','')}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("The document appears empty or only contains images. Try adding some text paragraphs first!")
