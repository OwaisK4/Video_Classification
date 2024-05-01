import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Open the audio file
with sr.AudioFile("audio.wav") as source:
    audio_text = r.record(source)
# Recognize the speech in the audio
# text = r.recognize_google(audio_text, language='en-US')
text = r.recognize_sphinx(audio_text, language='en-US')

# Print the transcript
file_name = "transcription.txt"

with open(file_name, "w") as file:
    file.write(text)