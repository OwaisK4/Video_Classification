import os, time
from dotenv import load_dotenv
load_dotenv()
import azure.cognitiveservices.speech as speechsdk

def from_file():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get("SPEECH_KEY"), region=os.environ.get("SPEECH_REGION"))
    speech_config.set_property(speechsdk.PropertyId.Speech_LogFilename, "LogfilePathAndName")
    audio_config = speechsdk.AudioConfig(filename="uploaded_file.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # result = speech_recognizer.recognize_once_async().get()
    # print(result.text)
    done = False

    textOut = ""
    def stop_cb(evt):
        print(evt)
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    def outPrint(evt):
        nonlocal textOut
        tmp_text = evt.result.text
        textOut += tmp_text + "\n"
        print(tmp_text)

    speech_recognizer.recognized.connect(outPrint)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)
    with open("output.txt", 'w') as f:
        f.write(textOut)

from_file()