import streamlit as st
import os

st.set_page_config(page_title="Photo Search", layout="wide")
st.title("📸 Intelligent Event Photo Retrieval System")
st.markdown("Find yourself in event photos!")

# Create tabs
tab1, tab2 = st.tabs(["📁 Index Photos", "🔍 Search Photos"])

with tab1:
    st.header("Step 1: Index Photos")
    st.write("This will process photos in the `data/input/` folder")
    
    if st.button("🚀 Start Indexing", type="primary"):
        st.success("Indexing started!")
        with st.spinner("Processing photos..."):
            st.write("Simulating photo processing...")
            # Simulate progress
            import time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            st.success("✅ 10 photos processed, 25 faces found!")

with tab2:
    st.header("Step 2: Search Photos")
    uploaded_file = st.file_uploader("Upload your selfie", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Your selfie", width=200)
        
    if st.button("🔎 Find My Photos"):
        if uploaded_file:
            st.success("Found 5 matching photos!")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image("https://picsum.photos/200/300", caption="Match 1: 92% similarity")
            with col2:
                st.image("https://picsum.photos/200/300", caption="Match 2: 88% similarity")
            with col3:
                st.image("https://picsum.photos/200/300", caption="Match 3: 85% similarity")
        else:
            st.error("Please upload a selfie first!")