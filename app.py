import streamlit as st
import io
import time
import whisper_timestamped as whisper
from sorter import sorter
from typing import Any


st.title("Video Sorter")

device = st.selectbox(
    'Select a device',
    ('cpu', 'cuda'), help='Choose what device to run the model on.')


uploaded_video = st.file_uploader("Choose a video file", type=["mp4","mkv"])

if uploaded_video is not None:
    g = io.BytesIO(uploaded_video.read()) 
    location = "video/sort.mp4"

    with open(location, "wb") as f:
        f.write(g.read())

    f.close()

    sorter(device)

    progress_text = "Beeep Boop sorting ya video"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
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