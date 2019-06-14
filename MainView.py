
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys
from PacketView import LivePacketView, PCAPView
from Overlays.Create_Edit_Hook_Overlay import Hook_Overlay, Edit_Hook_Overlay
from Overlays.Create_Edit_HookCollection_Overlay import HookCol_Overlay, Edit_HookCol_Overlay
from HookSub.HookCatalog import HookCatalog
from HookSub.HookCollectionCatalog import HookCollectionCatalog
#############################################
from Controller import  Controller
from PacketSub.PacketList import PacketList
from PacketSub.PcapClass import PcapClass
from PacketSub.Queueue import Queueue
from PacketSub.Fuzzer import Fuzzer
#############################################

class Index:
    def LoadViews(self, Controller):
        self.Controller = Controller
        self.Content = ContentViewClass(self.Controller)
        self.Content.ContentView.addWidget(HookViewClass(self.Controller))
        self.Content.ContentView.addWidget(HookCollectionViewClass(self.Controller))
        self.Content.ContentView.addWidget(LivePacketView(self.Controller))
        self.Content.ContentView.addWidget(PCAPView(self.Controller))

        return self.Content

class EventHandler:
    def __init__(self, Controller):
        super().__init__()
        self.Controller = Controller
        self.Content = Index().LoadViews(self.Controller)
        self.OptionView = OptionViewClass()
        self.OptioButtonHandler()

    def OptioButtonHandler(self):
        self.OptionView.btn.clicked.connect(lambda: self.on_click(0))
        self.OptionView.btn2.clicked.connect(lambda: self.on_click(1))
        self.OptionView.btn3.clicked.connect(lambda: self.on_click(2))
        self.OptionView.btn4.clicked.connect(lambda: self.on_click(3))

    @pyqtSlot()
    def on_click(self, number):
        print('PyQt5 button click')
        # Debbuging purposes
        print(number)
        # Changes the current index of a StackedLayout
        self.Content.ContentView.setCurrentIndex(number)
        print(number)

    def get_Content(self):
        return self.Content
    def get_Option(self):
        return self.OptionView


class OptionViewClass(QFrame):
    def __init__(self):
        super().__init__()

        # Creates a new Vertical BoxLayout
        self.OptionView = QVBoxLayout(self)
        # Creates 4 Button Widget while also setting the label
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        self.btn3 = QPushButton("LivePacket")
        self.btn4 = QPushButton("Pcap")
        self.initUI()

    def initUI(self):
        #Adds 4 button QWidgets to OptionView(BoxLayout)
        self.OptionView.addWidget(self.btn)
        self.OptionView.addWidget(self.btn2)
        self.OptionView.addWidget(self.btn3)
        self.OptionView.addWidget(self.btn4)
        self.setLayout(self.OptionView)

class ContentViewClass(QWidget):
    def __init__(self, Controller):
        #Create a new StackedLayout
        self.ContentView = QStackedLayout()
        super().__init__()
        self.Controller = Controller
        self.setWindowTitle("Content")
        # Awakens and stores location of HookCollectionViewClass
        #self.VHookCollection = HookCollectionViewClass()
        ## Awakens and stores location of PcapViewClass
        #self.VPcap = PCAPView()
        #self.VHook = HookViewClass()
        #self.VPacket = LivePacketView()
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):

        self.setLayout(self.ContentView)


class HookCollectionViewClass(QWidget):
    def __init__(self, Controller):
        super().__init__()
        #Calls function to begging making the view
        self.setStyleSheet('QWidget { font: 20px }')
        self.HookCollectionView = QGridLayout(self)
        self.Controller = Controller
        self.initUI()

    def initUI(self):
        # --------------------------
        self.addHookButton = QPushButton("+Hook Collection")
        self.addHookButton.clicked.connect(self.openCreateHookCol)
        self.editHookButton = QPushButton("Edit")
        self.editHookButton.clicked.connect(self.openEditHookCol)
        self.deleteHookButton = QPushButton("Delete")
        self.deleteHookButton.clicked.connect(self.deleteHookCol)
        self.searchLabel = QLabel("Search")
        self.searchBox = QLineEdit()
        self.searchBox.textChanged.connect(self.searchHookCol)

        self.layout = QGridLayout()
        self.layout.addWidget(self.addHookButton, 1, 0)
        self.layout.addWidget(self.editHookButton, 1, 1)
        self.layout.addWidget(self.deleteHookButton, 1, 2)
        self.layout.setColumnMinimumWidth(4, 100)
        self.layout.addWidget(self.searchLabel, 1, 5)
        self.layout.addWidget(self.searchBox, 1, 6)
        # -------------------------------
        self.HookCollectionPropertiesArea5 = QTreeWidget(self)
        self.HookCollectionPropertiesArea5.setSortingEnabled(True)
        self.HookCollectionPropertiesArea5.setHeaderLabels(["Hook Collection", "No. of Hooks", "Hook Collection status", "Hook Collection Execution Sequence", "Catalog Position"])
        self.HookCollectionPropertiesArea5.hideColumn(4)
        self.HookCollectionPropertiesArea5.setAlternatingRowColors(True)
        self.HookCollectionPropertiesArea5.setFixedWidth(1000)
        # -------------------------------
        self.HookCollectionView.addWidget(self.HookCollectionPropertiesArea5, 1, 0, 1, 1)
        self.HookCollectionView.addLayout(self.layout, 0, 0, 1, 1)
        self.setLayout(self.HookCollectionView)
    
    def updateView(self):
        self.HookCollectionPropertiesArea5.clear()
        index = 0
        for item in self.Controller.hookCollectionCatalog.hookCollectionCatalog:
            item.index = index
            
            HookCollectionPropertiesArea = QTreeWidget(self)
            HookCollectionPropertiesArea.setSelectionMode(QAbstractItemView.NoSelection)
            HookCollectionPropertiesArea.setAlternatingRowColors(True)
            HookCollectionPropertiesArea.setFixedWidth(700)
            labels = ["Hook ", "Description", "Hook status", "Hook Execution Sequence"]
            HookCollectionPropertiesArea.setHeaderLabels(labels)
            
            for hook in item.content:
                hookStatus = "Disabled"
                if hook.status:
                    hookStatus = "Enabled"
                hookChild = QTreeWidgetItem([hook.name, hook.description, hookStatus, str(hook.execNum)])
                HookCollectionPropertiesArea.addTopLevelItem(hookChild)
                
            
            hookStatus = 'Disabled'
            print(item.status)
            if item.status:
                hookStatus = 'Enabled'
            self.dummy = QTreeWidgetItem([item.name, str(len(item.content)), hookStatus, str(item.execNum), str(index)])
            self.HookCollectionPropertiesArea5.addTopLevelItem(self.dummy)
            temp = QTreeWidgetItem()
            self.dummy.addChild(temp)
            self.HookCollectionPropertiesArea5.setItemWidget(temp, 0, HookCollectionPropertiesArea)
            index += 1

    def openCreateHookCol(self):
        hookEditor = HookCol_Overlay(self, self.Controller)
        hookEditor.show()
        
    def openEditHookCol(self):
        if self.HookCollectionPropertiesArea5.selectedItems():
            editing = self.HookCollectionPropertiesArea5.selectedItems()
            for item in editing:
                index = int(item.text(4))
                hookEditor = Edit_HookCol_Overlay(self, self.Controller, index)
                hookEditor.show()
        
    def deleteHookCol(self):
        if self.HookCollectionPropertiesArea5.selectedItems():
            deleting = self.HookCollectionPropertiesArea5.selectedItems()
            for item in deleting:
                index = int(item.text(4))
                self.Controller.hookCollectionCatalog.removeHookCollection(self.Controller.hookCollectionCatalog.hookCollectionCatalog[index])
            self.updateView()
        
    def searchHookCol(self, target):
        if target == '':
            self.updateView()
            
        else:
            self.HookCollectionPropertiesArea5.clear()
            searchResults = self.Controller.hookCollectionCatalog.searchCatalog(self.Controller.hookCollectionCatalog.hookCollectionCatalog, target)
            for item in searchResults:
                HookCollectionPropertiesArea = QTreeWidget(self)
                HookCollectionPropertiesArea.setSelectionMode(QAbstractItemView.NoSelection)
                HookCollectionPropertiesArea.setAlternatingRowColors(True)
                HookCollectionPropertiesArea.setFixedWidth(700)
                labels = ["Hook ", "Description", "Hook status", "Hook Execution Sequence"]
                HookCollectionPropertiesArea.setHeaderLabels(labels)
                
                for hook in item.content:
                    hookStatus = "Disabled"
                    if hook.status:
                        hookStatus = "Enabled"
                    hookChild = QTreeWidgetItem([hook.name, hook.description, hookStatus, str(hook.execNum)])
                    HookCollectionPropertiesArea.addTopLevelItem(hookChild)
                    
                
                hookStatus = 'Disabled'
                if item.status:
                    hookStatus = 'Enabled'
                self.dummy = QTreeWidgetItem([item.name, str(len(item.content)), hookStatus, str(item.execNum), str(item.index)])
                self.HookCollectionPropertiesArea5.addTopLevelItem(self.dummy)
                temp = QTreeWidgetItem()
                self.dummy.addChild(temp)
                self.HookCollectionPropertiesArea5.setItemWidget(temp, 0, HookCollectionPropertiesArea)

class HookViewClass(QWidget):
    def __init__(self, Controller):
        super().__init__()        #Calls function to begging making the view
        self.setStyleSheet('QWidget { font: 20px }')
        self.HookView = QGridLayout(self)
        self.Controller = Controller
        self.initUI()

    def initUI(self):
        # --------------------------
        self.addHookButton = QPushButton("+Hook")
        self.addHookButton.clicked.connect(self.openCreateHook)
        self.editHookButton = QPushButton("Edit")
        self.editHookButton.clicked.connect(self.openEditHook)
        self.deleteHookButton = QPushButton("Delete")
        self.deleteHookButton.clicked.connect(self.deleteHook)
        self.searchLabel = QLabel("Search")
        self.searchBox = QLineEdit()
        self.searchBox.textChanged.connect(self.searchHook)

        self.layout = QGridLayout()
        self.layout.addWidget(self.addHookButton, 1, 0)
        self.layout.addWidget(self.editHookButton, 1, 1)
        self.layout.addWidget(self.deleteHookButton, 1, 2)
        self.layout.setColumnMinimumWidth(4, 100)
        self.layout.addWidget(self.searchLabel, 1, 5)
        self.layout.addWidget(self.searchBox, 1, 6)

        # ---------------

        self.HookPropertiesArea5 = QTreeWidget(self)
        self.HookPropertiesArea5.setHeaderLabels(["Hook", 'Description', 'Association to Hook Collection', 'Catalog Position'])
        self.HookPropertiesArea5.hideColumn(3)
        self.HookPropertiesArea5.setAlternatingRowColors(True)
        self.HookPropertiesArea5.setSortingEnabled(True)
        self.HookPropertiesArea5.setFixedWidth(1000)
        self.HookPropertiesArea5.resizeColumnToContents(1)

        self.HookView.addWidget(self.HookPropertiesArea5, 1, 0, 1, 1)
        self.HookView.addLayout(self.layout, 0, 0, 1, 1)


        self.HookPropertiesArea5.adjustSize()
        self.setLayout(self.HookView)

    def openCreateHook(self):
        hookEditor = Hook_Overlay(self, self.Controller)
        hookEditor.show()
        
    def openEditHook(self):
        if self.HookPropertiesArea5.selectedItems():
            editing = self.HookPropertiesArea5.selectedItems()
            for item in editing:
                index = int(item.text(3))
                hookEditor = Edit_Hook_Overlay(self, self.Controller, index)
                hookEditor.show()
        
    def deleteHook(self):
        if self.HookPropertiesArea5.selectedItems():
            deleting = self.HookPropertiesArea5.selectedItems()
            for item in deleting:
                index = int(item.text(3))
                self.Controller.hookCatalog.removeHook(self.Controller.hookCatalog.hookCatalog[index])
            self.updateView()
        
    def searchHook(self, target):
        if target == '':
            self.updateView()
            
        else:
            self.HookPropertiesArea5.clear()
            searchResults = self.Controller.hookCatalog.searchCatalog(self.Controller.hookCatalog.hookCatalog, target)
            for item in searchResults:
                self.dummy = QTreeWidgetItem([item.name, item.description, str(item.association), str(item.index)])
                self.HookPropertiesArea5.addTopLevelItem(self.dummy)
    
    def updateView(self):
        self.HookPropertiesArea5.clear()
        index = 0
        for item in self.Controller.hookCatalog.hookCatalog:
            item.index = index
            self.dummy = QTreeWidgetItem([item.name, item.description, str(item.association), str(index)])
            self.HookPropertiesArea5.addTopLevelItem(self.dummy)
            index += 1
        
class MainViewClass(QFrame):
    def __init__(self, Controller):
        super().__init__()
        #Set the Main window size ::: setGreometry(Location X, Location Y, Size X, Size Y)
        self.setGeometry(300, 100, 1100, 600)
        self.setWindowTitle("Network Traffic Protocol System")
        self.Controller = Controller
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):
        #Start GridLayout
        self.MainView = QGridLayout(self)
        self.LoadViews()
        self.setLayout(self.MainView)

    def LoadViews(self):
        Evnt = EventHandler(self.Controller)
        self.MainView.addWidget(Evnt.get_Option(), 0, 0, 0, 1)
        self.MainView.addWidget(Evnt.Content, 1, 1, 1, 5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ################
    hookCatalog = HookCatalog()
    hookColCatalog = HookCollectionCatalog()
    Queueue = Queueue()
    PcapClass = PcapClass()
    pktList = PacketList(hookColCatalog, PcapClass, Queueue)
    Fuzzer = Fuzzer(pktList)
    ################
    Controller = Controller(pktList, Queueue, PcapClass, Fuzzer, hookCatalog, hookColCatalog)
    ################
    Main = MainViewClass(Controller)
    #Displays the MainView QFrame
    Main.show()
    #app.exec is necessary to keep the window open even after execution
    sys.exit(app.exec_())
