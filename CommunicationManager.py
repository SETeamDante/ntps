

class C_manager:

    def __init__(self, Controller):
        self.Controller = Controller
        self.FieldNames = []
        self.FieldValues = []
        self.Frame = None
        self.Layer = None

    def SetFieldAreaText(self, FieldNames, FieldValues):
        self.FieldNames = FieldNames
        self.FieldValues = FieldValues

    def UpdateFrame(self, Frame):
        self.Frame = Frame

    def UpdateLayerAndFieldArea(self, Layer, PacketsList):
        self.Layer = Layer
        field_Names = []
        field_Values = []
        for i in PacketsList[self.Frame].GetFieldListNamesWnumber(Layer):
            field_Names.append(i)
        for i in PacketsList[self.Frame].GetFieldListValuesWnumber(Layer):
            field_Values.append(i)
        for i in range(len(self.FieldNames)):
            if len(field_Names) <= i :
                self.FieldNames[i].setText("")
                self.FieldValues[i].setText("")
            else:
                self.FieldNames[i].setText(field_Names[i])
                self.FieldValues[i].setText(field_Values[i])





