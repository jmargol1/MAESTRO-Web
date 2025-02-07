from utils.ai_api import get_ai_api
from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.VideoFileClip import AudioFileClip

class Stitcher:
    def __init__(self, ai_api=None):
        self.ai_api = get_ai_api(ai_api)
    
    def ImposeAudio(self):

        vids = dict(slide, scene in self.__dict__.items())
        auds = dict(slide, audio in self.__dict__.items())
        finVideo = {}

        for key in VideoDict:
            try: 
                auds[key] == True
                video = vids[key].fx(vfx.speedx, vids[key].duration/auds[key].duration)
                video.audio = auds[key]
            except:
                video = vids[key]
            finVideo[key] = video
        finVideo = list(finVideo.values())
        finVideo = concatenate_videoclips(finVideo)
        finVideo.write_videofile("Lecture.mp4", fps=30, audio_codec="aac", audio_bitrate="192k")

        return self.ai_api.generate_response(finVideo)