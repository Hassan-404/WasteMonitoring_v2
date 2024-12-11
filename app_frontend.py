from pathlib import Path
import PIL

import streamlit as st

import settings
import model_utils
from login import ensure_login

ensure_login()

st.set_page_config(
    page_title="Waste Monitoring",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Waste Monitoring System")


about_text = """
The world generates at least 3.5 million tons of waste per day, and this number is still increasing day by day.
That's why we need to be aware of waste.

This app helps you classify your waste into 6 different categories: Plastic, Biodegradable (Organic), Metal, Paper, Glass, Cardboard.
"""
st.markdown(f"<div class='description-text'>{about_text}</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None

model_type = 'Detection' 
confidence = 0.25 

model_path = Path(settings.DETECTION_MODEL)
try:
    model = model_utils.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        if source_img:
            try:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image", use_container_width=True)
            except Exception as ex:
                st.error("Error occurred while opening the image.")
                st.error(ex)
        else:
            st.warning("Please upload an image to proceed.")

    with col2:
        if source_img:
            if st.sidebar.button('Classify Items', key='classify_items'):
                try:
                    res = model.predict(uploaded_image, conf=confidence)
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image', use_container_width=True)
                except Exception as ex:
                    st.error("Error occurred during detection.")
                    st.error(ex)
        else:
            st.warning("Upload an image to detect objects.")

elif source_radio == settings.WEBCAM:
    captured_image = st.camera_input("Capture an image", key="capture")
    show_capture = True  

    col1, col2 = st.columns(2)

    with col1:
        if captured_image is not None:
            try:
                img = PIL.Image.open(captured_image).convert("RGB")
                st.image(img, caption="Captured Image", use_container_width=True)
            except Exception as ex:
                st.error("Error occurred while processing the captured image.")
                st.error(ex)
        else:
            st.warning("Please capture an image to proceed.")

    with col2:
        if captured_image is not None:
            try:
                if st.sidebar.button("Classify Captured Image", key="classify_captured_image"):
                    res = model.predict(img, conf=confidence)
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image', use_container_width=True)
            except Exception as ex:
                st.error("Error occurred during detection.")
                st.error(ex)
        else:
            st.warning("Capture an image to detect objects.")
else: 
    st.error("Please select a valid source type!")
