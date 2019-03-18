from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget)
import sys


# Helper class to make tree elements radio buttons
class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not index.parent().isValid():
            QStyledItemDelegate.paint(self, painter, option, index)
        else:
            widget = option.widget
            style = widget.style() if widget else QApplication.style()
            opt = QStyleOptionButton()
            opt.rect = option.rect
            opt.text = index.data()
            opt.state |= QStyle.State_On if index.data(Qt.CheckStateRole) else QStyle.State_Off
            style.drawControl(QStyle.CE_RadioButton, opt, painter, widget)

    def editorEvent(self, event, model, option, index):
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if value:
            if event.type() == QEvent.MouseButtonRelease:
                if index.data(Qt.CheckStateRole) == Qt.Checked:
                    parent = index.parent()
                    for i in range(model.rowCount(parent)):
                        if i != index.row():
                            ix = parent.child(i, 0)
                            model.setData(ix, Qt.Unchecked, Qt.CheckStateRole)
        return value


# PCAP View is set with this class
class PcapViewClass(QFrame):
    def __init__(self, parent=None):
        super(PcapViewClass, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.createPCAPFileArea()
        self.createCaptureFilterArea()
        self.createFieldArea()
        self.createPacketArea()
        self.createPlusMinusButtons()
        self.createFuzzingArea()

        # Placeholder to keep the size of the Packet Area
        self.test = QGroupBox()
        testButton1 = QPushButton("")
        testButton1.setFlat(True)
        testButton2 = QPushButton("")
        testButton2.setFlat(True)
        testButton3 = QPushButton("")
        testButton3.setFlat(True)
        testButton4 = QPushButton("")
        testButton4.setFlat(True)
        testButton5 = QPushButton("")
        testButton5.setFlat(True)
        testButton6 = QPushButton("")
        testButton6.setFlat(True)
        testlayout = QVBoxLayout()
        testlayout.addWidget(testButton1)
        testlayout.addWidget(testButton2)
        testlayout.addWidget(testButton3)
        testlayout.addWidget(testButton4)
        testlayout.addWidget(testButton5)
        testlayout.addWidget(testButton6)
        self.test.setLayout(testlayout)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.PCAPFileArea, 0, 0, 1, 11)
        mainLayout.addWidget(self.captureFilterArea, 1, 0, 1, 11)
        mainLayout.addWidget(self.test, 2, 0, 1, 11)
        mainLayout.addWidget(self.packetArea, 2, 0, 1, 11)

        mainLayout.addWidget(self.fieldArea, 3, 0, 1, 6)
        mainLayout.addWidget(self.PlusMinus, 3, 6, 1, 1)
        mainLayout.addWidget(self.fuzzingArea, 3, 7, 1, 4)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setRowStretch(3, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("Packet from PCAP View")

    # PCAP File Area defined here
    def createPCAPFileArea(self):
        self.PCAPFileArea = QGroupBox("PCAP File")

        PCAPFileLabel = QLabel("PCAP File:")
        PCAPFileEdit = QLineEdit()
        PCAPFileEdit.setPlaceholderText('PCAP File Path')
        PCAPFileLabel.setBuddy(PCAPFileEdit)

        # Open and Cancel buttons are set here
        PCAPFileOpenButton = QPushButton("Open")
        PCAPFileOpenButton.setDefault(False)
        PCAPFileCancelButton = QPushButton("Cancel")
        PCAPFileCancelButton.setDefault(False)

        layout = QHBoxLayout()
        layout.addWidget(PCAPFileLabel)
        layout.addWidget(PCAPFileEdit)
        layout.addWidget(PCAPFileOpenButton)
        layout.addWidget(PCAPFileCancelButton)
        self.PCAPFileArea.setLayout(layout)

    # Capture Filter Area defined here
    def createCaptureFilterArea(self):
        self.captureFilterArea = QGroupBox("Capture Filter")

        CaptureFilterLabel = QLabel("Filter:")
        CaptureFilterEdit = QLineEdit()
        CaptureFilterEdit.setPlaceholderText('Filter Expression')
        CaptureFilterLabel.setBuddy(CaptureFilterEdit)

        # Apply and Clear buttons are set here
        CaptureFilterApplyButton = QPushButton("Apply")
        CaptureFilterApplyButton.setDefault(False)
        CaptureFilterClearButton = QPushButton("Clear")
        CaptureFilterClearButton.setDefault(False)

        layout = QHBoxLayout()
        layout.addWidget(CaptureFilterLabel)
        layout.addWidget(CaptureFilterEdit)
        layout.addWidget(CaptureFilterApplyButton)
        layout.addWidget(CaptureFilterClearButton)
        self.captureFilterArea.setLayout(layout)

    # Plus Minus Buttons defined here
    def createPlusMinusButtons(self):
        self.PlusMinus = QGroupBox("")

        # Buttons are set here
        plusButton = QToolButton()
        plusButton.setArrowType(Qt.RightArrow)
        minusButton = QToolButton()
        minusButton.setArrowType(Qt.LeftArrow)

        layout = QVBoxLayout()
        layout.addWidget(plusButton, 0, Qt.AlignCenter)
        layout.addWidget(minusButton, 0, Qt.AlignCenter)
        self.PlusMinus.setLayout(layout)

    # Field Area defined here
    def createFieldArea(self):
        self.fieldArea = QGroupBox("Field Area")

        fieldNameLabel = QLabel("Field Name")
        fieldNameCheckBox1 = QCheckBox("icmp.type")
        fieldNameCheckBox2 = QCheckBox("icmp.code")
        fieldNameCheckBox3 = QCheckBox("icmp.checksum")
        fieldNameCheckBox4 = QCheckBox("icmp.ident")
        fieldNameCheckBox5 = QCheckBox("icmp.seq")

        valueLabel = QLabel("Value")
        valueText1 = QTextEdit()
        valueText1.setPlainText("08")
        valueText2 = QTextEdit()
        valueText2.setPlainText("00")
        valueText3 = QTextEdit()
        valueText3.setPlainText("6861")
        valueText4 = QTextEdit()
        valueText4.setPlainText("809e")
        valueText5 = QTextEdit()
        valueText5.setPlainText("0f00")

        maskLabel = QLabel("Mask")
        maskText1 = QTextEdit()
        maskText1.setPlainText("0")
        maskText2 = QTextEdit()
        maskText2.setPlainText("0")
        maskText3 = QTextEdit()
        maskText3.setPlainText("1")
        maskText4 = QTextEdit()
        maskText4.setPlainText("0")
        maskText5 = QTextEdit()
        maskText5.setPlainText("2")

        displayFormatLabel = QLabel("Display Format")
        displayFormats = ["Binary", "Hex", "Dissected"]
        displayFormatCBox1 = QComboBox()
        displayFormatCBox1.addItems(displayFormats)
        displayFormatCBox2 = QComboBox()
        displayFormatCBox2.addItems(displayFormats)
        displayFormatCBox3 = QComboBox()
        displayFormatCBox3.addItems(displayFormats)
        displayFormatCBox4 = QComboBox()
        displayFormatCBox4.addItems(displayFormats)
        displayFormatCBox5 = QComboBox()
        displayFormatCBox5.addItems(displayFormats)

        layout = QGridLayout()
        layout.addWidget(fieldNameLabel, 0, 0)
        layout.addWidget(fieldNameCheckBox1, 1, 0)
        layout.addWidget(fieldNameCheckBox2, 2, 0)
        layout.addWidget(fieldNameCheckBox3, 3, 0)
        layout.addWidget(fieldNameCheckBox4, 4, 0)
        layout.addWidget(fieldNameCheckBox5, 5, 0)
        layout.addWidget(valueLabel, 0, 1)
        layout.addWidget(valueText1, 1, 1)
        layout.addWidget(valueText2, 2, 1)
        layout.addWidget(valueText3, 3, 1)
        layout.addWidget(valueText4, 4, 1)
        layout.addWidget(valueText5, 5, 1)
        layout.addWidget(maskLabel, 0, 2)
        layout.addWidget(maskText1, 1, 2)
        layout.addWidget(maskText2, 2, 2)
        layout.addWidget(maskText3, 3, 2)
        layout.addWidget(maskText4, 4, 2)
        layout.addWidget(maskText5, 5, 2)
        layout.addWidget(displayFormatLabel, 0, 3)
        layout.addWidget(displayFormatCBox1, 1, 3)
        layout.addWidget(displayFormatCBox2, 2, 3)
        layout.addWidget(displayFormatCBox3, 3, 3)
        layout.addWidget(displayFormatCBox4, 4, 3)
        layout.addWidget(displayFormatCBox5, 5, 3)
        self.fieldArea.setLayout(layout)

    # Packet Area defined here
    def createPacketArea(self):
        self.packetArea = QGroupBox("Packet Area")
        PacketAreaTabWidget = QTabWidget()
        PacketAreaTabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        # Dissected Tab Formatting
        PacketAreaDissectedTab = QWidget()
        DissectedTabHBox = QHBoxLayout()
        DissectedTabTree = QTreeWidget()
        DissectedTabTree.setHeaderLabels([''])
        DissectedTabTree.setItemDelegate(Delegate())

        children = ["Frame XXX: 74 bytes on wire (592 bits), 74 bytes captured (592 bits) on interface 0",
                    "Ethernet II, Src: Elitegro_dd:12:cd (00:19:21:dd:12:cd), Dst: Broadcom_de:ad:05 [00:10:18:de:ad:05]",
                    "Internet Control Message Protocol",
                    "Tramission Control Protocol, Src Port: 55394 (55394), Dst Port:80 (80), Seq:0 Len:0"]
        for i in range(4):
            parent = QTreeWidgetItem(DissectedTabTree)
            parent.setText(0, "Frame 71{}: frame, eth, tcp".format(4 + i))
            for x in range(len(children)):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, children[x])
                child.setCheckState(0, Qt.Unchecked)
        DissectedTabHBox.addWidget(DissectedTabTree)
        PacketAreaDissectedTab.setLayout(DissectedTabHBox)

        # Binary Tab Formatting
        PacketAreaBinaryTab = QWidget()
        BinaryTextEdit = QTextEdit()
        BinaryTextEdit.setPlainText(
            "\\x00\\x02\\x157\\xa2D\\x00\\xae\\xf3R\\xaa\\xd1\\x08\\x00E\\x00\\x00C\\x00\\x01\\x00\\x00@\\x06x<\\xc0\n"
            "\\xa8\\x05\\x15B#\\xfa\\x97\\x00\\x14\\00P\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00P\\x02\\x00\n"
            "\\xbb9\\x00\\x00GET /index.html HTTP/1.0 \\n \\n\n")
        BinaryTextEdit.setReadOnly(True)

        BinaryTabHBox = QHBoxLayout()
        BinaryTabHBox.setContentsMargins(5, 5, 5, 5)
        BinaryTabHBox.addWidget(BinaryTextEdit)
        PacketAreaBinaryTab.setLayout(BinaryTabHBox)

        # Hex Tab Formatting
        PacketAreaHexTab = QWidget()
        HexTextEdit = QTextEdit()
        HexTextEdit.setPlainText("00 00 00 00 E0 1E A7 05 6F 00 10 ........\n"
                                 "00 00 08 5A A0 B9 12 08 00 46 00 ........\n"
                                 "00 00 10 03 68 00 00 00 00 0A 2E ........\n"
                                 "00 00 18 EE 33 0F 19 08 7F 0F 19 ........\n"
                                 "00 00 20 03 80 94 04 00 00 10 01 ........\n"
                                 "00 00 28 16 A2 0A 00 03 50 00 0C ........\n"
                                 "00 00 30 01 01 0F 19 03 80 11 01 ........\n")
        HexTextEdit.setReadOnly(True)

        HexTabHBox = QHBoxLayout()
        HexTabHBox.setContentsMargins(5, 5, 5, 5)
        HexTabHBox.addWidget(HexTextEdit)
        PacketAreaHexTab.setLayout(HexTabHBox)

        PacketAreaTabWidget.addTab(PacketAreaDissectedTab, "Dissected")
        PacketAreaTabWidget.addTab(PacketAreaBinaryTab, "Binary")
        PacketAreaTabWidget.addTab(PacketAreaHexTab, "Hex")
        packetAreaLayout = QHBoxLayout()
        packetAreaLayout.addWidget(PacketAreaTabWidget)
        self.packetArea.setLayout(packetAreaLayout)

    # Fuzzing Area defined here
    def createFuzzingArea(self):
        self.fuzzingArea = QGroupBox("Fuzzing Area")

        # Labels and text fields are set here
        packetNameLabel = QLabel("Selected Packet Name:")
        packetNameEdit = QLineEdit()
        packetNameEdit.setPlaceholderText('Selected Packet Name')
        packetNameLabel.setBuddy(packetNameEdit)

        packetFieldLabel = QLabel("Selected Field Name:")
        packetFieldEdit = QLineEdit()
        packetFieldEdit.setPlaceholderText('Selected Field Name')
        packetFieldLabel.setBuddy(packetFieldEdit)

        returnTypeLabel = QLabel("Expected Return Type:")
        returnTypeEdit = QLineEdit()
        returnTypeEdit.setPlaceholderText('Expected Return Type')
        returnTypeLabel.setBuddy(returnTypeEdit)

        minimumLabel = QLabel("Minimum:")
        minimumEdit = QLineEdit()
        minimumEdit.setPlaceholderText('Minimum')
        minimumLabel.setBuddy(minimumEdit)

        maximumLabel = QLabel("Maximum:")
        maximumEdit = QLineEdit()
        maximumEdit.setPlaceholderText('Maximum')
        maximumLabel.setBuddy(maximumEdit)

        # Fuzz and Stop buttons are set here
        fuzzButton = QPushButton("Fuzz")
        fuzzButton.setDefault(False)
        stopButton = QPushButton("Stop")
        stopButton.setDefault(False)

        layout = QGridLayout()

        layout.addWidget(packetNameLabel, 0, 0, 1, 2)
        layout.addWidget(packetNameEdit, 0, 1, 1, 2)
        layout.addWidget(packetFieldLabel, 1, 0, 1, 2)
        layout.addWidget(packetFieldEdit, 1, 1, 1, 2)
        layout.addWidget(returnTypeLabel, 2, 0, 1, 2)
        layout.addWidget(returnTypeEdit, 2, 1, 1, 2)
        layout.addWidget(minimumLabel, 3, 0, 1, 2)
        layout.addWidget(minimumEdit, 3, 1, 1, 2)
        layout.addWidget(maximumLabel, 4, 0, 1, 2)
        layout.addWidget(maximumEdit, 4, 1, 1, 2)
        layout.addWidget(fuzzButton, 5, 1)
        layout.addWidget(stopButton, 5, 2)
        layout.setRowStretch(5, 1)
        self.fuzzingArea.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = PcapViewClass()
    # Displays the MainView QFrame
    Main.show()
    # app.exec is necessary to keep the window open even after execution
    sys.exit(app.exec_())