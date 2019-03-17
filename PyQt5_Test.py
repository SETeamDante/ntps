from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import  QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys
import PCAPView
from PCAPView import *



class OptionViewClass(QFrame):
    def __init__(self, ContentView):
        super().__init__()
        #Pass reference of the ContentViewClass ContentView Layer
        self.ContentView = ContentView
        # Add a style to MainView (TO BE CHANGE)
        # TODO
        self.setStyleSheet("margin:5px; border:1px solid rgb(0, 10, 10); ")
        self.initUI()
        # ContentView  = ContentViewClass()

    def initUI(self):
        #Creates a new Vertical BoxLayout
        self.OptionView = QVBoxLayout(self)
        # Creates 4 Button Widget while also setting the label
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        self.btn3 = QPushButton("LivePacket")
        self.btn4 = QPushButton("Pcap")
        #Adds 4 button QWidgets to OptionView(BoxLayout)
        self.OptionView.addWidget(self.btn)
        self.OptionView.addWidget(self.btn2)
        self.OptionView.addWidget(self.btn3)
        self.OptionView.addWidget(self.btn4)
        #Connects a button with a function
        #-clicked.connect can only pass function calls and no primitives
        #-so we are using lambda to mask the arguments as a Call
        self.btn.clicked.connect(lambda : self.on_click(0))
        self.btn2.clicked.connect(lambda :self.on_click(1))
        self.btn3.clicked.connect(lambda :self.on_click(2))
        self.btn4.clicked.connect(lambda :self.on_click(3))
        self.setLayout(self.OptionView)

    @pyqtSlot()
    def on_click(self, number):
        print('PyQt5 button click')
        #Debbuging purposes
        print(number)
        #Changes the current index of a StackedLayout
        self.ContentView.setCurrentIndex(number)



class ContentViewClass(QWidget):
    def __init__(self):
        #Create a new StackedLayout
        self.ContentView = QStackedLayout()
        super().__init__()
        self.setWindowTitle("Content")
        #Add a style to ContentViewClass (TO BE CHANGE)
        #TODO
        # self.setStyleSheet("margin:1px; border:1px solid rgb(0, 0, 255); ")
        # Awakens and stores location of HookCollectionViewClass
        self.VHookCollection = HookCollectionViewClass()
        # Awakens and stores location of PcapViewClass
        self.VPcap = PcapViewClass()
        self.VHook = HookViewClass()
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):

        #Add QFrame( Or QWidget) to ContentView(StackLayout) in a Queue form
        self.ContentView.addWidget(self.VHookCollection)
        self.ContentView.addWidget(self.VHook)
        self.ContentView.addWidget(self.VPcap)
        # Inject ContentView Layout to the QFrame ( or QWidget)
        self.setLayout(self.ContentView)


class HookCollectionViewClass(QWidget):
    def __init__(self):
        super().__init__()
        #Calls function to begging making the view
        self.setStyleSheet('QWidget { font: 20px }')
        self.HookCollectionView = QGridLayout(self)
        self.initUI()

    def initUI(self):
        # --------------------------

        self.addHookButton = QPushButton("+Hook")
        self.editHookButton = QPushButton("Edit")
        self.deleteHookButton = QPushButton("Delete")
        self.searchLabel = QLabel("Search")
        self.searchBox = QLineEdit()

        self.layout = QGridLayout()
        self.layout.addWidget(self.addHookButton, 1, 0)
        self.layout.addWidget(self.editHookButton, 1, 1)
        self.layout.addWidget(self.deleteHookButton, 1, 2)
        self.layout.setColumnMinimumWidth(4, 100)
        self.layout.addWidget(self.searchLabel, 1, 5)
        self.layout.addWidget(self.searchBox, 1, 6)

        # ---------------

        self.HookCollectionPropertiesArea = QTreeWidget(self)
        self.HookCollectionPropertiesArea.setSelectionMode(QAbstractItemView.NoSelection)
        self.HookCollectionPropertiesArea.setAlternatingRowColors(True)
        self.HookCollectionPropertiesArea.setFixedWidth(700)
        self.labels = ["Hook ", "Description", "Hook status", "Hook Execution Sequence"]
        self.HookCollectionPropertiesArea.setHeaderLabels(self.labels)
        self.test = QTreeWidgetItem(["Hook1", "Description","Enable","1"])
        self.test2 = QTreeWidgetItem(["Hook2", "Description","Enable","2"])
        self.HookCollectionPropertiesArea.addTopLevelItem(self.test)
        self.HookCollectionPropertiesArea.addTopLevelItem(self.test2)
        self.test.addChild(self.test2)
        # -------------------------------
        self.HookCollectionPropertiesArea5 = QTreeWidget(self)
        self.HookCollectionPropertiesArea5.setHeaderLabels(["Hook Collection", "No. of Hooks", "Hook Collection status", "Hook Collection Execution Sequence"])
        self.HookCollectionPropertiesArea5.setAlternatingRowColors(True)
        self.HookCollectionPropertiesArea5.setSelectionMode(QAbstractItemView.NoSelection)
        self.HookCollectionPropertiesArea5.setFixedWidth(1000)
        self.test5 = QTreeWidgetItem(["Hook Collection 1", "2","Enable","1"])
        self.test55 = QTreeWidgetItem()
        self.HookCollectionPropertiesArea5.addTopLevelItem(self.test5)
        self.test5.addChild(self.test55)
        self.HookCollectionPropertiesArea5.setItemWidget(self.test55, 0, self.HookCollectionPropertiesArea)
        # -------------------------------
        self.HookCollectionView.addWidget(self.HookCollectionPropertiesArea5, 1, 0, 1, 1)
        self.HookCollectionView.addLayout(self.layout, 0, 0, 1, 1)
        self.setLayout(self.HookCollectionView)

class HookViewClass(QWidget):
    def __init__(self):
        super().__init__()        #Calls function to begging making the view
        self.setStyleSheet('QWidget { font: 20px }')
        self.HookView = QGridLayout(self)
        self.initUI()

    def initUI(self):
        # --------------------------

        self.addHookButton = QPushButton("+Hook")
        self.editHookButton = QPushButton("Edit")
        self.deleteHookButton = QPushButton("Delete")
        self.searchLabel = QLabel("Search")
        self.searchBox = QLineEdit()

        self.layout = QGridLayout()
        self.layout.addWidget(self.addHookButton, 1, 0)
        self.layout.addWidget(self.editHookButton, 1, 1)
        self.layout.addWidget(self.deleteHookButton, 1, 2)
        self.layout.setColumnMinimumWidth(4, 100)
        self.layout.addWidget(self.searchLabel, 1, 5)
        self.layout.addWidget(self.searchBox, 1, 6)

        # ---------------

        self.HookPropertiesArea5 = QTreeWidget(self)
        # self.HookPropertiesArea5.setStyleSheet('QWidget { font: 29px }')
        self.HookPropertiesArea5.setHeaderLabels(["Hook", 'Description', 'Association to Hook Collection'])
        self.HookPropertiesArea5.setAlternatingRowColors(True)

        self.HookPropertiesArea5.setFixedWidth(1000)
        self.HookPropertiesArea5.resizeColumnToContents(1)


        # # Adds widgets to PcapView( a vertical Box Layout) in Queue form
        self.test5 = QTreeWidgetItem(["Hook1", "Description_of_Hook", "0"])
        self.test55 = QTreeWidgetItem()
        self.HookPropertiesArea5.addTopLevelItem(self.test5)
        # self.HookPropertiesArea5.setItemWidget(self.test5, 0, self.btn5)

        self.HookView.addWidget(self.HookPropertiesArea5, 1, 0, 1, 1)
        self.HookView.addLayout(self.layout, 0, 0, 1, 1)


        self.HookPropertiesArea5.adjustSize()
        self.setLayout(self.HookView)

class MainViewClass(QFrame):
    def __init__(self):
        super().__init__()
        #Set the Main window size ::: setGreometry(Location X, Location Y, Size X, Size Y)
        self.setGeometry(300, 100, 1100, 600)
        self.setWindowTitle("Network Traffic Protocol System")
        #Add a style to MainView (TO BE CHANGE)
        #TODO
        # self.setStyleSheet("margin:5px; border:5px solid rgb(255, 0, 0); ")
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):
        #Start GridLayout
        self.MainView = QGridLayout(self)
        # Initialize and stores location of ContentViewClass
        self.VContent = ContentViewClass()
        # Initialize and stores location of OptionViewClass while also sending ContentView layout information
        self.VOption = OptionViewClass(self.VContent.ContentView)
        #Adds widget(or frame) in a GridLayout ::: .addWidget(Qwidget or QFrame ,X ,Y ,SizeX ,SizeY):::X and Y start
        #top right
        self.MainView.addWidget(self.VOption,0,0,0,1 )
        self.MainView.addWidget(self.VContent, 1,1,1,5)
        #Inject MainView Layout to the Qframe ( or QWidget)
        self.setLayout(self.MainView)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    Main = MainViewClass()
    #Displays the MainView QFrame
    Main.show()
    #app.exec is necessary to keep the window open even after execution
    sys.exit(app.exec_())
