"""
MIT License

Copyright (c) 2025 Erdem Mirza 

This file is part of the project and is licensed under the MIT License.
"""


from PySide6.QtCore import (QTime, QTimer, QThread,
    QSize, QUrl, Qt)
from PySide6.QtGui import (QAction, QIcon, QKeySequence)

from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QFileDialog, QMessageBox,
    QSlider, QListWidget,QDialog,QTimeEdit,
    QVBoxLayout, QWidget, QFrame, QLabel)

import csv
from cuts import Cut    
from segmented_bar import SegmentedBar
from player import Player
from cut_widgets import CutWidgets
from thread import Worker
from dialog import CustomDialog
import whisper

class AnnotationWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.model = whisper.load_model("medium")

        self.threads = []
        self.list_item_widgets = []
        self.control_button_isPaused = False
        self.transcript_dialog = None
        self.time_dialog= None
        self.colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
        self.color_index = 0

        vertical_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        self.playerWidget = Player()
        self._construct_control_bar()
        self._construct_list()
        self.segmented_bar = SegmentedBar()
        self.segmented_bar.setMinimumHeight(20)

        self.start_time = 0
        self.end_time = 0
        self.interface = QWidget()
        

        vertical_layout.addWidget(self.playerWidget)
        vertical_layout.addWidget(self.buttonFrame)
    
        horizontal_layout.addLayout(vertical_layout)
        horizontal_layout.addWidget(self.listWidget)
        horizontal_layout.setStretch(0,2)
        horizontal_layout.setStretch(1,1)
        
        vertical2 = QVBoxLayout()
        vertical2.addLayout(horizontal_layout)
        vertical2.addWidget( self.segmented_bar)

        self.interface.setLayout(vertical2)
        self.setCentralWidget(self.interface)

        self._signals_and_slots()
        self.actions_and_menu()


    def _construct_control_bar(self):

        self.control_button = QPushButton(QIcon("icons\control.png"),"")
        self.forward_button = QPushButton(QIcon("icons\control-double.png"),"")
        self.backward_button = QPushButton(QIcon("icons\control-double-180.png"),"")

        self.control_button.setShortcut(QKeySequence("Space"))
        self.forward_button.setShortcut(QKeySequence("Right"))
        self.backward_button.setShortcut(QKeySequence("Left"))

        self.take_button = QPushButton("Take")
        self.cut_button = QPushButton("Cut")
        self.cut_button.setDisabled(True)

        self.take_button.setStyleSheet(" background-color: rgb(40,40,40) ; border : 1px solid white ; font-weight: bold;")
        self.cut_button.setStyleSheet(" background-color:  rgb(40,40,40) ;  border : 1px solid white ; font-weight: bold;")
        self.take_button.setShortcut("Ctrl+X")
        self.cut_button.setShortcut("Ctrl+C")
        
        self.take_button.setToolTip("Ctrl+X")
        self.cut_button.setToolTip("Ctrl+C")

        self.take_button.setFixedSize(QSize(30,30))
        self.cut_button.setFixedSize(QSize(30,30))


        self.control_button.setStyleSheet(""" 
            QPushButton{
            border-radius: 14px ;
            border: none;
            background-color: white;
            }
            QPushButton:hover{
            background-color: rgba(255, 255, 255,150);
            } """)
        
        self.control_button.setIconSize(QSize(24,24))
        self.forward_button.setIconSize(QSize(24,24))
        self.backward_button.setIconSize(QSize(24,24))
        self.backward_button.setStyleSheet( """
            QPushButton{
            background : white;
            border-radius: 10px ;
            border: none;
            }
            QPushButton:hover{
            background-color: rgba(255, 255, 255,150);
            }""")

        self.forward_button.setStyleSheet( """
            QPushButton{
            background : white;
            border-radius: 10px ;
            border: none;
            }
            QPushButton:hover{
            background-color: rgba(255, 255, 255,150);
            }""")
        
        self.control_button.setFixedSize(40,30)

        self.control_button.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)

        self.volume_text = QLineEdit()
        self.volume_text.setMaximumWidth(30)
        self.volume_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_text.setText("25")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimumWidth(200)
        self.volume_slider.setValue(25)

        layout = QHBoxLayout()
        layout.addSpacing(50)
        layout.addWidget(self.take_button)
        layout.addWidget(self.cut_button)
        layout.addStretch(1)
        layout.addWidget(self.backward_button)
        layout.addWidget(self.control_button)
        layout.addWidget(self.forward_button)
        layout.addStretch(1)
        layout.addWidget(self.volume_text)
        layout.addWidget(self.volume_slider)
        layout.setStretch(8,1)
        layout.setStretch(4,0.05)

        self.buttonFrame = QFrame()
        self.buttonFrame.setStyleSheet("""
            background-color: rgb(60, 60, 60);
            border-radius: 24px;
        """)
        self.buttonFrame.setMaximumHeight(48)
        self.buttonFrame.setLayout(layout)

    def _construct_list(self):

        self.startLabel = QLabel("Start Time")
        self.endLabel = QLabel("End Time")
        self.scriptLabel = QLabel("Script")
        self.colorLabel = QLabel("Color")
        labels = [self.startLabel, self.endLabel, self.scriptLabel, self.colorLabel]
        
        layout = QHBoxLayout()
        layout.addSpacing(10)

        for i,label in enumerate(labels):
            
            if i == 1:
                layout.addSpacing(10)
            layout.addWidget(label)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            label.setStyleSheet("font-weight: bold;")        
            
            if i != len(labels) - 1 :
                frame = QFrame()
                frame.setFrameShape(QFrame.VLine)
                frame.setStyleSheet("background-color: white;")
                frame.setFixedWidth(1)
                layout.addWidget(frame)
        
    
        layout.setStretch(6,1)
            
        self.listFrame = QFrame()
        self.listFrame.setStyleSheet(" "
        "background-color: rgb(60,60,60);"
        "border-top-right-radius: 12px ; "
        "border-top-left-radius: 12px;")
        self.listFrame.setLayout(layout)

        self.list = QListWidget()

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.listFrame)
        vLayout.addWidget(self.list)
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(0,0,0,0)
        self.listWidget = QWidget()
        self.listWidget.setLayout(vLayout)

    def _signals_and_slots(self):
        
        self.control_button.clicked.connect(self.control_clicked)
        self.forward_button.clicked.connect(self.forward_or_bacward)
        self.backward_button.clicked.connect(self.forward_or_bacward)
        self.take_button.clicked.connect(self.take_clicked)
        self.cut_button.clicked.connect(self.cut_clicked)

        self.playerWidget.player.durationChanged.connect(self.update_duration)
        self.playerWidget.player.positionChanged.connect(self.update_position)
        self.playerWidget.slider.valueChanged.connect(self.slider_moved)
        self.playerWidget.slider.sliderReleased.connect(self.slider_released)

        self.volume_slider.valueChanged.connect(lambda val: self.playerWidget.audioPlayer.setVolume(val / self.volume_slider.maximum()))
        self.volume_slider.valueChanged.connect( lambda val: self.volume_text.setText(str(val)))

        self.segmented_bar.segmentClicked.connect(self.color_segment_clicked)
        self.segmented_bar.segmentDoubleClicked.connect(self.color_segment_double_clicked)
     
    def actions_and_menu(self):

        
        load_action = QAction("&Load Video",self)
        load_action.setShortcut(Qt.CTRL | Qt.Key_A)
        load_action.triggered.connect(self.open_file)
        
        help_action = QAction("&Get Help",self)
        help_action.setShortcut(Qt.CTRL | Qt.Key_H)
        help_action.triggered.connect(self.help)

        export_action = QAction("&Export to CSV file",self)
        export_action.setShortcut(Qt.CTRL | Qt.Key_S)
        export_action.triggered.connect(self.save)

        append_action = QAction("&Append from CSV file",self)
        append_action.setShortcut(Qt.CTRL | Qt.Key_E)
        append_action.triggered.connect(self.append_csv)

        import_action = QAction("&Import from CSV file",self)
        import_action.setShortcut(Qt.CTRL | Qt.Key_D)
        import_action.triggered.connect(self.import_csv)



        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        help_menu = menu.addMenu("&Help")

        file_menu.addAction(load_action)
        file_menu.addAction(export_action)
        file_menu.addAction(append_action)
        file_menu.addAction(import_action)
        help_menu.addAction(help_action)

    def start_thread(self, listWidget: CutWidgets):
        
        self.thread = QThread()
        self.worker = Worker(listWidget.cut, self.model)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(lambda text : self.thread_success(text,listWidget))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.threads.append(self.thread)
        self.thread.finished.connect(lambda thr=self.thread: self.threads.remove(thr))


        self.worker.error.connect(lambda _ : self.thread_error(listWidget))
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)


        self.thread.start()

    def listWidget_signals(self,listedItemWidget):

        self.list_item_widgets.append(listedItemWidget)
        self.list_item_widgets.sort(key= lambda x : x.cut.start_time)
        listedItemWidget.addList(self.list_item_widgets.index(listedItemWidget))

        #Signals of cutWidget instance
        listedItemWidget.colorButton.customClicked.connect(lambda time: self.color_button_clicked(time, self.list.row(self.list.itemAt(listedItemWidget.pos()))))
        listedItemWidget.colorButton.customDoubleClicked.connect(lambda time: self.color_button_double_clicked(time,self.list.row(self.list.itemAt(listedItemWidget.pos()))))
        listedItemWidget.itemRemoved.connect(self.item_removed)
        listedItemWidget.script.clicked.connect(lambda: self.dialog(listedItemWidget))
        listedItemWidget.start_time_button.clicked.connect(lambda : self.start_time_dialog(listedItemWidget))
        listedItemWidget.end_time_button.clicked.connect(lambda : self.end_time_dialog(listedItemWidget))

    #Slot
    def control_clicked(self):
        
        if self.playerWidget.player.isPlaying():
            self.control_button.setIcon(QIcon("icons\control.png"))
            self.playerWidget.player.pause()
            self.control_button_isPaused = True
        else:
            self.control_button.setIcon(QIcon("icons\control-pause.png"))
            self.playerWidget.player.play()
            self.control_button_isPaused = False

    #Slot
    def forward_or_bacward(self):

        if self.sender() == self.forward_button :
            self.playerWidget.player.setPosition(self.playerWidget.player.position() + 10000) #forwarding 10sec
        elif self.sender() == self.backward_button :
             self.playerWidget.player.setPosition(self.playerWidget.player.position() - 10000) # going backward 10sec

    #Slot
    def update_duration(self,time):
        self.playerWidget.slider.setMaximum(time)
        self.playerWidget.total_time.setText(AnnotationWindow.time_converter(time))
        self.segmented_bar.set_duration(time)
        self.segmented_bar.update()

    #Slot
    def update_position(self,pos):

        self.playerWidget.current_time.setText(AnnotationWindow.time_converter(pos))
        
        self.playerWidget.slider.blockSignals(True)
        self.playerWidget.slider.setValue(pos)
        self.playerWidget.slider.blockSignals(False)

    #Slot
    def slider_moved(self,pos):
        self.playerWidget.player.setPosition(pos)
        self.playerWidget.player.pause()

    #Slot
    def slider_released(self):
        if not self.control_button_isPaused:
            self.playerWidget.player.play()
            
    #Slot
    def take_clicked(self):
        self.take_button.setDisabled(True)
        self.cut_button.setDisabled(False)

        self.start_time = self.playerWidget.player.position()
    
    #Slot(and signal connections of ListItemWidget instance)
    def cut_clicked(self):
        self.take_button.setDisabled(False)
        self.cut_button.setDisabled(True)

        self.end_time = self.playerWidget.player.position()
 
        color = self.colors[self.color_index]
        self.color_index =  (self.color_index + 1) % len(self.colors)

        cut = Cut(self.start_time,self.end_time,color,self.playerWidget.player.source().toLocalFile() )

        self.segmented_bar.addSegment(cut)
        listedItemWidget = CutWidgets(cut,self.list)
        self.listWidget_signals(listedItemWidget)

        self.start_thread(listedItemWidget)
        self.start_time, self.end_time = 0, 0

    #Slot
    def color_button_clicked(self,time,index):
        self.playerWidget.player.setPosition(time)
        self.control_button.setIcon(QIcon("icons\control-pause.png"))
        self.playerWidget.player.play()
        self.list.setCurrentRow(index)

    #Slot
    def color_button_double_clicked(self,time,index):
        self.playerWidget.player.setPosition(time)
        self.control_button.setIcon(QIcon("icons\control.png"))
        self.playerWidget.player.pause()
        self.list.setCurrentRow(index)

    #Slot
    def color_segment_clicked(self,index,time):
        self.playerWidget.player.setPosition(time)
        self.control_button.setIcon(QIcon("icons\control-pause.png"))
        self.playerWidget.player.play()
        self.list.setCurrentRow(index)

    #Slot
    def color_segment_double_clicked(self,index,time):
        self.playerWidget.player.setPosition(time)
        self.control_button.setIcon(QIcon("icons\control.png"))
        self.playerWidget.player.pause()
        self.list.setCurrentRow(index)

    #Slot
    def item_removed(self,index):
        self.segmented_bar.removeSegment(index)
        self.list_item_widgets.pop(index)

    #Slot(Dialog)
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "All files (*.*);; mp4 Video (*.mp4);;mp3 Audio (*.mp3);;Movie files (*.mov);;",
        )

        if path:
            self.playerWidget.player.setSource(QUrl.fromLocalFile(path))
        
        self.control_button.setIcon(QIcon("icons\control-pause.png"))
        self.playerWidget.player.play()
    
    #Slot(Dialog)
    def save(self):
        
        file_path, _ = QFileDialog.getSaveFileName(
        self,
        "Save CSV",
        "", 
        "CSV Files (*.csv);;All Files (*)"
    )
        if file_path:  
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["start", "end", "text"])
                for cut in self.segmented_bar.segments:
                    writer.writerow([AnnotationWindow.time_converter(cut.start_time), AnnotationWindow.time_converter(cut.end_time), cut.script])

    #Slot(Dialog)
    def help(self):
        button = QMessageBox.information(
            self,
            "Need Help?",
            "This annotation application was created for research projects conducted at Hacettepe University by Erdem Mirza Kısa. " \
            "If you encounter any errors or need assistance, please feel free to contact me:" \
            "\n\ne-mail: erdem.mirzak@gmail.com",
        )

    #Slot(Dialog)
    def dialog(self,listedItem):
        
        if  self.transcript_dialog != None :
            self.transcript_dialog.close()

        dlg = CustomDialog(listedItem,self)
        self.transcript_dialog = dlg

        if dlg.exec():
            listedItem.script.setText(dlg.textEdit.toPlainText())
            listedItem.cut.set_script(dlg.textEdit.toPlainText())
        else:
            listedItem.script.setText(listedItem.script.text())
            listedItem.cut.set_script(listedItem.script.text())
        
        self.transcript_dialog = None

    #Slot(Dialog)
    def start_time_dialog(self,listedItem):

        if self.time_dialog is not None:
            self.time_dialog.close()

        dialog = QDialog(self)
        self.time_dialog = dialog
        dialog.setWindowTitle("Tweak the Time")

        layout = QVBoxLayout(dialog)

        current_text = listedItem.start_time_button.text()
        parts = current_text.split(":")
        if len(parts) == 3:
            h, m, s = map(int, parts)
        else:
            h, m, s = 0, 0, 0

        time_edit = QTimeEdit(QTime(h, m, s))
        time_edit.setDisplayFormat("HH:mm:ss")
        time_edit.setKeyboardTracking(False)

        QTimer.singleShot(0, lambda: time_edit.setCurrentSection(QTimeEdit.SecondSection))
        layout.addWidget(time_edit)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(ok_button)
        buttonLayout.addWidget(cancel_button)

        layout.addLayout(buttonLayout)

        ok_button.clicked.connect(lambda: dialog.accept())
        cancel_button.clicked.connect(lambda: dialog.reject())

        dialog.setLayout(layout)
        dialog.setModal(False)

        dialog.show()

        def finished(result):
            if result:
                new_time = time_edit.time().toString("HH:mm:ss")
                listedItem.start_time_button.setText(new_time)
                listedItem.script.setText("...")
                listedItem.cut.set_script("...")
                listedItem.cut.set_start(AnnotationWindow.reverse_time_converter(new_time))
                self.segmented_bar.update()
                self.start_thread(listedItem)
            self.time_dialog = None

        dialog.finished.connect(finished)

    #Slot(Dialog)
    def end_time_dialog(self, listedItem):
        if self.time_dialog is not None:

            self.time_dialog.close()
        dialog = QDialog(self)
        self.time_dialog = dialog
        dialog.setWindowTitle("Tweak the Time")

        layout = QVBoxLayout(dialog)

        current_text = listedItem.end_time_button.text()
        parts = current_text.split(":")
        if len(parts) == 3:
            h, m, s = map(int, parts)
        else:
            h, m, s = 0, 0, 0

        time_edit = QTimeEdit(QTime(h, m, s))
        time_edit.setDisplayFormat("HH:mm:ss")
        time_edit.setKeyboardTracking(False)

        QTimer.singleShot(0, lambda: time_edit.setCurrentSection(QTimeEdit.SecondSection))
        layout.addWidget(time_edit)

        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(ok_button)
        buttonLayout.addWidget(cancel_button)

        layout.addLayout(buttonLayout)

        ok_button.clicked.connect(lambda: dialog.accept())
        cancel_button.clicked.connect(lambda: dialog.reject())

        dialog.setLayout(layout)
        dialog.setModal(False)

        dialog.show()

        def finished(result):
            if result:
                new_time = time_edit.time().toString("HH:mm:ss")
                listedItem.end_time_button.setText(new_time)
                listedItem.script.setText("...")
                listedItem.cut.set_script("...")
                listedItem.cut.set_end(AnnotationWindow.reverse_time_converter(new_time))
                self.segmented_bar.update()
                self.start_thread(listedItem)
            self.time_dialog = None

        dialog.finished.connect(finished)
        
    # Slot(Dialog)
    def append_csv(self):
 
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            cuts = []
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # skipping header row
                for row in reader:
                    start = AnnotationWindow.reverse_time_converter(row[0])
                    end = AnnotationWindow.reverse_time_converter(row[1])
                    text = row[2]
                    color = self.colors[self.color_index]
                    self.color_index =  (self.color_index + 1) % len(self.colors)
                    cuts.append(Cut(start, end, color,script=text))


            self.segmented_bar.segments.extend(cuts)
            self.segmented_bar.segments.sort(key = lambda x : x.start_time)
            self.segmented_bar.update()

            for cut in cuts:

                listedItemWidget = CutWidgets(cut,self.list)
                self.listWidget_signals(listedItemWidget)
                listedItemWidget.script.setText(cut.get_script())

    # Slot(Dialog)
    def import_csv(self):

        file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Open CSV",
        "",
        "CSV Files (*.csv);;All Files (*)"
        )
        self.color_index = 0

        if file_path:
            cuts = []
            with open(file_path, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # skipping header row
                for row in reader:
                    start = AnnotationWindow.reverse_time_converter(row[0])
                    end = AnnotationWindow.reverse_time_converter(row[1])
                    text = row[2]
                    color = self.colors[self.color_index]
                    self.color_index =  (self.color_index + 1) % len(self.colors)
                    cuts.append(Cut(start, end, color,script=text))
            for widget in self.list_item_widgets:
                index = widget.parent.row(widget.item)
                widget.parent.takeItem(index)
                widget.item = None
                widget.deleteLater()
            self.list_item_widgets.clear()
            self.segmented_bar.segments.clear()
            self.segmented_bar.segments.extend(cuts)
            self.segmented_bar.update()
        
            for cut in cuts:
            
                listedItemWidget = CutWidgets(cut,self.list)
                self.listWidget_signals(listedItemWidget)
                listedItemWidget.script.setText(cut.get_script())
        

        
            
    #Slot
    def thread_success(self,text,listWidget):
        try:
            if listWidget and listWidget.script:
                listWidget.script.setText(text)
                listWidget.cut.set_script(text)
        except RuntimeError:
            pass
        
    #Slot
    def thread_error(self,listWidget):
        try:
            if listWidget and listWidget.script:
                listWidget.script.setText("xxx")
                listWidget.cut.set_script("xxx")
        except:
            pass
    
    @staticmethod
    def time_converter(time):

        seconds = time // 1000
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @staticmethod
    def reverse_time_converter(str):
        h, m, s = map(int, str.split(":"))
        return ((h * 3600) + (m * 60) + s) * 1000
    

if __name__ == "__main__" :
    
    app = QApplication([])
    window = AnnotationWindow()
    window.showMaximized()
    app.exec()