"""
MIT License

Copyright (c) 2025 Erdem Mirza 

This file is part of the project and is licensed under the MIT License.
"""


from PySide6.QtCore import Signal
from PySide6.QtGui import (QColor,
    QPainter)
from PySide6.QtWidgets import (QApplication,QWidget)

from cuts import Cut

class SegmentedBar(QWidget):
    
    segmentClicked = Signal(int,int)
    segmentDoubleClicked = Signal(int,int)

    def __init__(self, duration=1000, start_time=0):
        super().__init__()

        self.segments = []  # List of cuts.
        self.start_time = start_time
        self.duration = duration  # Duration of the video
    
    
    def val_to_coordinate(self, value):
        val = (( value - self.start_time ) / (self.duration - self.start_time)) * self.width()
        return round(val)
    
    def set_duration(self, duration):
        self.duration = duration

    def paintEvent(self, ev):
        super().paintEvent(ev)
        painter = QPainter(self)

        x = 0
        y = 0
        w = self.width()
        h = self.height()

        
        painter.setBrush("black")
        painter.setPen("white")
        painter.drawRect(x, y, w, h)


        for cut in self.segments:

            start_pos = self.val_to_coordinate(cut.get_start_time())
            end_pos = self.val_to_coordinate(cut.get_end_time())
            segment_x = x + start_pos
            segment_width = end_pos - start_pos

            color = QColor(cut.get_color())
            painter.setBrush(color)
            painter.drawRect(segment_x,y,segment_width,h)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        x = event.position().x()
        for cut in self.segments:

            starting_x = self.val_to_coordinate(cut.get_start_time())
            ending_x = self.val_to_coordinate(cut.get_end_time())
            
            if starting_x <= x <= ending_x:

                self.segmentClicked.emit(self.segments.index(cut), cut.get_start_time())

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        x = event.position().x()

        for cut in self.segments:

            starting_x = self.val_to_coordinate(cut.get_start_time())
            ending_x = self.val_to_coordinate(cut.get_end_time())

            if starting_x <= x <= ending_x:

                self.segmentDoubleClicked.emit(self.segments.index(cut), cut.get_start_time())


    def addSegment(self, cut):

        self.segments.append(cut)
        self.segments.sort(key = lambda x : x.start_time)
        self.update()

    def removeSegment(self,index):
        self.segments.pop(index)
        self.update()

if __name__ == "__main__":
    
    app = QApplication([])
    window = SegmentedBar(1000)
    cut1 = Cut(12.5, 100, "yellow")
    cut2 = Cut(100, 150, "yellow")
    cut3 = Cut(150, 200, "yellow")
    cut4 = Cut(200, 300, "green")
    window.addSegment(cut1)
    window.addSegment(cut2)
    window.addSegment(cut3)
    window.addSegment(cut4)
    window.show()
    app.exec()