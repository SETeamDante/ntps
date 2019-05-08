import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class App(QWidget):

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

        self.ProxyDisabled = QMessageBox.information(self, 'Proxy Disabled Notification',
                                                    "Proxy behavior has been disabled.  "
                                                    "The System has restored to the previous Proxy settings and it will"
                                                    "stop appending packet information to the live Traffic PCAP file.",
                                                    QMessageBox.Ok)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
