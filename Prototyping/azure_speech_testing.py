import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

def from_file():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
    speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "LogfilePathAndName")
    audio_config = speechsdk.AudioConfig(filename="uploaded_file.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    print(result.text)

from_file()