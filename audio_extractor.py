from pydub import AudioSegment

filepath = "Materials/Toronto_30s.mp4"

# Load the video file
video = AudioSegment.from_file(filepath, format="mp4")
audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2)
audio.export("audio.wav", format="wav")