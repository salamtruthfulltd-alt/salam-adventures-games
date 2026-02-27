import streamlit as st
from streamlit_drawable_canvas_fix import st_canvas
from PIL import Image
import fitz  # PyMuPDF
from docx import Document
import io

st.set_page_config(page_title="Salam Truthful Pro Studio", layout="wide")

# 1. KDP SIZES
KDP_TRIM_SIZES = {
    "8.5 x 8.5 (Square)": (8.5, 8.5),
    "8 x 10 (Classic Picture Book)": (8, 10),
    "6 x 9 (Standard Novel)": (6, 9),
    "8.5 x 11 (Max Size)": (8.5, 11)
}

st.title("🎨 Pro KDP Converter & Editor")
st.write("Convert Word or PDF into Amazon-ready formats.")

# --- SIDEBAR ---
selected_label = st.sidebar.selectbox("Target KDP Trim Size:", list(KDP_TRIM_SIZES.keys()))
base_w, base_h = KDP_TRIM_SIZES[selected_label]
has_bleed = st.sidebar.checkbox("Apply 0.125\" Bleed", value=True)

final_w = base_w + 0.125 if has_bleed else base_w
final_h = base_h + 0.25 if has_bleed else base_h

# --- FILE UPLOADER (DOCX & PDF) ---
uploaded_file = st.file_uploader("Upload Word Doc or PDF", type=["pdf", "docx"])

if uploaded_file:
    pages = []

    # A. HANDLE PDF
    if uploaded_file.type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            pix = page.get_pixmap(dpi=150) # Convert to image
            img_data = pix.tobytes("png")
            pages.append(Image.open(io.BytesIO(img_data)))
    
    # B. HANDLE WORD (DOCX)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        # Note: In Word, we extract images. For text pages, we recommend converting Word to PDF first.
        st.warning("Word Support: Currently extracting images. For full layout editing, save your Word doc as PDF first.")
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                pages.append(Image.open(io.BytesIO(rel.target_part.blob)))

    # --- THE EDITING WINDOW ---
    if pages:
        st.write(f"### Detected {len(pages)} Pages. Adjust them below:")
        
        # Page Selector
        page_num = st.slider("Select Page to Edit", 1, len(pages), 1)
        current_img = pages[page_num - 1]

        # Canvas Setup
        canvas_width = 700 
        canvas_height = int(canvas_width * (final_h / final_w))

        st.info(f"Editing Page {page_num} of {len(pages)}")
        
        canvas_result = st_canvas(
            background_image=current_img,
            height=canvas_height,
            width=canvas_width,
            drawing_mode="rect",
            key=f"canvas_p{page_num}_{selected_label}"
        )

        # --- EXPORT SECTION ---
        st.markdown("---")
        if st.button("Generate Final KDP PDF"):
            st.success(f"Creating a {final_w}x{final_h} document... Please wait.")
            # PDF Compilation logic would go here
            st.markdown(f"[Go back to SalamTruthful.com](https://www.salamtruthful.com)")
