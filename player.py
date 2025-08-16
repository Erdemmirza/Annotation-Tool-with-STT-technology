"""
MIT License

Copyright (c) 2025 Erdem Mirza 

This file is part of the project and is licensed under the MIT License.
"""


from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import  QApplication, QVBoxLayout, QHBoxLayout, QWidget, QSlider, QSizePolicy, QLabel
from PySide6.QtCore import Qt




class Player(QWidget):
    
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audioPlayer = QAudioOutput()
        self.videoPlayer = QVideoWidget()
    
        self.player.setVideoOutput(self.videoPlayer)
        self.player.setAudioOutput(self.audioPlayer)
        self.audioPlayer.setVolume(25)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet( "background: rgb(10,10,10) ; ")

        self.current_time = QLabel("00:00:00")
        self.total_time = QLabel("00:00:00")
        self.current_time.setMaximumWidth(60)
        self.total_time.setMaximumWidth(60)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.current_time)
        time_layout.addStretch(1)
        time_layout.addWidget(self.total_time)
        


        layout = QVBoxLayout()
 
        
        self.videoPlayer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.videoPlayer)
        layout.addWidget(self.slider)
        layout.addItem(time_layout)
        
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        
        self.setLayout(layout) 
        
        

if __name__ == "__main__":
    
    app = QApplication([])
    window = Player()
    window.showMaximized()
    app.exec()

