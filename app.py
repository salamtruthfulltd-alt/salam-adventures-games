import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import gc

st.set_page_config(page_title="Salam Truthful - Smart Fixer", layout="centered")

KDP_TRIM_SIZES = {
    "8.5 x 8.5": (8.5, 8.5),
    "8 x 10": (8, 10),
    "6 x 9": (6, 9),
    "8.5 x 11": (8.5, 11)
}

st.title("🎨 KDP Smart-Fit Studio")
st.subheader("Preventing "Cut-off" Art")

selected_size = st.selectbox("Your Amazon Trim Size:", list(KDP_TRIM_SIZES.keys()))
base_w, base_h = KDP_TRIM_SIZES[selected_size]

# KDP Math (points: 72 per inch)
# We calculate the "Safe Zone" vs the "Bleed Zone"
bleed = 0.125
final_w_pts = (base_w + bleed) * 72
final_h_pts = (base_h + (bleed * 2)) * 72
safe_rect = fitz.Rect(bleed*72, bleed*72, (base_w)*72, (base_h+bleed)*72)

uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg"])

if uploaded_file:
    output_pdf = fitz.open()
    
    if uploaded_file.name.endswith(".pdf"):
        in_pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in in_pdf:
            pix = page.get_pixmap(dpi=200)
            img_data = pix.tobytes("png")
            
            new_page = output_pdf.new_page(width=final_w_pts, height=final_h_pts)
            
            # THE SMART FIX: 
            # This "shrink-wraps" your image into the SAFE ZONE 
            # so the edges don't get cut off.
            new_page.insert_image(safe_rect, stream=img_data, keep_proportion=True)
            
            del pix
            gc.collect()

    st.success("Pages centered in Safe Zone. Edges are now protected!")
    
    # Download
    st.download_button("📥 Download Protected PDF", output_pdf.tobytes(), "KDP_Safe_Book.pdf")
