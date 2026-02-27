import streamlit as st
import fitz  # PyMuPDF
import io

# 1. Setup
st.set_page_config(page_title="Salam Truthful KDP Fixer")
st.title("🛡️ KDP Safe-Zone Fixer")
st.write("Ensuring your art never gets cut off by Amazon's blades.")

# 2. Dimensions
size_choice = st.selectbox("Select Trim Size", ["8.5 x 8.5", "8 x 10", "6 x 9", "8.5 x 11"])
w_in, h_in = [float(x) for x in size_choice.split(" x ")]

# 3. The Math (72 points = 1 inch)
# We add the required 0.125" bleed
final_w = (w_in + 0.125) * 72
final_h = (h_in + 0.25) * 72

up = st.file_uploader("Upload your PDF", type="pdf")

if up:
    try:
        out_pdf = fitz.open()
        with st.spinner("Protecting Safe Zones..."):
            in_pdf = fitz.open(stream=up.read(), filetype="pdf")
            
            # This is how we solve the cut-off: 
            # We create a 'Safe Rect' that is slightly smaller than the page.
            # Your art goes INSIDE this box so it's never near the blade.
            safe_margin = 18  # 0.25 inch safety cushion
            safe_rect = fitz.Rect(safe_margin, safe_margin, final_w - safe_margin, final_h - safe_margin)

            for page in in_pdf:
                # Convert page to image
                pix = page.get_pixmap(dpi=150)
                img_data = pix.tobytes("png")
                
                # Create KDP sized page
                new_page = out_pdf.new_page(width=final_w, height=final_h)
                
                # Insert image into the SAFE ZONE only
                new_page.insert_image(safe_rect, stream=img_data, keep_proportion=True)

        st.success("Success! Art is now centered and safe.")
        st.download_button("📥 Download KDP-Ready PDF", out_pdf.tobytes(), "KDP_Safe_Book.pdf")
        
    except Exception as e:
        st.error("Server error. Please try a smaller PDF or refresh the page.")
