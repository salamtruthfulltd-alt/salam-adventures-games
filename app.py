import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import fitz  # This is PyMuPDF
from docx import Document
import io

# --- 1. INITIAL SETUP ---
st.set_page_config(page_title="Salam Truthful Pro Studio", layout="wide")

# Standard Amazon KDP Sizes
KDP_TRIM_SIZES = {
    "8.5 x 8.5 (Square)": (8.5, 8.5),
    "8 x 10 (Classic Picture Book)": (8, 10),
    "6 x 9 (Standard Novel)": (6, 9),
    "8.25 x 11 (Standard Large)": (8.25, 11),
    "8.5 x 11 (Max Size)": (8.5, 11)
}

st.title("🎨 Pro KDP Converter & Editor")
st.write("Upload your book (PDF or Word) to format it for Amazon KDP.")

# --- 2. SIDEBAR SETTINGS ---
st.sidebar.header("Book Settings")
selected_label = st.sidebar.selectbox("Target Trim Size:", list(KDP_TRIM_SIZES.keys()))
base_w, base_h = KDP_TRIM_SIZES[selected_label]

# Automated Bleed Math (Amazon's 0.125" rule)
has_bleed = st.sidebar.checkbox("Apply Amazon Bleed (+0.125\")", value=True)
final_w = base_w + 0.125 if has_bleed else base_w
final_h = base_h + 0.25 if has_bleed else base_h

st.sidebar.info(f"Final Export: {final_w}\" x {final_h}\"")

# --- 3. THE CONVERSION ENGINE ---
uploaded_file = st.file_uploader("Upload Word Doc or PDF", type=["pdf", "docx"])

pages = []

if uploaded_file:
    # Handle PDF
    if uploaded_file.name.endswith(".pdf"):
        with st.spinner("Converting PDF pages..."):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for page in doc:
                pix = page.get_pixmap(dpi=150)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                pages.append(img)
    
    # Handle Word
    elif uploaded_file.name.endswith(".docx"):
        with st.spinner("Extracting images from Word..."):
            doc = Document(uploaded_file)
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    img = Image.open(io.BytesIO(rel.target_part.blob))
                    pages.append(img)
        if not pages:
            st.warning("No images found in Word doc. For text-heavy books, please save as PDF first.")

# --- 4. THE EDITING WINDOW ---
if pages:
    st.success(f"Loaded {len(pages)} pages successfully!")
    
    # Slider to navigate through the book
    page_idx = st.select_slider("Flip through your book:", options=range(len(pages)), format_func=lambda x: f"Page {x+1}")
    
    current_img = pages[page_idx]

    # Calculate Canvas Aspect Ratio
    canvas_width = 800
    canvas_height = int(canvas_width * (final_h / final_w))

    st.subheader(f"Editing Page {page_idx + 1}")
    
    # The Editor Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        background_image=current_img,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="rect",
        key=f"canvas_page_{page_idx}" # Unique key per page
    )

    st.markdown("---")
    st.write("### 📜 Final Verification")
    if st.checkbox("I have reviewed this layout for KDP compliance."):
        st.button("🚀 Download Amazon-Ready PDF")
        st.markdown(f"[Back to SalamTruthful.com](https://www.salamtruthful.com)")

else:
    st.info("Please upload a file to begin.")
