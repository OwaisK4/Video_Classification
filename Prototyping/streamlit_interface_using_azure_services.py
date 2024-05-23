import streamlit as st
from ffmpy import FFmpeg
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk
from dotenv import load_dotenv
load_dotenv()
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
basepath = os.path.dirname(__name__)

st.title("Video Transcriber")
genre = st.radio("What language should be used for transcription?",
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
        # inputs = {video_path: None},
        # outputs = {audio_path: "-ac 2 -f wav"}
        inputs = {video_path: "-y -ss 00:00:00"},
        outputs = {audio_path: "-t 00:02:00 -ac 2 -f wav"}
    )

    print(ff.cmd)
    ff.run()

    if os.path.exists(audio_path):
        # result = model.transcribe(audio_path, language=codes[genre])
        # print(result["text"])
        # st.header("Transcribed text:")
        # st.write(result["text"])
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
        audio_config = speechsdk.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once_async().get()
        print(result.text)
        st.header("Transcribed text:")
        st.write(result.text)
        
        endpoint = os.environ["LANGUAGE_ENDPOINT"]
        key = os.environ["LANGUAGE_KEY"]
        text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        tagged = text_analytics_client.recognize_entities([result.text])
        tagged = [t for t in tagged if not t.is_error]
        named_entities = []
        for review in tagged:
            print(review.entities)
            for entity in review.entities:
                print(f"Entity: '{entity.text}' has category '{entity.category}'")
                named_entities.append(f"Entity: '{entity.text}' has category '{entity.category}'")
        st.header("Named Entities:")
        st.write(named_entities)
        # tokens = word_tokenize(result["text"])
        # tagged_words = pos_tag(tokens)
        # named_entities = ne_chunk(tagged_words)
        # chunks = []
        # for chunk in named_entities:
        #     if hasattr(chunk, 'label'):
        #         print(chunk.label(), ' '.join(c[0] for c in chunk))
        #         chunks.append(chunk.label() + " " + ' '.join(c[0] for c in chunk))
        # st.header("Named Entities:")
        # st.write(chunks)
        # st.write(named_entities)