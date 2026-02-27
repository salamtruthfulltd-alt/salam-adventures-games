import streamlit as st
from docx import Document
from streamlit_drawable_canvas import st_canvas
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from PIL import Image, ImageDraw

# 1. SEO & KDP SETUP
st.set_page_config(page_title="Fix KDP Books | Professional Studio", layout="wide")

st.title("📚 Fix KDP Books: Professional Studio")
st.write("Layout your book with automated KDP compliance and safety guides.")

# 2. SESSION STATE
if 'pages' not in st.session_state:
    st.session_state.pages = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

# 3. KDP CALCULATOR (Bleed, Gutter, Margins)
st.sidebar.header("📐 KDP Print Standards")
trim_choice = st.sidebar.selectbox("Trim Size", ["8.5 x 8.5", "6 x 9", "8.5 x 11"])
has_bleed = st.sidebar.checkbox("Apply Bleed", value=True)

# KDP Rules: Bleed adds 0.125" to width and 0.25" to total height
trim_map = {"8.5 x 8.5": (8.5, 8.5), "6 x 9": (6, 9), "8.5 x 11": (8.5, 11)}
base_w, base_h = trim_map[trim_choice]

if has_bleed:
    final_w, final_h = base_w + 0.125, base_h + 0.25
    trim_offset = 0.125 # The "cut" line starts 0.125 in from the edge
else:
    final_w, final_h = base_w, base_h
    trim_offset = 0

# Safe Zone: KDP requires text to be 0.375" from edges
safe_margin = 0.375

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload your DOCX", type="docx")

if uploaded_file and not st.session_state.pages:
    doc = Document(uploaded_file)
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            st.session_state.pages.append({"img_bytes": rel.target_part.blob, "text": "", "rects": []})

# --- VISUAL STUDIO ---
if st.session_state.pages:
    idx = st.session_state.current_page
    col_nav, col_main = st.columns([1, 4])
    
    with col_nav:
        st.write(f"**Page {idx+1} of {len(st.session_state.pages)}**")
        if st.button("Previous Page") and idx > 0: st.session_state.current_page -= 1; st.rerun()
        if st.button("Next Page") and idx < len(st.session_state.pages)-1: st.session_state.current_page += 1; st.rerun()
        
    with col_main:
        # Create a preview image with KDP GUIDES
        orig_img = Image.open(io.BytesIO(st.session_state.pages[idx]["img_bytes"]))
        # Scale image to 600px for the editor
        preview_img = orig_img.resize((600, 600))
        draw = ImageDraw.Draw(preview_img)
        
        # DRAW DOTTED GUIDES
        # 1. Trim Line (Red - Where it cuts)
        trim_px = (trim_offset / final_w) * 600
        draw.rectangle([trim_px, trim_px, 600-trim_px, 600-trim_px], outline="red", width=2)
        
        # 2. Safe Zone (Yellow Dotted - Keep text inside here)
        safe_px = ((trim_offset + safe_margin) / final_w) * 600
        draw.rectangle([safe_px, safe_px, 600-safe_px, 600-safe_px], outline="yellow", width=1)

        st.subheader("Visual Layout Editor")
        st.caption("🔴 Red Line = Trim Edge | 🟡 Yellow Line = Safe Zone (Keep text inside)")
        
        canvas_result = st_canvas(
            background_image=preview_img,
            drawing_mode="rect",
            stroke_color="#00FF00",
            stroke_width=2,
            height=600, width=600,
            key=f"canvas_{idx}"
        )
        
        user_text = st.text_area("Add text for this page:", value=st.session_state.pages[idx]["text"])
        st.session_state.pages[idx]["text"] = user_text

    # --- PDF EXPORT ---
    if st.sidebar.button("🚀 CREATE KDP PDF"):
        output = io.BytesIO()
        c = canvas.Canvas(output, pagesizes=(final_w * inch, final_h * inch))
        
        for p in st.session_state.pages:
            img = Image.open(io.BytesIO(p["img_bytes"]))
            # Stretch image to cover the full Bleed size
            c.drawInlineImage(img, 0, 0, width=final_w*inch, height=final_h*inch)
            
            if p["text"]:
                c.setFont("Helvetica-Bold", 16)
                c.setFillColor(colors.white)
                # Centered at bottom safe zone
                c.drawCentredString((final_w/2)*inch, (trim_offset + 0.5)*inch, p["text"])
            c.showPage()
        
        c.save()
        st.sidebar.download_button("📥 Download Final PDF", output.getvalue(), "KDP_READY.pdf")
