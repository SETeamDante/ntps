import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Hook Execution Error'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("QMessageBox {background-color: rgb(216,228,237);}")

        self.HookExecutionError = QMessageBox.warning(self, 'Hook Execution Error',
                                                 "There is another hook with that sequence number.  "
                                                 "Would you like to override the sequence number and update "
                                                 "the sequencing for the rest of hooks within this hook collection?",
                                                 QMessageBox.Yes | QMessageBox.No)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
