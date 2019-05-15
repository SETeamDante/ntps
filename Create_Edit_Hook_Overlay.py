import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QLabel, QFileDialog, QGridLayout
from HookSub.Hook import Hook
from Hook_Warning_Overlay import Hook_Warning_Overlay
from HookSub.HookCatalog import HookCatalog

class Hook_Overlay(QMainWindow):


    #def __init__(self):
        #super().__init__()
    def __init__(self, parent, hookCatalog):
        super(Hook_Overlay, self).__init__(parent)
        self.title = 'Create/Edit Hook'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 160
        self.parentView = parent
        self.catalog = hookCatalog
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("QMainWindow {background-color: rgb(216,228,237);}")
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        
        layout = QGridLayout()
        self.widget.setLayout(layout)

        # Create Hook Name textbox and label
        self.HNlabel = QLabel("Hook Name", self)
        layout.addWidget(self.HNlabel, 0, 0, 1, 1)
        self.HookName = QLineEdit(self)
        self.HookName.setPlaceholderText("Hook Name")
        layout.addWidget(self.HookName, 0, 1, 1, 2)


        # Create Hook Description textbox and label
        self.HDlabel = QLabel("Description", self)
        layout.addWidget(self.HDlabel, 1, 0, 1, 1)
        self.HookDescription = QLineEdit(self)
        self.HookDescription.setPlaceholderText("Hook Description")
        layout.addWidget(self.HookDescription, 1, 1, 1, 2)

        # Create Hook Path textbox
        self.HPlabel = QLabel("Hook Path", self)
        layout.addWidget(self.HPlabel, 2, 0, 1, 1)
        self.HookPath = QLineEdit(self)
        self.HookPath.setPlaceholderText("Hook Path")
        layout.addWidget(self.HookPath, 2, 1, 1, 2)

        # Create a Browse button in the window
        self.browseButton = QPushButton('Browse', self)
        self.browseButton.clicked.connect(self.browseHook)
        layout.addWidget(self.browseButton, 2, 3, 1, 1)

        # Create a Save button in the window
        self.saveButton = QPushButton('Save', self)
        self.saveButton.clicked.connect(self.saveHook)
        layout.addWidget(self.saveButton, 3, 2, 1, 1)


        # Create a Cancel button in the window
        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.cancelHook)
        layout.addWidget(self.cancelButton, 3, 3, 1, 1)

        self.show()
    
    
    def browseHook(self):
        hookName = QFileDialog.getOpenFileName(self, 'Select Hook', 'c:\\home\\student', '')
        self.HookPath.setText(hookName[0])
        
    def saveHook(self):
        newHook = Hook(self.HookName.text(), self.HookDescription.text(), self.HookPath.text())
        if newHook.checkHookProtocol():
            self.catalog.addHook(newHook)
            self.parentView.updateView()
            self.close()
            
        else:
            warning = Hook_Warning_Overlay()
        
    
    def cancelHook(self):
        self.close()

#if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #ex = Hook_Overlay()
    #sys.exit(app.exec_())
