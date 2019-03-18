import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QLabel

class App(QMainWindow):


    def __init__(self):
        super().__init__()


        self.title = 'Create/Edit Hook'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 160
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("QMainWindow {background-color: rgb(216,228,237);}")
        # self.setStyleSheet("QMApplication {background-color: rgb(216,228,237);}")



        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create Hook Name textbox and label
        self.HNlabel = QLabel("Hook Name", self)
        self.HNlabel.move(7, 20)
        self.HookName = QLineEdit(self)
        self.HookName.setPlaceholderText("Hook Name")
        self.HookName.move(80, 20)
        self.HookName.resize(180, 25)


        # Create Hook Description textbox and label
        self.HDlabel = QLabel("Description", self)
        self.HDlabel.move(7, 60)
        self.HookDescription = QLineEdit(self)
        self.HookDescription.setPlaceholderText("Hook Description")
        self.HookDescription.move(80, 60)
        self.HookDescription.resize(180, 30)

        # Create Hook Path textbox
        self.HPlabel = QLabel("Hook Path", self)
        self.HPlabel.move(7, 100)
        self.HookPath = QLineEdit(self)
        self.HookPath.setPlaceholderText("Hook Path")
        self.HookPath.move(80, 100)
        self.HookPath.resize(160, 25)

        # Create a Browse button in the window
        self.browseButton = QPushButton('Browse', self)
        self.browseButton.move(300, 100)
        self.browseButton.resize(67, 25)

        # Create a Save button in the window
        self.saveButton = QPushButton('Save', self)
        self.saveButton.move(240, 130)
        self.saveButton.resize(65, 25)


        # Create a Cancel button in the window
        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.move(300, 130)
        self.cancelButton.resize(65, 25)

        self.show()
        #connect button to function on_click
        # self.browseButton.clicked.connect(self.on_click)



    # @pyqtSlot()
    # def on_click(self):
    #     textboxValue = self.textbox.text()
    #
    #
    #     QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
    #     self.textbox.setText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())