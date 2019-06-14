import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QComboBox, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QGroupBox, QGridLayout, QCheckBox, QPushButton
from HookSub.HookCollectionCatalog import HookCollectionCatalog
from HookSub.HookCatalog import HookCatalog
from HookSub.HookCollection import HookCollection
from HookSub.Hook import Hook
from Controller import  Controller


class HookCol_Overlay(QMainWindow):

    def __init__(self, parent, Controller):
        super(HookCol_Overlay, self).__init__(parent)
        self.title = 'Create Hook Collection'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 300
        self.parentView = parent
        self.Controller = Controller
        self.hookItemList = []
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
        self.status.addItem('Disabled')
        self.status.addItem('Enabled')
        layout.addWidget(self.status, 2, 1, 1, 2)

        # Create Execution Sequence textbox and label
        self.ExecSeqlabel = QLabel("Execution\nNumber", self)
        layout.addWidget(self.ExecSeqlabel, 3, 0, 1, 1)
        self.ExecSequence = QLineEdit(self)
        self.ExecSequence.setPlaceholderText("Enter Sequence No.")
        layout.addWidget(self.ExecSequence, 3, 1, 1, 2)
        
        layout.addWidget(HookList(self.Controller, self.hookItemList), 4, 0, 2, 3)
        
        
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.saveHookCol)
        layout.addWidget(self.saveButton, 6, 1, 1, 1)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelHookCol)
        layout.addWidget(self.cancelButton, 6, 2, 1, 1)

        
    def saveHookCol(self):
        status = False
        if self.status.currentText() == 'Enabled':
            status = True
            
        newCollection = HookCollection(self.HookCollectionName.text(), self.HookCollDescription.text(), status, self.ExecSequence.text())
        hooksInCollection = [] 
        for i in self.hookItemList:
            if i.checkBox.checkState():
                if i.combo_box.currentText() == 'Enabled':
                    i.hook.status = True
                else: 
                    i.hook.status = False
                i.hook.execNum = i.lineEdit.text()
                hooksInCollection.append(i.hook)
        newCollection.content = hooksInCollection
        
        self.Controller.hookCollectionCatalog.addHookCollection(newCollection)
        self.parentView.updateView()
        self.close()
    
    def cancelHookCol(self):
        self.close()

class Edit_HookCol_Overlay(QMainWindow):

    def __init__(self, parent, Controller, index):
        super(Edit_HookCol_Overlay, self).__init__(parent)
        self.title = 'Edit Hook Collection'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 300
        self.parentView = parent
        self.Controller = Controller
        self.index = index
        self.hookItemList = []
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
        self.HookCollectionName.setText(self.Controller.hookCollectionCatalog.hookCollectionCatalog[self.index].name)
        layout.addWidget(self.HookCollectionName, 0, 1, 1, 2)

        # Create Hook Collection Description textbox and label
        self.HCDlabel = QLabel("Description", self)
        layout.addWidget(self.HCDlabel, 1, 0, 1, 1)
        self.HookCollDescription = QLineEdit(self)
        self.HookCollDescription.setText(self.Controller.hookCollectionCatalog.hookCollectionCatalog[self.index].description)
        layout.addWidget(self.HookCollDescription, 1, 1, 1, 2)
        
        # Create Hook Collection Description textbox and label
        self.statusLabel = QLabel("Status", self)
        layout.addWidget(self.statusLabel, 2, 0, 1, 1)
        self.status = QComboBox()
        self.status.addItem('Disabled')
        self.status.addItem('Enabled')
        if self.Controller.hookCollectionCatalog.hookCollectionCatalog[self.index].status:
            self.status.setCurrentIndex(1)
        layout.addWidget(self.status, 2, 1, 1, 2)

        # Create Execution Sequence textbox and label
        self.ExecSeqlabel = QLabel("Execution\nNumber", self)
        layout.addWidget(self.ExecSeqlabel, 3, 0, 1, 1)
        self.ExecSequence = QLineEdit(self)
        self.ExecSequence.setText(self.Controller.hookCollectionCatalog.hookCollectionCatalog[self.index].execNum)
        layout.addWidget(self.ExecSequence, 3, 1, 1, 2)
        
        layout.addWidget(HookList(self.Controller, self.hookItemList), 4, 0, 2, 3)
        
        for item in self.hookItemList:
            if item.hook in self.Controller.hookCollectionCatalog.hookCollectionCatalog[self.index].content:
                item.checkBox.setChecked(True)
            if item.hook.status:
                item.combo_box.setCurrentIndex(1)
        
        self.saveButton = QPushButton('Save')
        self.saveButton.clicked.connect(self.saveHookCol)
        layout.addWidget(self.saveButton, 6, 1, 1, 1)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelHookCol)
        layout.addWidget(self.cancelButton, 6, 2, 1, 1)

        
    def saveHookCol(self):
        status = False
        if self.status.currentText() == 'Enabled':
            status = True
            
        newCollection = HookCollection(self.HookCollectionName.text(), self.HookCollDescription.text(), status, self.ExecSequence.text())
        hooksInCollection = [] 
        for i in self.hookItemList:
            if i.checkBox.checkState():
                if i.combo_box.currentText() == 'Enabled':
                    i.hook.status = True
                else: 
                    i.hook.status = False
                i.hook.execNum = i.lineEdit.text()
                hooksInCollection.append(i.hook)
        newCollection.content = hooksInCollection
        
        self.Controller.hookCollectionCatalog.hookCollectionCatalog[self.index] = newCollection
        self.parentView.updateView()
        self.close()
    
    def cancelHookCol(self):
        self.close()

class Area(QGroupBox):
    def __init__(self, title=None):
        super().__init__(title)

class HookList(Area):
    def __init__(self, Controller, hookItemList):
        super().__init__('Hook Selection')

        layout = QGridLayout()
        self.hookItemList = hookItemList
        self.Controller = Controller
        self.setLayout(layout)

        layout.addWidget(QLabel('Hook'), 0, 0, 1, 1)
        layout.addWidget(QLabel('Status'), 0, 1, 1, 1)
        layout.addWidget(QLabel('Hook Execution Sequence'), 0, 2, 1, 1)
        layout.setColumnStretch (0, 1)
        layout.setColumnStretch (1, 1)
        layout.setColumnStretch (2, 1)
        index = 1
        
        for i in self.Controller.hookCatalog.hookCatalog:
            hookItem = HookItem(i)
            hookItemList.append(hookItem)
            layout.addWidget(hookItem, index, 0, 1, 3)
            index += 1
            
class HookItem(QWidget):
    def __init__(self, Hook):
        super().__init__()
        layout = QGridLayout()
        self.hook = Hook
        self.setLayout(layout)
        
        self.checkBox = QCheckBox(self.hook.name)
        self.checkBox.setTristate(False)
        layout.addWidget(self.checkBox, 0, 0, 1, 1)
        
        display_formats = ['Disabled', 'Enabled']
        self.combo_box = QComboBox()
        self.combo_box.addItems(display_formats)
        layout.addWidget(self.combo_box, 0, 1, 1, 1)
        
        self.lineEdit = QLineEdit(str(self.hook.execNum))
        layout.addWidget(self.lineEdit, 0, 2, 1, 1)
        
        layout.setColumnStretch (0, 1)
        layout.setColumnStretch (1, 1)
        layout.setColumnStretch (2, 1)

