import streamlit as st
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from PIL import Image

# 1. SEARCH ENGINE OPTIMIZATION (SEO)
st.set_page_config(
    page_title="Fix KDP Books | Word to KDP Picture Book Converter",
    page_icon="📚",
    layout="wide"
)

# Custom Styling for the viewing window
st.markdown("""
    <style>
    .stImage {border: 2px solid #f0f2f6; border-radius: 10px;}
    .page-box {background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Fix KDP Books: Studio Edition")
st.subheader("The easiest way to convert Word layouts into KDP-ready PDFs")

# 2. SESSION STATE (The app's "Memory")
if 'layout_order' not in st.session_state:
    st.session_state.layout_order = []

# 3. SIDEBAR: KDP COMPLIANCE
st.sidebar.header("📐 KDP Print Settings")
size_choice = st.sidebar.selectbox("Trim Size", ["8.5 x 8.5", "6 x 9", "8.5 x 11"])
bleed = st.sidebar.checkbox("Add KDP Bleed (Recommended)", value=True)

# Calculate dimensions
dims = {"8.5 x 8.5": (8.5, 8.5), "6 x 9": (6, 9), "8.5 x 11": (8.5, 11)}
w, h = dims[size_choice]
if bleed:
    w += 0.125
    h += 0.25

# 4. FILE UPLOADER
uploaded_file = st.file_uploader("Upload your DOCX manuscript (like Luna and the Feather Forest)", type="docx")

if uploaded_file and not st.session_state.layout_order:
    with st.spinner("Scanning manuscript layers..."):
        doc = Document(uploaded_file)
        
        # Extract Images (Backgrounds)
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                st.session_state.layout_order.append({
                    "type": "image", 
                    "content": rel.target_part.blob,
                    "name": "Background Artwork"
                })
        
        # Extract Text (Story Layers)
        for p in doc.paragraphs:
            if p.text.strip():
                st.session_state.layout_order.append({
                    "type": "text", 
                    "content": p.text.strip(),
                    "name": "Story Text"
                })

# 5. THE VIEWING & EDITING STUDIO
if st.session_state.layout_order:
    st.write("---")
    st.header("🖼️ Page Layout Window")
    st.write("Review the order of your pages. Use the arrows to move content or the X to delete.")

    for i, item in enumerate(st.session_state.layout_order):
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col1:
                st.write(f"**Item {i+1}**")
                if st.button("⬆️", key=f"up_{i}") and i > 0:
                    st.session_state.layout_order[i], st.session_state.layout_order[i-1] = st.session_state.layout_order[i-1], st.session_state.layout_order[i]
                    st.rerun()
                if st.button("⬇️", key=f"down_{i}") and i < len(st.session_state.layout_order)-1:
                    st.session_state.layout_order[i], st.session_state.layout_order[i+1] = st.session_state.layout_order[i+1], st.session_state.layout_order[i]
                    st.rerun()

            with col2:
                if item["type"] == "image":
                    st.image(item["content"], caption=f"Detected Image {i+1}", width=300)
                else:
                    st.info(f"📜 **Text Layer:** {item['content']}")

            with col3:
                if st.button("❌", key=f"del_{i}", help="Delete this layer"):
                    st.session_state.layout_order.pop(i)
                    st.rerun()

    # 6. PDF GENERATOR
    st.write("---")
    if st.button("🚀 FINISHED: Generate KDP-Ready PDF", use_container_width=True):
        output = io.BytesIO()
        pdf_canvas = canvas.Canvas(output, pagesizes=(w * inch, h * inch))
        
        for item in st.session_state.layout_order:
            if item["type"] == "image":
                img_data = Image.open(io.BytesIO(item["content"]))
                pdf_canvas.drawInlineImage(img_data, 0, 0, width=w*inch, height=h*inch)
                pdf_canvas.showPage()
            else:
                # Basic text placement if text is separate
                pdf_canvas.setFont("Helvetica-Bold", 14)
                pdf_canvas.drawCentredString((w/2)*inch, (h/2)*inch, item["content"])
                pdf_canvas.showPage()
        
        pdf_canvas.save()
        output.seek(0)
        
        st.balloons()
        st.success("Your KDP-compliant PDF is ready!")
        st.download_button(
            label="📥 Download Now",
            data=output,
            file_name=f"KDP_Final_{size_choice.replace(' ','')}.pdf",
            mime="application/pdf"
        )
else:
    if uploaded_file:
        st.warning("We found the file, but no images or text were detected. Try a different DOCX format.")
