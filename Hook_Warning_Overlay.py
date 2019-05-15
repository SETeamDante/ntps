import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

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

        self.QueueError = QMessageBox.critical(self, 'Hook Error Message',
                                                                "This hook does not follow "
                                                                "the proper guidelines.",
                                                                QMessageBox.Ok)
        
#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = Q_Err_Overlay()
    #sys.exit(app.exec_())