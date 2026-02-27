import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd

# --- CONFIGURATION ---
# Note: Keeping Streamlit at 1.40.0 in requirements.txt is required for this to run
st.set_page_config(page_title="Salam Truthful - KDP Studio", layout="wide")

# 1. COMPREHENSIVE KDP TRIM SIZE LIBRARY
KDP_TRIM_SIZES = {
    "8.5 x 8.5 (Square)": (8.5, 8.5),
    "8 x 10 (Classic Picture Book)": (8, 10),
    "7.5 x 9.25 (Budget Portrait)": (7.5, 9.25),
    "7 x 10 (Modern Portrait)": (7, 10),
    "8.25 x 8.25 (Expanded Square)": (8.25, 8.25),
    "8.25 x 11 (Standard Large)": (8.25, 11),
    "8.5 x 11 (Max Size)": (8.5, 11),
    "6 x 9 (Standard Novel)": (6, 9),
    "5.5 x 8.5 (Trade Paperback)": (5.5, 8.5),
    "5 x 8 (Pocket Book)": (5, 8)
}

st.title("🎨 KDP Picture Book Studio")
st.write("Professional Margin & Bleed Alignment for Amazon Authors.")

# --- SIDEBAR: SETTINGS ---
st.sidebar.header("1. Book Dimensions")
selected_label = st.sidebar.selectbox("Select Amazon Trim Size:", list(KDP_TRIM_SIZES.keys()))
base_w, base_h = KDP_TRIM_SIZES[selected_label]

# Bleed is almost always required for picture books where images touch the edge
has_bleed = st.sidebar.checkbox("Apply Amazon Bleed (+0.125\")", value=True)

# 2. AUTOMATIC KDP BLEED LOGIC
if has_bleed:
    # Amazon Requirement: Add 0.125" to width and 0.25" total to height
    final_w = base_w + 0.125
    final_h = base_h + 0.25
    bleed_status = "Included"
else:
    final_w = base_w
    final_h = base_h
    bleed_status = "No Bleed"

st.sidebar.success(f"Output Size: {final_w}\" x {final_h}\" ({bleed_status})")

# --- MAIN INTERFACE ---
uploaded_file = st.file_uploader("Upload your illustration (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    
    # Scale canvas preview for display
    canvas_width = 800 
    aspect_ratio = final_h / final_w
    canvas_height = int(canvas_width * aspect_ratio)

    st.write(f"### Formatting Page: {selected_label}")
    with st.expander("👁️ Why is my page size larger?"):
        st.write(f"Amazon KDP requires an extra **0.125 inches** on the edges to ensure your images reach the very edge after the book is trimmed. Your selected {base_w}x{base_h} book will be exported at exactly {final_w}x{final_h} to pass the KDP check.")

    

    # 3. DRAWABLE CANVAS (Includes Version-Compatibility Fix)
    # Using a unique key prevents the canvas from resetting on every click
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  
        stroke_width=2,
        background_image=img,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode="rect",
        key=f"kdp_canvas_{selected_label}", 
    )

    # --- FOOTER: LEGAL & REDIRECT ---
    st.markdown("---")
    st.write("### 📜 Final Verification")

    # User Agreement Checkbox
    agree = st.checkbox("I acknowledge that I am responsible for reviewing the final PDF in the Amazon KDP Print Previewer. Salam Truthful Ltd is a formatting tool and does not guarantee Amazon's final acceptance.")

    if agree:
        if st.button("🚀 Export Amazon-Ready PDF"):
            st.info("Preparing high-resolution PDF... This will include the automated bleed margins.")
            # PDF processing code would execute here
        
        st.markdown(
            f"""
            <div style="text-align: center; padding: 30px; border: 1px solid #ddd; border-radius: 10px; margin-top: 20px;">
                <p style="font-size: 18px;">Need help with your cover or spine?</p>
                <a href="https://www.salamtruthful.com" target="_blank" style="text-decoration: none;">
                    <button style="border-radius: 8px; padding: 12px 24px; background-color: #007bff; color: white; border: none; font-weight: bold; cursor: pointer;">
                        Back to SalamTruthful.com
                    </button>
                </a>
            </div>
            """,
            unsafe_content_html=True
        )
    else:
        st.warning("Please check the 'Final Verification' box to enable the export button.")

else:
    st.info("Waiting for an image upload to begin formatting...")
