import streamlit as st
from ffmpy import FFmpeg
from dotenv import load_dotenv
load_dotenv()
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os, time
basepath = os.path.dirname(__name__)
done = False

st.title("Video Transcriber")
genre = st.radio("What language should be used for transcription?",
["English", "Japanese"],
captions = ["Transcribe video into English text", "動画を日本語テキストに書き写す"])
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
        inputs = {video_path: "-y"},
        outputs = {audio_path: "-ac 2 -f wav"}
        # inputs = {video_path: "-y -ss 00:00:00"},
        # outputs = {audio_path: "-t 00:01:00 -ac 2 -f wav"}
    )

    print(ff.cmd)
    ff.run()

    if os.path.exists(audio_path):
        f = open("Output.txt", "w")

        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
        audio_config = speechsdk.AudioConfig(filename=audio_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        # result = speech_recognizer.recognize_once_async().get()
        textOut = []
        def stop_cb(evt):
            print(evt)
            speech_recognizer.stop_continuous_recognition()
            global done
            done = True

        def outPrint(evt):
            global textOut
            tmp_text = evt.result.text
            tmp_text = tmp_text.strip('"')
            textOut.append(tmp_text)
            print(tmp_text)

        speech_recognizer.recognized.connect(outPrint)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.start_continuous_recognition()

        while not done:
            time.sleep(.5)

        print(textOut)
        st.header("Transcribed text:")
        st.write(" ".join(textOut))
        f.write("Transcribed text:\n")
        f.write(" ".join(textOut))
        f.write("\n\n")
        
        endpoint = os.environ["LANGUAGE_ENDPOINT"]
        key = os.environ["LANGUAGE_KEY"]
        text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

        # tagged = text_analytics_client.recognize_entities(textOut)
        tagged = []
        for i in range(0, len(textOut), 5):
            k = min(i + 5, len(textOut))
            result = text_analytics_client.recognize_entities(textOut[i:k])
            result = [review for review in result if not review.is_error]
            tagged += result
        named_entities = []
        for review in tagged:
            print(review.entities)
            for entity in review.entities:
                print(f"Entity: '{entity.text}' has category '{entity.category}'")
                named_entities.append(f"Entity: '{entity.text}' has category '{entity.category}'")
        named_entities = list(set(named_entities))
        st.header("Named Entities:")
        st.write(named_entities)
        f.write("Named Entities:\n")
        for ne in named_entities:
            f.write(ne)
            f.write("\n")

        f.close()