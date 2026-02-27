import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from docx import Document
import io
import gc  # Garbage Collector to prevent memory crashes

st.set_page_config(page_title="KDP Auto-Fixer", layout="centered")

KDP_TRIM_SIZES = {
    "8.5 x 8.5": (8.5, 8.5),
    "8 x 10": (8, 10),
    "6 x 9": (6, 9),
    "8.5 x 11": (8.5, 11)
}

st.title("🛡️ KDP Professional Auto-Fixer")

# Sidebar for Settings
selected_size = st.selectbox("Select Your Book's Trim Size:", list(KDP_TRIM_SIZES.keys()))
base_w, base_h = KDP_TRIM_SIZES[selected_size]

# Amazon KDP Bleed Math
final_w = base_w + 0.125
final_h = base_h + 0.25

uploaded_file = st.file_uploader("Upload PDF or Word Document", type=["pdf", "docx"])

if uploaded_file:
    output_pdf = fitz.open()
    
    try:
        if uploaded_file.name.endswith(".pdf"):
            with st.spinner("Processing PDF Pages..."):
                input_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in input_pdf:
                    # Reduced DPI slightly (200 instead of 300) to prevent memory crash
                    pix = page.get_pixmap(dpi=200) 
                    img_data = pix.tobytes("png")
                    
                    new_page = output_pdf.new_page(width=final_w*72, height=final_h*72)
                    rect = fitz.Rect(0, 0, final_w*72, final_h*72)
                    new_page.insert_image(rect, stream=img_data)
                    
                    # Force memory cleanup
                    del pix
                    gc.collect()

        elif uploaded_file.name.endswith(".docx"):
            with st.spinner("Extracting Word Images..."):
                doc = Document(uploaded_file)
                for rel in doc.part.rels.values():
                    if "image" in rel.target_ref:
                        new_page = output_pdf.new_page(width=final_w*72, height=final_h*72)
                        rect = fitz.Rect(0, 0, final_w*72, final_h*72)
                        new_page.insert_image(rect, stream=rel.target_part.blob)
                        gc.collect()

        if len(output_pdf) > 0:
            st.success(f"Perfect! {len(output_pdf)} pages are ready for Amazon.")
            pdf_bytes = output_pdf.tobytes()
            st.download_button(
                label="📥 Download KDP-Ready PDF",
                data=pdf_bytes,
                file_name=f"KDP_Ready_{selected_size.replace(' ','')}.pdf",
                mime="application/pdf"
            )
    
    except Exception as e:
        st.error(f"The file was too large for the server. Try a smaller PDF or export your Word doc as a PDF first.")
    
    finally:
        output_pdf.close()
