import streamlit as st
import io
import time
import whisper_timestamped as whisper
from sorter import sorter
from typing import Any


st.title("Video Sorter")

models = st.selectbox(
    'Select a model',
    ('tiny', 'base', 'small', 'medium', 'large'), help='Whisper model to use for video sorting')

if models:
    @st.cache_resource(show_spinner='cahcing model beep boop')
    def cache_model() -> Any:
        """
        Cache the model

        Returns:
            Any: The cached model
        """
        # Load the model
        model = whisper.load_model(models, device="cpu")
        
        return model

    model = cache_model()

uploaded_video = st.file_uploader("Choose a video file", type=["mp4"])

if uploaded_video is not None:
    g = io.BytesIO(uploaded_video.read()) 
    location = "video/sort.mp4"

    with open(location, "wb") as f:
        f.write(g.read())

    f.close()

    sorter(model)

    progress_text = "Beeep Boop sorting ya video"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(1000):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    
    with open("video/final.mp4", "rb") as file:
        btn = st.download_button(
                label="Download video",
                data=file,
                file_name="final.mp4",
                mime="video/mp4"
            )