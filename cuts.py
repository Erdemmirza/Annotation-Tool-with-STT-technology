"""
MIT License

Copyright (c) 2025 Erdem Mirza 

This file is part of the project and is licensed under the MIT License.
"""

#Class of frames or cuts extracted from the video.

class Cut:
    def __init__(self,start = 0 , end = 0, color = "", source_video_path = "",script = ""):
        

        self.start_time = start #Time stamps
        self.end_time = end
        self.color = color
        self.source_video_path = source_video_path
        self.script = script
    
    def set_start(self, start):
        self.start_time = start

    def set_end(self, end):
        self.end_time = end

    def set_color(self, color):
        self.color = color

    def set_video(self,video_path):
        self.video_path = video_path

    def set_audio(self,audio_path):
        self.audio_path = audio_path

    def set_script(self, text):
        self.script = text
    
    def get_script(self):
        return self.script

    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time
    
    def get_color(self):
        return self.color

