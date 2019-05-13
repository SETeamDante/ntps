import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class Hook_Ex_Seq_Err_Overlay(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'title'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("QMessageBox {background-color: rgb(216,228,237);}")

        self.HookCollectionExecutionError = QMessageBox.warning(self, 'Hook Collection Execution Sequence Error',
                                                 "There is another collection with that sequence number.  "
                                                 "Would you like to override the sequence number and update the "
                                                 "sequencing for the rest of hook collections?",
                                                 QMessageBox.Yes | QMessageBox.No)

