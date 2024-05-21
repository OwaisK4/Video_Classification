import whisper
import os
basepath = os.path.dirname(__name__)
audio_path = os.path.join(basepath, "uploaded_file.wav")

model = whisper.load_model("base")
result = model.transcribe(audio_path, language="en")
print(result["text"])