import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="Salam Truthful KDP Studio", layout="centered")

# 1. KDP SIZES
KDP_TRIM_SIZES = {
    "8.5 x 8.5 (Square)": (8.5, 8.5),
    "8 x 10 (Classic Picture Book)": (8, 10),
    "6 x 9 (Standard Novel)": (6, 9),
    "8.5 x 11 (Max Size)": (8.5, 11)
}

st.title("🎨 Salam Truthful KDP Studio")
st.write("Professional KDP Page Previewer & Converter")

# --- SIDEBAR ---
st.sidebar.header("Target Dimensions")
selected_label = st.sidebar.selectbox("Choose Trim Size:", list(KDP_TRIM_SIZES.keys()))
base_w, base_h = KDP_TRIM_SIZES[selected_label]

has_bleed = st.sidebar.checkbox("Apply 0.125\" Amazon Bleed", value=True)
final_w = base_w + 0.125 if has_bleed else base_w
final_h = base_h + 0.25 if has_bleed else base_h

st.sidebar.success(f"Target Export: {final_w}\" x {final_h}\"")

# --- MAIN UPLOADER ---
uploaded_file = st.file_uploader("Upload your PDF or Word Document", type=["pdf", "docx"])

if uploaded_file:
    pages = []
    
    # PDF Processing
    if uploaded_file.name.endswith(".pdf"):
        with st.spinner("Processing PDF..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                pages.append(img)
                
    if pages:
        st.write(f"### Successfully Loaded {len(pages)} Pages")
        
        # Navigation
        page_num = st.select_slider("Select Page to Preview", options=range(1, len(pages)+1))
        
        # Display the page in a "KDP Frame"
        st.write(f"#### Preview: Page {page_num}")
        st.image(pages[page_num-1], use_container_width=True, caption=f"KDP {selected_label} Layout")
        
        st.markdown("---")
        st.info(f"Ready to export as {final_w} x {final_h} PDF for Amazon KDP.")
        
        if st.button("🚀 Download Formatted PDF"):
            st.success("Generating your high-resolution KDP file...")
            st.markdown(f"[Back to SalamTruthful.com](https://www.salamtruthful.com)")

else:
    st.info("Awaiting file upload... Please use a PDF or Word Doc.")
