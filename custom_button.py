"""
MIT License

Copyright (c) 2025 Erdem Mirza

This file is part of the project and is licensed under the MIT License.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton

#Almost identical to a standard QPushButton, except it includes custom mouse events and additional signals.
class CustomButton(QPushButton):
    
    customClicked = Signal(int)
    customDoubleClicked = Signal(int)

    def __init__(self, start_time):
        super().__init__()
        self.time = start_time
    
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.customDoubleClicked.emit(self.time)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.customClicked.emit(self.time)
