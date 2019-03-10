from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys


class OptionViewClass(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("margin:5px; border:1px solid rgb(0, 10, 10); ")
        self.initUI()
        # ContentView  = ContentViewClass()

    def initUI(self):
        self.OptionView = QVBoxLayout(self)
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        self.btn3 = QPushButton("LivePacket")
        self.btn4 = QPushButton("Pcap")
        self.OptionView.addWidget(self.btn)
        self.OptionView.addWidget(self.btn2)
        self.OptionView.addWidget(self.btn3)
        self.OptionView.addWidget(self.btn4)
        self.Combo = QButtonGroup()
        self.Combo.addButton(self.btn)
        self.Combo.addButton(self.btn2)
        self.Combo.addButton(self.btn3)
        self.Combo.addButton(self.btn4)
        self.btn.clicked.connect(self.on_click)
        self.btn2.clicked.connect(self.on_click2)
        self.setLayout(self.OptionView)


    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        # self.ContentView.setCurrentIndex(1)

    @pyqtSlot()
    def on_click2(self):
        print('PyQt5 button click')
        # self.ContentView.setCurrentIndex(0)


class ContentViewClass(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("margin:5px; border:1px solid rgb(0, 0, 255); ")
        self.initUI()

    def initUI(self):
        self.ContentView = QStackedLayout()
        self.VHook = HookViewClass()
        self.VPcap = PcapViewClass()
        self.ContentView.addWidget(self.VHook)
        self.ContentView.addWidget(self.VPcap)
        self.setLayout(self.ContentView)


class HookViewClass(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.HookView = QVBoxLayout(self)
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        self.HookView.addWidget(self.btn)
        self.HookView.addWidget(self.btn2)
        self.setLayout(self.HookView)

class PcapViewClass(QFrame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.PcapView = QVBoxLayout()
        self.btn = QPushButton("Hook")
        self.btn2 = QPushButton("Hook Collection")
        self.btn3 = QPushButton("Pcap")
        self.PcapView.addWidget(self.btn)
        self.PcapView.addWidget(self.btn2)
        self.PcapView.addWidget(self.btn3)
        self.setLayout(self.PcapView)

class MainViewClass(QFrame):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 100, 1100, 600)
        self.setStyleSheet("margin:5px; border:5px solid rgb(255, 0, 0); ")
        self.initUI()

    def initUI(self):
        self.MainView = QGridLayout(self)
        self.VOption = OptionViewClass()
        self.VContent = ContentViewClass()
        self.MainView.addWidget(self.VOption,0,0,0,1 )
        self.MainView.addWidget(self.VContent, 1,1,1,5)
        self.setLayout(self.MainView)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainViewClass()

    Main.show()

    sys.exit(app.exec_())


# #Here we begin
# app = QApplication([])
# window = QWidget()
# window.setGeometry(300,100,1100,600)
# # window.resize(100,100)
# # window.showFullScreen()
#
#
#
# # window3 = QWidget()
# # OptionView3 = QVBoxLayout()
# # btn = QPushButton("Hook")
# # OptionView3.addWidget(btn)
# # btn2 = QPushButton("Hook Collection")
# # OptionView3.addWidget(btn2)
# # btn3 = QPushButton("LivePacket")
# # OptionView3.addWidget(btn3)
# # btn4 = QPushButton("Pcap")
# # OptionView3.addWidget(btn4)
# # Combo = QButtonGroup()
# # Combo.addButton(btn)
# # Combo.addButton(btn2)
# # Combo.addButton(btn3)
# # Combo.addButton(btn4)
#
# # btn.clicked.connect(on_click)
# # btn2.clicked.connect(on_click2)
#
# # window3.setStyleSheet("border:3px solid rgb(255, 0, 0); ")
# # window3.setLayout(OptionView3)
#
# # layout = QGridLayout()
# #
# # window2 = QWidget()
# # OptionView2 = QStackedLayout()
#
#
# window4 = QWidget()
# OptionView4 = QVBoxLayout()
# OptionView4.addWidget(QPushButton("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
# OptionView4.addWidget(QPushButton("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa"))
# OptionView4.addWidget(QPushButton("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"))
# window4.setLayout(OptionView4)
#
# window5 = QWidget()
# OptionView5 = QVBoxLayout()
# OptionView5.addWidget(QPushButton("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"))
# OptionView5.addWidget(QPushButton("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"))
# OptionView5.addWidget(QPushButton("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"))
# window5.setLayout(OptionView5)
#
# OptionView2.addWidget(window4)
# OptionView2.addWidget(window5)
#
# window2.setStyleSheet("margin:5px; border:1px solid rgb(0, 10, 10); ")
# window2.setLayout(OptionView2)
#
# layout.addWidget(window2,1,1,1,5)
# layout.addWidget(window3,0,0,0,1)
#
# window.setLayout(layout)
#
# window.show()
# app.exec_()



