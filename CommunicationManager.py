

class C_manager:

    def __init__(self, Controller):
        self.Controller = Controller
        self.FieldNames = []
        self.FieldValues = []
        self.ViewFrame = None
        self.LayerNumber = None

    def SetFieldAreaText(self, FieldNames, FieldValues):
        self.FieldNames = FieldNames
        self.FieldValues = FieldValues

    def UpdateFieldValues(self, FieldValues):
        self.FieldValues = FieldValues

    def UpdateFrame(self, ViewFrame):
        self.ViewFrame = ViewFrame
        for i in range(len(self.FieldNames)):
            self.FieldNames[i].setText('')
            self.FieldValues[i].setText('')

    def UpdatePacket(self):
        for i in range(len(self.FieldNames)):
            if self.FieldNames[i] != '':
                self.Controller.pktList.UpdatePacketValue(self.ViewFrame, self.LayerNumber, self.FieldNames[i].text(), self.FieldValues[i].text())
        self.Controller.pktList.UpdateLayerListDisplay(self.ViewFrame, self.LayerNumber)

    def UpdateLayerAndFieldArea(self, LayerNumber, PacketsList):
        self.LayerNumber = LayerNumber
        field_Names = []
        field_Values = []
        for i in PacketsList[self.ViewFrame].GetFieldListNamesWnumber(LayerNumber):
            field_Names.append(i)
        for i in PacketsList[self.ViewFrame].GetFieldListValuesWnumber(LayerNumber):
            field_Values.append(i)
        for i in range(len(self.FieldNames)):
            if len(field_Names) <= i:
                self.FieldNames[i].setText("")
                self.FieldValues[i].setText("")
            else:
                self.FieldNames[i].setText(field_Names[i])
                self.FieldValues[i].setText(field_Values[i])
