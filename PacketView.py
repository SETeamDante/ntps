from PyQt5.QtCore import QEvent, Qt, pyqtSlot
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QStyle, QStyledItemDelegate, QStyleOptionButton,
                             QTabWidget, QTextEdit, QTreeWidget,
                             QTreeWidgetItem, QToolButton, QVBoxLayout, QWidget)
from Overlays.Proxy_Disabled_Overlay import Proxy_Dis_Overlay
from Overlays.Proxy_Enabled_Overlay import Proxy_En_Overlay
from Proxy import iptable
from PacketSub.PcapClass import PcapClass
from CommunicationManager import C_manager

#  TODO Integrate Field Area

#  TODO Integrate Fuzz Area

#  TODO Integrate and fix forward/drop packet

#  TODO Fix Proxy Behavior pre-interception

#  TODO Fix Binary Tab

#  TODO Fix or Remove Filter expression


class Area(QGroupBox):
    def __init__(self, Controller, title=None):
        super().__init__(title)

        self.PacketList = []
        self.Controller = Controller

    def updatePacketList(self, Packet):
        self.PacketList.append(Packet)

class manualPacketManipulation(Area):
    def __init__(self, Controller, c_manager):
        super().__init__('Field Name, Value and Display Format are editable fields')

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.c_manager = c_manager

        self.saveButton = QPushButton('Save Modification')
        self.forwardButton = QPushButton('Forward')
        self.dropButton = QPushButton('Drop')

        layout.addWidget(self.saveButton)
        layout.addWidget(self.forwardButton)
        layout.addWidget(self.dropButton)

        self.saveButton.clicked.connect(self.saveModification)
        self.forwardButton.clicked.connect(self.forwardPacket)
        self.dropButton.clicked.connect(self.dropPacket)

    def saveModification(self):
        print("Saving")
        self.c_manager.UpdatePacket()

    def forwardPacket(self):
        print("Forwarding")
        self.c_manager.FowardPacket()

    def dropPacket(self):
        print("Dropping")
        self.c_manager.DropPacket()


class CaptureFilterArea(Area):
    def __init__(self, Controller, c_manager):
        super().__init__('Capture Filter')

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.filter_text_box = QLineEdit()
        self.filter_text_box.setPlaceholderText('Filter Expression')

        self.applyButton = QPushButton('Apply')
        self.clearButton = QPushButton('Clear')

        layout.addWidget(QLabel('Filter:'))
        layout.addWidget(self.filter_text_box)
        layout.addWidget(self.applyButton)
        layout.addWidget(self.clearButton)

        self.applyButton.clicked.connect(self.applyFilter)
        self.clearButton.clicked.connect(self.clearFilter)

    def applyFilter(self):
        print("Applying")

    def clearFilter(self):
        self.filter_text_box.clear()

class DissectedTabDelegate(QStyledItemDelegate):
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

class PacketArea(Area):
    def __init__(self, Controller, c_manager):
        super().__init__('Packet Area')

        self.hex = None
        self.binary = None

        self.Controller = Controller
        self.Controller.pktList.SetPacketAreaRef(self)
        self.c_manager = c_manager

        layout = QHBoxLayout()
        self.setLayout(layout)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Dissected Tab Formatting TODO: Deserves to be in own class
        self.dissected_tab_tree = self.SetDissectedTab(tab_widget)
        self.dissected_tab_tree.setRootIsDecorated(False)

        # Binary Tab Formatting TODO: Deserves to be in own class
        self.binary_tab_text_box = self.SetBinaryTab(tab_widget)

        # Hex Tab Formatting TODO: Deserves to be in own class
        self.hex_tab_text_box = self.SetHexTab(tab_widget)

        # Set Event handler
        self.dissected_tab_tree.itemClicked.connect\
            (lambda: self.PacketItemClick
                (
                    (self.dissected_tab_tree.indexOfTopLevelItem(self.dissected_tab_tree.currentItem()), False)
                if
                    (self.dissected_tab_tree.indexOfTopLevelItem(self.dissected_tab_tree.currentItem()) != -1)
                else
                    (self.dissected_tab_tree.currentItem().parent().indexOfChild(self.dissected_tab_tree.currentItem()), True)
                )
            )

    def updateList(self):
        parent = QTreeWidgetItem(self.dissected_tab_tree)  # Make a new QTreeWidgetItem

        pkt = self.PacketList[len(self.PacketList) - 1]  # Get Latest Packet
        lyr = pkt.GetLayerListNames()  # Get the layers names from "pkt"
        parent.setText(0, "Frame " + str(pkt.GetFrame()) + ": " + str(lyr))  # Set the text for the parent

        for i in lyr:  # Iterating through the layers and creates children for the parent treeWidgetItem
            child = QTreeWidgetItem(parent)
            child.setText(0, i + " = " + str(pkt.GetFieldListNamesAndValues(i)))
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setCheckState(0, Qt.Unchecked)

    @pyqtSlot()
    def PacketItemClick(self, index):
        # index.removeChild(index)
        # index = None

        if index[1]:  # If is children
            self.UpdateLayer(index[0])
        else:         # If parent
            self.UpdateFrame(index[0])
            for i in range(len(self.PacketList)):  # Collapses all items except the one being used
                if i != index[0]:
                    self.dissected_tab_tree.topLevelItem(i).setExpanded(False)
                else:
                    self.dissected_tab_tree.topLevelItem(i).setExpanded(True)

            self.hex_tab_text_box.setPlainText(self.PacketList[index[0]].GetHexDump())  # Display Hex Values

        # self.binary_tab_text_box.setPlainText(binary)

    def UpdateFrame(self, Frame):
        self.c_manager.UpdateFrame(Frame, self.PacketList[Frame].GetFrame())

    def UpdateLayer(self, Layer):
        self.c_manager.UpdateLayerAndFieldArea(Layer, self.PacketList)

    def UpdateModifiedPacket(self, Frame, Layer):
        pkt = self.PacketList[Frame]  # Get Latest Packet
        lyr = pkt.GetLayerName(Layer)
        child = self.dissected_tab_tree.topLevelItem(Frame).child(Layer)
        child.setText(0, lyr + " = " + str(pkt.GetFieldListNamesAndValuesWnumber(Layer)))

    def DropPacket(self, FrameIndex):
        del self.PacketList[FrameIndex]
        self.dissected_tab_tree.takeTopLevelItem(FrameIndex)


    def SetDissectedTab(self, tab_widget):
        dissected_tab = QWidget()
        tab_widget.addTab(dissected_tab, "Dissected")

        dissected_tab_layout = QHBoxLayout()

        dissected_tab.setLayout(dissected_tab_layout)

        dissected_tab_tree = QTreeWidget()
        dissected_tab_tree.setHeaderLabels([''])
        dissected_tab_tree.setItemDelegate(DissectedTabDelegate())

        dissected_tab_layout.addWidget(dissected_tab_tree)

        return dissected_tab_tree

    def SetBinaryTab(self, tab_widget):
        binary_tab = QWidget()
        tab_widget.addTab(binary_tab, "Binary")

        binary_tab_layout = QHBoxLayout()
        binary_tab_layout.setContentsMargins(5, 5, 5, 5)

        binary_tab.setLayout(binary_tab_layout)

        binary_tab_text_box = QTextEdit()
        binary_tab_text_box.setPlainText(self.hex)
        binary_tab_text_box.setReadOnly(True)

        binary_tab_layout.addWidget(binary_tab_text_box)

        return binary_tab_text_box

    def SetHexTab(self, tab_widget):
        hex_tab = QWidget()
        tab_widget.addTab(hex_tab, "Hex")

        hex_tab_layout = QHBoxLayout()
        hex_tab_layout.setContentsMargins(5, 5, 5, 5)

        hex_tab.setLayout(hex_tab_layout)

        hex_tab_text_box = QTextEdit()
        hex_tab_text_box.setPlainText(self.binary)
        hex_tab_text_box.setReadOnly(True)

        hex_tab_layout.addWidget(hex_tab_text_box)

        return hex_tab_text_box

class FieldArea(Area):
    def __init__(self, Controller, c_manager):
        super().__init__('Field Area')

        layout = QGridLayout()
        self.setLayout(layout)

        self.c_manager = c_manager

        layout.addWidget(QLabel('Field Name'), 0, 0)
        layout.addWidget(QLabel('Value'), 0, 1)

        self.fields = ['', '', '', '', '', '', '', '']

        self.FieldNames = []
        self.FieldValues = []


        for i, text in enumerate(self.fields):
            tmp = QCheckBox(text)
            self.FieldNames.append(tmp)
            layout.addWidget(tmp, i+1, 0)

        for i, text in enumerate(self.fields):
            tmp = QLineEdit(text)
            self.FieldValues.append(tmp)
            layout.addWidget(tmp, i+1, 1)

        c_manager.SetFieldAreaText(self.FieldNames, self.FieldValues)

class FuzzingArea(Area):
    def __init__(self, Controller, c_manager):
        super().__init__('Fuzzing Area')

        layout = QGridLayout()
        self.setLayout(layout)

        self.c_manager = c_manager

        FuzzerValues = []

        layout.addWidget(QLabel('Selected Packet:'), 0, 0)
        layout.addWidget(QLabel('Selected Fields:'), 1, 0)


        self.packet_name_text_box = QLineEdit()
        self.packet_name_text_box.setReadOnly(True)
        self.field_name_text_box = QLineEdit()
        self.field_name_text_box.setReadOnly(True)


        self.packet_name_text_box.setPlaceholderText('')
        self.field_name_text_box.setPlaceholderText('')


        FuzzerValues.append(self.packet_name_text_box)
        FuzzerValues.append(self.field_name_text_box)


        c_manager.SetFuzzerAreaText(FuzzerValues)

        layout.addWidget(self.packet_name_text_box, 0, 1, 1, 2)
        layout.addWidget(self.field_name_text_box, 1, 1, 1, 2)


        self.fuzz_button = QPushButton('Fuzz')
        self.stop_button = QPushButton('Stop')

        layout.addWidget(self.fuzz_button, 5, 1)
        layout.addWidget(self.stop_button, 5, 2)

        self.fuzz_button.clicked.connect(self.fuzzField)
        self.stop_button.clicked.connect(self.stopFuzzing)

    def fuzzField(self):
        print("Fuzzing")
        self.c_manager.StartFuzzing()

    def stopFuzzing(self):
        print("Stopping")
        self.c_manager.StopFuzzing()

class PlusMinusButtons(QGroupBox):
    def __init__(self, c_manager):
        super().__init__('')
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.c_manager = c_manager

        plus_button = QToolButton()
        minus_button = QToolButton()

        plus_button.setArrowType(Qt.RightArrow)
        minus_button.setArrowType(Qt.LeftArrow)

        layout.addWidget(plus_button, 0, Qt.AlignCenter)
        layout.addWidget(minus_button, 0, Qt.AlignCenter)

        plus_button.clicked.connect(self.add)
        minus_button.clicked.connect(self.remove)

    def add(self):
        print("Add")
        self.c_manager.UpdateFuzzerFieldText()

    def remove(self):
        print("Remove")
        self.c_manager.RemoveFuzzerFieldText()

class PCAPFileArea(Area):
    def __init__(self, Controller):
        super().__init__('PCAP File')

        self.Controller = Controller

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.pcap_file_text_box = QLineEdit()
        self.openButton = QPushButton('Open')
        self.cancelButton = QPushButton('Cancel')

        self.pcap_file_text_box.setPlaceholderText('PCAP File Path')

        layout.addWidget(QLabel('PCAP File:'))
        layout.addWidget(self.pcap_file_text_box)
        layout.addWidget(self.openButton)
        layout.addWidget(self.cancelButton)

        self.openButton.clicked.connect(self.openPCAP)
        self.cancelButton.clicked.connect(self.cancelPCAP)

    def openPCAP(self):
        self.pcap = PcapClass()
        self.pcap.LoadPcap(self.pcap_file_text_box.text(), self.Controller.pktList)

    def cancelPCAP(self):
        self.pcap_file_text_box.clear()

class LivePacketBehaviors(QWidget):
    def __init__(self, Controller):
        super().__init__()

        self.Controller = Controller

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.queue_text_box = QLineEdit('100')
        self.proxy_combo_box = QComboBox()
        self.interception_combo_box = QComboBox()

        self.proxy_combo_box.addItems(['Disabled', 'Enabled'])
        self.interception_combo_box.addItems(['Disabled', 'Enabled'])

        self.interception_combo_box.setEnabled(False)

        layout.addWidget(QLabel('Proxy Behavior:'))
        layout.addWidget(self.proxy_combo_box)
        layout.addWidget(QLabel('Interception Behavior:'))
        layout.addWidget(self.interception_combo_box)
        layout.addWidget(QLabel('Queue Size:'))
        layout.addWidget(self.queue_text_box)

        self.queue_text_box.textChanged.connect(self.adjustQueueSize)
        self.proxy_combo_box.currentIndexChanged.connect(self.toggleProxy)
        self.interception_combo_box.currentIndexChanged.connect(self.toggleInterception)

    def toggleProxy(self, i):
        ipt = iptable.IPTable()

        if i == 0:
            if ipt.isProxyOn():
                ipt.toggleProxy(self.Controller.pktList)

            Proxy_Dis_Overlay()
            self.interception_combo_box.setEnabled(False)

        if i == 1:
            if not ipt.isProxyOn():
                ipt.toggleProxy(self.Controller.pktList)

            self.interception_combo_box.setEnabled(True)
            Proxy_En_Overlay()

    def toggleInterception(self, i):
        ipt = iptable.IPTable()

        if i == 0:
            if ipt.isInterceptorOn():
                ipt.toggleInterceptor()

            print("Disabled")
            self.proxy_combo_box.setEnabled(True)

        if i == 1:
            if not ipt.isInterceptorOn():
                ipt.toggleInterceptor()

            print("Enabled")
            self.proxy_combo_box.setEnabled(False)

    def adjustQueueSize(self, size):
        self.Controller.Queueue.ChangeQueueSize(int(size))

class PacketView(QWidget):
    def __init__(self, Controller, top_widget=None):
        super().__init__()

        self.Controller = Controller

        layout = QGridLayout()
        self.setLayout(layout)

        if top_widget:
            layout.addWidget(top_widget, 0, 0, 1, 3)

        self.c_manager = C_manager(self.Controller)

        layout.addWidget(manualPacketManipulation(self.Controller, self.c_manager), 4, 0, 1, 1)
        layout.addWidget(CaptureFilterArea(self.Controller, self.c_manager), 1, 0, 1, 3)
        layout.addWidget(FuzzingArea(self.Controller, self.c_manager), 3, 2, 2, 1)
        layout.addWidget(FieldArea(self.Controller, self.c_manager), 3, 0, 1, 1)
        layout.addWidget(PacketArea(self.Controller, self.c_manager), 2, 0, 1, 3)
        layout.addWidget(PlusMinusButtons(self.c_manager), 3, 1, 2, 1)

class LivePacketView(PacketView):
    def __init__(self, Controller):
        super().__init__(Controller,LivePacketBehaviors(Controller))

class PCAPView(PacketView):
    def __init__(self, Controller):
        super().__init__(Controller,PCAPFileArea(Controller))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    live_packet = LivePacketView()
    live_packet.show()

    pcap = PCAPView()
    pcap.show()

    sys.exit(app.exec_())
