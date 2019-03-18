import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Create/Edit Hook Collection'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("QMainWindow {background-color: rgb(216,228,237);}")

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)


        # Create Hook Collection Name textbox and label
        self.HCNlabel = QLabel("Hook Collection\nName", self)
        self.HCNlabel.move(7, 20)
        self.HookCollectionName = QLineEdit(self)
        self.HookCollectionName.setPlaceholderText("Hook Collection Name")
        self.HookCollectionName.move(110, 20)
        self.HookCollectionName.resize(180, 25)

        # Create Hook Collection Description textbox and label
        self.HCDlabel = QLabel("Description", self)
        self.HCDlabel.move(7, 60)
        self.HookCollDescription = QLineEdit(self)
        self.HookCollDescription.setPlaceholderText("Hook Collection Description")
        self.HookCollDescription.move(110, 60)
        self.HookCollDescription.resize(180, 25)

        layout = QHBoxLayout()
        # Create Hook Collection Description textbox and label
        self.statusLabel = QLabel("Status", self)
        self.statusLabel.move(7, 100)
        self.status = QComboBox(self.widget)
        self.status.addItem('Enabled')
        self.status.addItem('Disabled')
        self.status.move(110, 100)
        self.status.resize(180, 25)

        layout.addWidget(self.status)
        self.setWindowTitle(self.title)

        # Create Execution Sequence textbox and label
        self.ExecSeqlabel = QLabel("Execution\nNumber", self)
        self.ExecSeqlabel.move(7, 140)
        self.ExecSequence = QLineEdit(self)
        self.ExecSequence.setPlaceholderText("Enter Sequence No.")
        self.ExecSequence.move(110, 140)
        self.ExecSequence.resize(180, 30)

        self.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())