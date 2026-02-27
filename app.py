import streamlit as st
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from PIL import Image

st.set_page_config(page_title="PictureBook Studio", layout="wide")

st.title("🎨 PictureBook Layout Studio")

# Initialize "Session State" to remember your layout changes
if 'layout_order' not in st.session_state:
    st.session_state.layout_order = []

# --- SIDEBAR: KDP SETTINGS ---
st.sidebar.header("KDP Settings")
size_choice = st.sidebar.selectbox("Trim Size", ["8.5 x 8.5", "6 x 9", "8.5 x 11"])
bleed = st.sidebar.checkbox("Apply KDP Bleed", value=True)

# Math for PDF
dims = {"8.5 x 8.5": (8.5, 8.5), "6 x 9": (6, 9), "8.5 x 11": (8.5, 11)}
w, h = dims[size_choice]
if bleed: w += 0.125; h += 0.25

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload your DOCX", type="docx")

if uploaded_file and not st.session_state.layout_order:
    doc = Document(uploaded_file)
    # Extract images and text into a list we can move
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            st.session_state.layout_order.append({"type": "image", "content": rel.target_part.blob})
    for p in doc.paragraphs:
        if p.text.strip():
            st.session_state.layout_order.append({"type": "text", "content": p.text.strip()})

# --- THE VIEWING & EDITING WINDOW ---
if st.session_state.layout_order:
    st.subheader("🖼️ Layout Editor")
    st.write("Rearrange your pages before generating the PDF.")

    for i, item in enumerate(st.session_state.layout_order):
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col1:
            st.write(f"**Page {i+1}**")
            if st.button("⬆️", key=f"up_{i}") and i > 0:
                st.session_state.layout_order[i], st.session_state.layout_order[i-1] = st.session_state.layout_order[i-1], st.session_state.layout_order[i]
                st.rerun()
            if st.button("⬇️", key=f"down_{i}") and i < len(st.session_state.layout_order)-1:
                st.session_state.layout_order[i], st.session_state.layout_order[i+1] = st.session_state.layout_order[i+1], st.session_state.layout_order[i]
                st.rerun()

        with col2:
            if item["type"] == "image":
                st.image(item["content"], width=200)
            else:
                st.info(item["content"])

        with col3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.layout_order.pop(i)
                st.rerun()

    # --- FINAL EXPORT ---
    if st.button("🚀 Generate Final KDP PDF"):
        output = io.BytesIO()
        c = canvas.Canvas(output, pagesizes=(w * inch, h * inch))
        
        for item in st.session_state.layout_order:
            if item["type"] == "image":
                img = Image.open(io.BytesIO(item["content"]))
                c.drawInlineImage(img, 0, 0, width=w*inch, height=h*inch)
            else:
                c.setFont("Helvetica-Bold", 14)
                c.drawCentredString((w/2)*inch, 1*inch, item["content"])
            c.showPage()
        
        c.save()
        output.seek(0)
        st.download_button("Download Book", output, "My_Layout.pdf")
