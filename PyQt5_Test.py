from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys


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
        self.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 255); ")
        # Awakens and stores location of HookViewClass
        self.VHook = HookViewClass()
        # Awakens and stores location of PcapViewClass
        self.VPcap = PcapViewClass()
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):

        #Add QFrame( Or QWidget) to ContentView(StackLayout) in a Queue form
        self.ContentView.addWidget(self.VHook)
        self.ContentView.addWidget(self.VPcap)
        # Inject ContentView Layout to the QFrame ( or QWidget)
        self.setLayout(self.ContentView)


#TODO
class HookViewClass(QFrame):
    def __init__(self):
        super().__init__()
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):
        #Creates a vertical Box Layout
        self.HookView = QVBoxLayout(self)
        # Creates 2 Button Widget while also setting the label
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        # Adds widgets to PcapView( a vertical Box Layout) in Queue form
        self.HookView.addWidget(self.btn)
        self.HookView.addWidget(self.btn2)
        # Inject PcapView Layout to the QFrame ( or QWidget)
        self.setLayout(self.HookView)

#TODO
class PcapViewClass(QFrame):
    def __init__(self):
        super().__init__()
        #Calls function to begging making the view
        self.initUI()

    def initUI(self):
        #Creates a vertical Box Layout
        self.PcapView = QVBoxLayout()
        #Creates 3 Button Widget while also setting the label
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        self.btn3 = QPushButton("Pcap")
        #Adds widgets to PcapView( a vertical Box Layout) in Queue form
        self.PcapView.addWidget(self.btn)
        self.PcapView.addWidget(self.btn2)
        self.PcapView.addWidget(self.btn3)
        # Inject PcapView Layout to the Qframe ( or QWidget)
        self.setLayout(self.PcapView)

class MainViewClass(QFrame):
    def __init__(self):
        super().__init__()
        #Set the Main window size ::: setGreometry(Location X, Location Y, Size X, Size Y)
        self.setGeometry(300, 100, 1100, 600)
        self.setWindowTitle("Network Traffic Protocol System")
        #Add a style to MainView (TO BE CHANGE)
        #TODO
        self.setStyleSheet("margin:5px; border:5px solid rgb(255, 0, 0); ")
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
    Main = MainViewClass()
    #Displays the MainView QFrame
    Main.show()
    #app.exec is necessary to keep the window open even after execution
    sys.exit(app.exec_())
