from scapy.all import rdpcap
from scapy.all import hexdump
from scapy.all import raw

class Packet:
    def __init__(self, pkt, Frame, PktList, IsPcap):
        self.Frame = Frame
        self.pkt = pkt
        self.pktList = PktList
        self.layerList = LayerList(self.pkt)
        PktList.appendPacket(self)
        self.IsPcap = IsPcap

    def GetPacket(self):
        return self.pkt

    def GetHexDump(self):
        return hexdump(self.pkt, dump=True)

    def GetBinary(self):
        return raw(self.pkt)

    def AddtoPktList(self, PktList):
        PktList.appendPacket(self)

    def GetLayerListNames(self):
        LayerListName = []
        for i in self.layerList.List:
            LayerListName.append(i.lyr_name)
        return LayerListName

    def GetFieldListNames(self, LayerName):
        FiledListName = []
        for i in self.layerList.getLayer(LayerName).fieldList.List:
            FiledListName.append(i.fld_name)
        return FiledListName

    def GetFieldListNamesWnumber(self, LayerIndex):
        FiledListName = []
        for i in self.layerList.getLayerWnumber(LayerIndex).fieldList.List:
            FiledListName.append(i.fld_name)
        return FiledListName

    def GetFieldListValuesWnumber(self, LayerIndex):
        FiledListValues = []
        for i in self.layerList.getLayerWnumber(LayerIndex).fieldList.List:
            FiledListValues.append(i.val)
        return FiledListValues

    def GetFieldListNamesAndValues(self, LayerName):
        FiledListName = []
        for i in self.layerList.getLayer(LayerName).fieldList.List:
            FiledListName.append(i.fld_name +"= "+ i.val)
        return FiledListName

    def hasLayer(self, LayerName):
        return self.layerList.hasLayer(LayerName)

    def hasField(self, LayerName, FieldName):
        if self.hasLayer(LayerName):
            layer = self.layerList.getLayer(LayerName)
            return layer.fieldList.hasField(FieldName)
        return False

    def GetFieldValue(self, LayerName, FieldName):
        if self.hasField(LayerName, FieldName):
            layer = self.layerList.getLayer(LayerName)
            return layer.fieldList.GetField(FieldName).val

    def EditField(self, LayerName, FieldName, NewVal):
        if self.hasField(LayerName, FieldName):
            exec("self.pkt["+'"'+LayerName+'"'+"]."+FieldName+" = "+ str(NewVal))
            self.RedrawPkt()

    def RedrawPkt(self):
        self.layerList = LayerList(self.pkt)

    def SetFrame(self, newValue):
        self.Frame = newValue

    def GetFrame(self):
        return self.Frame

    def GetIsPcap(self):
        return self.IsPcap

class LayerList():
    def __init__(self, pkt):
        self.pkt = pkt
        self.List = []
        self.List = self.getLayerList()


    def getLayerList(self):
        split_pkt = self.spliting()
        counter = 0

        for i in split_pkt[1:]:

            layer = Layer(i, counter)
            self.List.append(layer)
            counter += 1

        return self.List

    def getLayer(self, layer):
        for i in self.List:
            if i.lyr_name == layer:
                return i

    def getLayerWnumber(self, layerIndex):
        return self.List[layerIndex]

    def hasLayer(self, layer):
        for i in self.List:
            if i.lyr_name == layer:
                return True
        return False

    def spliting(self):
        pkt_strng = self.pkt.show(dump=True)
        pkt_strng = pkt_strng.split("###[")
        return pkt_strng

class Layer():
    def __init__(self, lyr, pos):
        self.lyr = lyr
        self.lyr_name = lyr.split("]###")[0].strip()

        self.pos = pos

        self.fieldList = FieldList(self.lyr)


class FieldList():
    def __init__(self, lyr):
        self.lyr = lyr
        self.List = []
        self.List = self.getFieldList()

    def getFieldList(self):
        split_lyr = self.spliting()
        counter = 0
        for i in split_lyr[1:]:
            if len(i) < 1 or len(i.split("= ")) <= 1 or i.split("= ")[1] == None or i.split("= ")[0] == None:
                continue
            field = Field(i, counter)
            self.List.append(field)
            counter += 1
        return self.List

    def GetField(self, field):
        for i in self.List:
            if i.fld_name == field:
                return i
        return False

    def hasField(self, field):
        for i in self.List:
            if i.fld_name == field:
                return True
        return False

    def spliting(self):
        pkt_lyr = self.lyr.split('\n')
        return pkt_lyr

class Field():
    def __init__(self, fld, pos):
        self.fld = fld
        self.fld_name = fld.split("= ")[0].strip()

        self.pos = pos

        self.val = fld.split("= ")[1]

if __name__ == '__main__':
    test = rdpcap("test.pcap")
