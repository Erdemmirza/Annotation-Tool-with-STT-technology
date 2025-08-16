"""
MIT License

Copyright (c) 2025 Erdem Mirza

This file is part of the project and is licensed under the MIT License.
"""

import subprocess
import os
from cuts import Cut
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QApplication
import sys
import threading

import whisper

class Worker(QObject):
    finished = Signal(str) 
    error = Signal(str)
    
    run_count = 1
    model_lock = threading.Lock() 

    def __init__(self, cut, model):
        super().__init__()
        self.cut = cut
        self.model = model

    def run(self):
        
        try:
            temp_path = "temp_cut" + str(Worker.run_count) + ".wav"
            Worker.run_count += 1
            duration = (self.cut.end_time - self.cut.start_time) / 1000
            start = self.cut.start_time / 1000

            args = [
                "-ss", str(start),
                "-i", self.cut.source_video_path,
                "-t", str(duration),
                "-ar", "16000",
                "-ac", "1",
                "-acodec", "pcm_s16le",
                "-y",
                temp_path
            ]

            result = subprocess.run(
                    ["ffmpeg"] + args,
                    capture_output=True,
                    text=True,
                    check= True
                )


            if result.returncode != 0:
                self.error.emit(f"FFmpeg error: {result.stderr}")
                return

            with Worker.model_lock:  
                result = self.model.transcribe(temp_path)

            os.remove(temp_path)

            self.finished.emit(result["text"])

        except (Exception,subprocess.CalledProcessError) as e:
            print("Error", e)
            self.error.emit(str(e))

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    model = whisper.load_model("medium")  # medium, large vs.
    cut = Cut(start=12500, end=30000, color="red", source_video_path="videoplayback.mp4")

    thread = QThread()
    worker = Worker(cut, model)

    worker.moveToThread(thread)

    thread.started.connect(worker.run)
    
    worker.finished.connect(lambda text: print("Transcription done:", text))
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)

    worker.error.connect(lambda err: print("Error:", err))
    worker.error.connect(thread.quit)
    worker.error.connect(worker.deleteLater)
    thread.start()

    sys.exit(app.exec())