"""
MIT License

Copyright (c) 2025 Erdem Mirza

This file is part of the project and is licensed under the MIT License.
"""

from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox ,QApplication,QLabel
from cut_widgets import CutWidgets

class CustomDialog(QDialog):

    def __init__(self, listedItem : CutWidgets, parent = None ):
        super().__init__(parent)

        self.resize(400,100)
        self.setModal(False)
        self.setWindowTitle("Transcription")

        QBtn = (
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.label = QLabel("Edit the transcription if necessary:")
        self.textEdit = QTextEdit(listedItem.script.text())

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.show()



if __name__ == "__main__":
    
    app = QApplication([])
    window = CustomDialog()
    window.show()
    app.exec()