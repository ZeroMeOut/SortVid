import whisper_timestamped as whisper
from moviepy.editor import *
import json

def sorter(model):
    
    video = VideoFileClip("video/sort.mp4")
    video.audio.write_audiofile("audio/audio.wav")
    audio = whisper.load_audio("audio/audio.wav")

    result = whisper.transcribe(model, audio, language="en")
    
    data = result['segments'][0]['words']

    sorted_data = sorted(data, key=lambda x: (x["text"].lower(), x["start"]))

    final = None
    concatclip = None

    for index, value in enumerate(sorted_data):
        start = value['start']
        end = value['end']
        clip = video.subclip(start, end)

        if concatclip == None:
            concatclip = clip
            final = concatclip
        else:
            final = concatenate_videoclips([concatclip, clip])
            concatclip = final
    return final.write_videofile("video/final.mp4")
