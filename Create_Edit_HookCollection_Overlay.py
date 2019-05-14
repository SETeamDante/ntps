import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QGroupBox, QGridLayout, QCheckBox, QPushButton


class HookCol_Overlay(QMainWindow):


    #def __init__(self):
        #super().__init__()
    def __init__(self, parent):
        super(HookCol_Overlay, self).__init__(parent)
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
        self.setWindowTitle(self.title)
        
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        
        layout = QGridLayout()
        self.widget.setLayout(layout)

        # Create Hook Collection Name textbox and label
        self.HCNlabel = QLabel("Hook Collection\nName", self)
        layout.addWidget(self.HCNlabel, 0, 0, 1, 1)
        self.HookCollectionName = QLineEdit(self)
        self.HookCollectionName.setPlaceholderText("Hook Collection Name")
        layout.addWidget(self.HookCollectionName, 0, 1, 1, 2)

        # Create Hook Collection Description textbox and label
        self.HCDlabel = QLabel("Description", self)
        layout.addWidget(self.HCDlabel, 1, 0, 1, 1)
        self.HookCollDescription = QLineEdit(self)
        self.HookCollDescription.setPlaceholderText("Hook Collection Description")
        layout.addWidget(self.HookCollDescription, 1, 1, 1, 2)
        
        # Create Hook Collection Description textbox and label
        self.statusLabel = QLabel("Status", self)
        layout.addWidget(self.statusLabel, 2, 0, 1, 1)
        self.status = QComboBox()
        self.status.addItem('Enabled')
        self.status.addItem('Disabled')
        layout.addWidget(self.status, 2, 1, 1, 2)

        # Create Execution Sequence textbox and label
        self.ExecSeqlabel = QLabel("Execution\nNumber", self)
        layout.addWidget(self.ExecSeqlabel, 3, 0, 1, 1)
        self.ExecSequence = QLineEdit(self)
        self.ExecSequence.setPlaceholderText("Enter Sequence No.")
        layout.addWidget(self.ExecSequence, 3, 1, 1, 2)
        
        layout.addWidget(HookList(), 4, 0, 2, 3)
        
        
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.saveHookCol)
        layout.addWidget(self.saveButton, 6, 1, 1, 1)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelHookCol)
        layout.addWidget(self.cancelButton, 6, 2, 1, 1)
        
        #self.show()
        
    def saveHookCol(self):
        print("Saved")
    
    def cancelHookCol(self):
        self.close()

class Area(QGroupBox):
    def __init__(self, title=None):
        super().__init__(title)

class HookList(Area):
    def __init__(self):
        super().__init__('Hook Selection')

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Field Hook'), 0, 0)
        field_names = ['icmp.type', 'icmp.code', 'icmp.checksum',
                       'icmp.ident', 'icmp.seq']
        for i, text in enumerate(field_names):
            layout.addWidget(QCheckBox(text), i+1, 0)

        layout.addWidget(QLabel('Status'), 0, 1)
        display_formats = ['Disabled', 'Enabled']
        for i in range(1, len(field_names)+1):
            combo_box = QComboBox()
            combo_box.addItems(display_formats)
            combo_box.setCurrentIndex(1)
            layout.addWidget(combo_box, i, 1)

        layout.addWidget(QLabel('Hook Execution Sequence'), 0, 2)
        masks = ['0', '0', '1', '0', '2']
        for i, text in enumerate(masks):
            layout.addWidget(QLineEdit(text), i+1, 2)

#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = HookCol_Overlay()
    #sys.exit(app.exec_())
