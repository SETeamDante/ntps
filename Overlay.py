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

        self.HookExecutionError = QMessageBox.warning(self, 'Hook Execution Error',
                                                 "There is another hook with that sequence number.  "
                                                 "Would you like to override the sequence number and update "
                                                 "the sequencing for the rest of hooks within this hook collection?",
                                                 QMessageBox.Yes | QMessageBox.No)

        self.HookCollectionExecutionError = QMessageBox.warning(self, 'Hook Collection Execution Sequence Error',
                                                 "There is another collection with that sequence number.  "
                                                 "Would you like to override the sequence number and update the "
                                                 "sequencing for the rest of hook collections?",
                                                 QMessageBox.Yes | QMessageBox.No)

        self.QueueError = QMessageBox.critical(self, 'Hook Collection Execution Sequence Error',
                                                                "The queue has reached its capability.  "
                                                                "No new packets will be excepted until there is "
                                                                "space available.",
                                                                QMessageBox.Ok)

        self.ProxyEnabled = QMessageBox.information(self, 'Proxy Enabled Notification',
                                                    "Proxy behavior has been enabled.  "
                                                    "The System has backed up the System’s Proxy settings and will "
                                                    "restore to it when the Proxy behavior is disabled.",
                                                    QMessageBox.Ok)

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