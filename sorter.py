import whisper_timestamped as whisper
import json
from moviepy.editor import *


def sorter(device):
    
    video = VideoFileClip("video/sort.mp4")
    video.audio.write_audiofile("audio/audio.wav")
    
    audio = whisper.load_audio("audio/audio.wav")

    model = whisper.load_model("NbAiLab/whisper-large-v2-nob", device=device)

    result = whisper.transcribe(model, audio, language="en")
    
    segments = result['segments']
    len_segments = len(segments)
    data = None

    for i in range(0, len_segments):
        if data == None:
            data = segments[i]["words"]
        else:
            data = data + segments[i]["words"]

    sorted_data = sorted(data, key=lambda x: (x["text"].lower(), x["start"]))

    final = None
    concatclip = []

    for index, value in enumerate(sorted_data):
        start = value['start']
        end = value['end']
        clip = video.subclip(start, end)
        concatclip.append(clip)

    final = concatenate_videoclips(concatclip)
    return final.write_videofile("video/final.mp4")
