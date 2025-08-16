"""
MIT License

Copyright (c) 2025 Erdem Mirza 

This file is part of the project and is licensed under the MIT License.
"""


from PySide6.QtCore import (QSize, Signal, Qt)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import ( QHBoxLayout, QListWidgetItem,
    QMenu, QPushButton,QListWidget, QFrame)
from custom_button import CustomButton

class CutWidgets(QFrame):
    
    itemRemoved = Signal(int)

    def __init__(self, cut,  parent: QListWidget = None):
        if not isinstance(parent,QListWidget):
            raise TypeError("Parent must be a QlistWidget or its subclass")
        super().__init__(parent)

        layout = QHBoxLayout()
        self.cut = cut
        self.parent = parent
        self.item = None

        self.menu = QMenu(self)
        remove_action = QAction("Remove cut",self)
        remove_action.triggered.connect(self.remove)
        self.menu.setStyleSheet("""
            QMenu::item {
                padding: 10px;

                text-align: center; 
            }
        """)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos : self.menu.exec(self.mapToGlobal(pos)))
        self.menu.addAction(remove_action)

        self.start_time_button = QPushButton(CutWidgets.time_converter(self.cut.get_start_time()))
        self.end_time_button = QPushButton(CutWidgets.time_converter(self.cut.get_end_time()))
        self.colorButton = CustomButton(self.cut.get_start_time())
        self.colorButton.setStyleSheet(f" background-color:{self.cut.get_color()}")
        self.script = QPushButton("...")

        self.colorButton.setFocusPolicy(Qt.NoFocus)


        layout.addWidget(self.start_time_button)
        layout.addWidget(self.end_time_button)
        layout.addSpacing(10)
        layout.addWidget(self.script)
        layout.addWidget(self.colorButton)
        layout.setStretch(3,3)

        """  self.start_time_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.end_time_button.setAlignment(Qt.AlignmentFlag.AlignCenter) """
        self.colorButton.setFixedSize(QSize(30,30))
        self.setObjectName("mainFrame")
        self.setStyleSheet("" \
        "QFrame#mainFrame{" \
        "background-color: transparent; border-bottom: 1px solid rgb(255,255,255) ;}")
        
        self.setLayout(layout)
    
    def addList(self,index):
        
        item = QListWidgetItem()
        self.parent.insertItem(index, item)
        self.parent.setItemWidget(item, self)
        item.setSizeHint(self.sizeHint())
        self.item = item


    def remove(self):
       
       index = self.parent.row(self.item)
       self.parent.takeItem(index)
       self.item = None
       self.deleteLater()
       self.itemRemoved.emit(index)

    @staticmethod
    def time_converter(time):

        seconds = time // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"
