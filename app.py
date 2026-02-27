import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Salam Truthful - KDP Fixer")

st.title("🛡️ KDP Safe-Zone Fixer")
st.write("Ensuring your art stays away from the 'Cut Line'.")

# 1. Dimensions
size_choice = st.selectbox("Select Trim Size", ["8.5 x 8.5", "8 x 10", "6 x 9", "8.5 x 11"])
w_in, h_in = [float(x) for x in size_choice.split(" x ")]

# KDP Math: 72 points per inch. We add 0.125" bleed.
final_w = (w_in + 0.125) * 72
final_h = (h_in + 0.25) * 72

up = st.file_uploader("Upload your PDF", type="pdf")

if up:
    try:
        out_pdf = fitz.open()
        in_pdf = fitz.open(stream=up.read(), filetype="pdf")
        
        # SAFE ZONE MATH: We keep the art 0.375" away from the edge.
        # This prevents the "Cutoff" you are experiencing.
        margin = 27 
        safe_rect = fitz.Rect(margin, margin, final_w - margin, final_h - margin)

        for page in in_pdf:
            pix = page.get_pixmap(dpi=150)
            img_data = pix.tobytes("png")
            
            new_page = out_pdf.new_page(width=final_w, height=final_h)
            # Insert image INTO the safe zone so it doesn't touch the edges
            new_page.insert_image(safe_rect, stream=img_data, keep_proportion=True)

        st.success("Art protected! It is now centered away from the blade.")
        st.download_button("📥 Download KDP PDF", out_pdf.tobytes(), "KDP_Safe_Book.pdf")
        
    except Exception as e:
        st.error("Please refresh and try again with a smaller file.")
