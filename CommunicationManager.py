

class C_manager:

    def __init__(self, Controller):
        self.Controller = Controller
        self.FieldNames = []
        self.FieldValues = []
        self.FuzzerValues = []
        self.ViewFrame = None
        self.LayerNumber = None
        self.PacketFrame = None
        self.LayerToFuzz = None

    def SetFieldAreaText(self, FieldNames, FieldValues):
        self.FieldNames = FieldNames
        self.FieldValues = FieldValues

    def SetFuzzerAreaText(self, FuzzerValues):
        self.FuzzerValues = FuzzerValues

    def UpdateFieldValues(self, FieldValues):
        self.FieldValues = FieldValues

    def UpdateFrame(self, ViewFrame, PacketFrame):
        self.ViewFrame = ViewFrame
        self.PacketFrame = PacketFrame
        for i in range(len(self.FieldNames)):
            self.FieldNames[i].setText('')
            self.FieldValues[i].setText('')

    def UpdatePacket(self):
        for i in range(len(self.FieldNames)):
            if self.FieldNames[i].text() != '':
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

    def DropPacket(self):
        self.Controller.pktList.DropPacketWnumber(self.ViewFrame)
        self.Controller.pktList.DropDisplayPacket(self.ViewFrame)

    def FowardPacket(self):
        self.Controller.pktList.FowardPacketWnumber(self.ViewFrame)
        self.Controller.pktList.DropDisplayPacket(self.ViewFrame)

    def UpdateFuzzerFieldText(self):
        self.LayerToFuzz = self.LayerNumber
        SelectedFields = ""
        for i in range(len(self.FieldNames)):
            if self.FieldNames[i].isChecked():
                if SelectedFields == "":
                    SelectedFields = self.FieldNames[i].text()
                else:
                    SelectedFields = SelectedFields + ", " + self.FieldNames[i].text()
        self.FuzzerValues[1].setText(SelectedFields)
        self.FuzzerValues[0].setText("Frame:" + str(self.PacketFrame))

    def RemoveFuzzerFieldText(self):
        self.FuzzerValues[0].setText("")
        self.FuzzerValues[1].setText("")

    def StartFuzzing(self):
        if self.FuzzerValues[0].text() != "":
            Fuzziner_Field = []
            for i in self.FieldNames:
                if i.isChecked():
                    Fuzziner_Field.append(i.text())
            Frame = self.FuzzerValues[0].text().split(":")[1]
            Fuzz_pkt = self.Controller.pktList.GetPacket(int(Frame))
            lyr = Fuzz_pkt.GetLayerName(self.LayerToFuzz)
            self.Controller.Fuzzer.SelectPkt(Fuzz_pkt, lyr, Fuzziner_Field)
            self.Controller.Fuzzer.StartFuzzer()

    def StopFuzzing(self):
        self.Controller.Fuzzer.StopFuzzer()


