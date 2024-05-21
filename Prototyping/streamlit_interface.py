import streamlit as st
from ffmpy import FFmpeg
import whisper
model = whisper.load_model("base")
import os
basepath = os.path.dirname(__name__)

st.title("Video Transcriber")
genre = st.radio("What's your favorite movie genre",
["English", "Japanese"],
captions = ["Transcribe video into English text", "動画を日本語テキストに書き写す"])
# st.write(genre)
codes = {"English":"en", "Japanese": "ja"}

uploaded_file = st.file_uploader("Choose a file", type="mp4")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    video_path = os.path.join(basepath, "uploaded_file.mp4")
    audio_path = os.path.join(basepath, "uploaded_file.wav")
    with open(video_path, "wb") as f:
        f.write(bytes_data)
    
    ff = FFmpeg(
        # inputs = {video_path: None},s
        # outputs = {audio_path: "-ac 2 -f wav"}
        inputs = {video_path: "-y -ss 00:00:00"},
        outputs = {audio_path: "-t 00:02:00 -ac 2 -f wav"}
    )

    print(ff.cmd)
    ff.run()
    # st.write(audio_path)

    if os.path.exists(audio_path):
        result = model.transcribe(audio_path, language=codes[genre])
        print(result["text"])
        st.header("Transcribed text:")
        st.write(result["text"])