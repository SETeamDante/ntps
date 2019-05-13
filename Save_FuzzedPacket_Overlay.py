import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QLabel

class Saved_FuzzPacket_Overlay(QMainWindow):


    def __init__(self):
        super().__init__()


        self.title = 'Save Fuzzed Packets'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 160
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("QMainWindow {background-color: rgb(216,228,237);}")



        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create Fuzzed PCAP Name textbox and label
        self.HNlabel = QLabel("Fuzzed PCAP\nName", self)
        self.HNlabel.move(7, 20)
        self.HookName = QLineEdit(self)
        self.HookName.setPlaceholderText("PCAP File")
        self.HookName.move(90, 20)
        self.HookName.resize(180, 25)


        # Create PCAP Description textbox and label
        self.HDlabel = QLabel("Description", self)
        self.HDlabel.move(7, 60)
        self.HookDescription = QLineEdit(self)
        self.HookDescription.setPlaceholderText("Description")
        self.HookDescription.move(90, 60)
        self.HookDescription.resize(180, 25)

        # Create a Save button in the window
        self.saveButton = QPushButton('Save', self)
        self.saveButton.move(240, 130)
        self.saveButton.resize(65, 25)

        # Create a Cancel button in the window
        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.move(300, 130)
        self.cancelButton.resize(65, 25)

        self.show()

#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = App()
    #sys.exit(app.exec_())
