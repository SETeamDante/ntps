import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class Q_Err_Overlay(QWidget):

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
        self.QueueError = QMessageBox.warning(self, 'Queue Error Message',
                                                  "The queue has reached its capability.  "
                                                  "No new packets will be excepted until there is "
                                                  "space available.",
                                                  QMessageBox.Ok)
