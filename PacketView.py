from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QStyle, QStyledItemDelegate, QStyleOptionButton,
                             QTabWidget, QTextEdit, QTreeWidget,
                             QTreeWidgetItem, QToolButton, QVBoxLayout, QWidget)


class Area(QGroupBox):
    def __init__(self, title=None):
        super().__init__(title)


class CaptureFilterArea(Area):
    def __init__(self):
        super().__init__('Capture Filter')

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.filter_text_box = QLineEdit()
        self.filter_text_box.setPlaceholderText('Filter Expression')

        layout.addWidget(QLabel('Filter:'))
        layout.addWidget(self.filter_text_box)
        layout.addWidget(QPushButton('Apply'))
        layout.addWidget(QPushButton('Clear'))


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
    def __init__(self):
        super().__init__('Packet Area')

        layout = QHBoxLayout()
        self.setLayout(layout)

        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # Dissected Tab Formatting TODO: Deserves to be in own class
        dissected_tab = QWidget()
        tab_widget.addTab(dissected_tab, "Dissected")

        dissected_tab_layout = QHBoxLayout()
        dissected_tab.setLayout(dissected_tab_layout)

        dissected_tab_tree = QTreeWidget()
        dissected_tab_tree.setHeaderLabels([''])
        dissected_tab_tree.setItemDelegate(DissectedTabDelegate())
        dissected_tab_layout.addWidget(dissected_tab_tree)

        layers = [
            "Frame XXX: 74 bytes on wire (592 bits), 74 bytes captured " +
            "(592 bits) on interface 0",
            "Ethernet II, Src: Elitegro_dd:12:cd (00:19:21:dd:12:cd), Dst: " +
            "Broadcom_de:ad:05 [00:10:18:de:ad:05]",
            "Internet Control Message Protocol",
            "Transmission Control Protocol, Src Port: 55394 (55394), Dst " +
            "Port:80 (80), Seq:0 Len:0"]
        for i in range(4):
            parent = QTreeWidgetItem(dissected_tab_tree)
            parent.setText(0, "Frame 71{}: frame, eth, tcp".format(4 + i))
            for layer in layers:
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, layer)
                child.setCheckState(0, Qt.Unchecked)

        # Binary Tab Formatting TODO: Deserves to be in own class
        binary_tab = QWidget()
        tab_widget.addTab(binary_tab, "Binary")

        binary_tab_layout = QHBoxLayout()
        binary_tab_layout.setContentsMargins(5, 5, 5, 5)
        binary_tab.setLayout(binary_tab_layout)

        binary_tab_text_box = QTextEdit()
        binary_tab_text_box.setPlainText("\\x00\\x02\\x157\\xa2D\\x00\\xae\\xf3R\\xaa\\xd1\\x08\\x00E\\x00\\x00C\\x00\\x01\\x00\\x00@\\x06x<\\xc0\n"
                                         "\\xa8\\x05\\x15B#\\xfa\\x97\\x00\\x14\\00P\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00P\\x02\\x00\n" 
                                         "\\xbb9\\x00\\x00GET /index.html HTTP/1.0 \\n \\n\n")
        binary_tab_text_box.setReadOnly(True)
        binary_tab_layout.addWidget(binary_tab_text_box)

        # Hex Tab Formatting TODO: Deserves to be in own class
        hex_tab = QWidget()
        tab_widget.addTab(hex_tab, "Hex")

        hex_tab_layout = QHBoxLayout()
        hex_tab_layout.setContentsMargins(5, 5, 5, 5)
        hex_tab.setLayout(hex_tab_layout)

        hex_tab_text_box = QTextEdit()
        hex_tab_text_box.setPlainText("00 00 00 00 E0 1E A7 05 6F 00 10 ........\n"
                                      "00 00 08 5A A0 B9 12 08 00 46 00 ........\n"
                                      "00 00 10 03 68 00 00 00 00 0A 2E ........\n"
                                      "00 00 18 EE 33 0F 19 08 7F 0F 19 ........\n"
                                      "00 00 20 03 80 94 04 00 00 10 01 ........\n"
                                      "00 00 28 16 A2 0A 00 03 50 00 0C ........\n"
                                      "00 00 30 01 01 0F 19 03 80 11 01 ........\n")

        hex_tab_text_box.setReadOnly(True)
        hex_tab_layout.addWidget(hex_tab_text_box)


class FieldArea(Area):
    def __init__(self):
        super().__init__('Field Area')

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Field Name'), 0, 0)
        field_names = ['icmp.type', 'icmp.code', 'icmp.checksum',
                       'icmp.ident', 'icmp.seq']
        for i, text in enumerate(field_names):
            layout.addWidget(QCheckBox(text), i+1, 0)

        layout.addWidget(QLabel('Value'), 0, 1)
        field_values = ['08', '00', '6861', '809e', '0f00']
        for i, text in enumerate(field_values):
            layout.addWidget(QLineEdit(text), i+1, 1)

        layout.addWidget(QLabel('Mask'), 0, 2)
        masks = ['0', '0', '1', '0', '2']
        for i, text in enumerate(masks):
            layout.addWidget(QLineEdit(text), i+1, 2)

        layout.addWidget(QLabel("Display Format"), 0, 3)
        display_formats = ['Binary', 'Hex', 'Dissected']
        for i in range(1, len(field_names)+1):
            combo_box = QComboBox()
            combo_box.addItems(display_formats)
            combo_box.setCurrentIndex(1)
            layout.addWidget(combo_box, i, 3)


class FuzzingArea(Area):
    def __init__(self):
        super().__init__('Fuzzing Area')

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel('Selected Packet Name:'), 0, 0)
        self.packet_name_text_box = QLineEdit()
        self.packet_name_text_box.setPlaceholderText('Selected Packet Name')
        layout.addWidget(self.packet_name_text_box, 0, 1, 1, 2)

        layout.addWidget(QLabel('Selected Field Name:'), 1, 0)
        self.field_name_text_box = QLineEdit()
        self.field_name_text_box.setPlaceholderText('Selected Field Name')
        layout.addWidget(self.field_name_text_box, 1, 1, 1, 2)

        layout.addWidget(QLabel('Expected Return Type:'), 2, 0)
        self.return_type_text_box = QLineEdit()
        self.return_type_text_box.setPlaceholderText('Expected Return Type')
        layout.addWidget(self.return_type_text_box, 2, 1, 1, 2)

        layout.addWidget(QLabel('Minimum:'), 3, 0)
        self.minimum_text_box = QLineEdit()
        self.minimum_text_box.setPlaceholderText('Minimum')
        layout.addWidget(self.minimum_text_box, 3, 1, 1, 2)

        self.maximum_text_box = QLineEdit()
        self.maximum_text_box.setPlaceholderText('Maximum')
        layout.addWidget(QLabel('Maximum:'), 4, 0)
        layout.addWidget(self.maximum_text_box, 4, 1, 1, 2)

        self.fuzz_button = QPushButton('Fuzz')
        layout.addWidget(self.fuzz_button, 5, 1)

        self.stop_button = QPushButton('Stop')
        layout.addWidget(self.stop_button, 5, 2)


class PlusMinusButtons(QGroupBox):
    def __init__(self):
        super().__init__('')

        layout = QVBoxLayout()
        self.setLayout(layout)

        plus_button = QToolButton()
        plus_button.setArrowType(Qt.RightArrow)
        layout.addWidget(plus_button, 0, Qt.AlignCenter)

        minus_button = QToolButton()
        minus_button.setArrowType(Qt.LeftArrow)
        layout.addWidget(minus_button, 0, Qt.AlignCenter)

class PCAPFileArea(Area):
    def __init__(self):
        super().__init__('PCAP File')

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.pcap_file_text_box = QLineEdit()
        self.pcap_file_text_box.setPlaceholderText('PCAP File Path')

        layout.addWidget(QLabel('PCAP File:'))
        layout.addWidget(self.pcap_file_text_box)
        layout.addWidget(QPushButton('Open'))
        layout.addWidget(QPushButton('Cancel'))


class LivePacketBehaviors(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.proxy_combo_box = QComboBox()
        self.proxy_combo_box.addItems(['Disabled', 'Enabled'])

        self.interception_combo_box = QComboBox()
        self.interception_combo_box.addItems(['Disabled', 'Enabled'])

        self.queue_text_box = QLineEdit('100')

        layout.addWidget(QLabel('Proxy Behavior:'))
        layout.addWidget(self.proxy_combo_box)
        layout.addWidget(QLabel('Interception Behavior:'))
        layout.addWidget(self.interception_combo_box)
        layout.addWidget(QLabel('Queue Size:'))
        layout.addWidget(self.queue_text_box)


class PacketView(QWidget):
    def __init__(self, top_widget=None):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        if top_widget:
            layout.addWidget(top_widget, 0, 0, 1, 3)

        layout.addWidget(CaptureFilterArea(), 1, 0, 1, 3)
        layout.addWidget(PacketArea(), 2, 0, 1, 3)
        layout.addWidget(FieldArea(), 3, 0, 1, 1)
        layout.addWidget(PlusMinusButtons(), 3, 1, 1, 1)
        layout.addWidget(FuzzingArea(), 3, 2, 1, 1)

class LivePacketView(PacketView):
    def __init__(self):
        super().__init__(LivePacketBehaviors())

class PCAPView(PacketView):
    def __init__(self):
        super().__init__(PCAPFileArea())

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    live_packet = LivePacketView()
    live_packet.show()

    pcap = PCAPView()
    pcap.show()

    sys.exit(app.exec_())
