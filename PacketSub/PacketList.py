from scapy.all import send

class PacketList:
    def __init__(self, HookCollection, PcapSystem, Queue):
        self.list = []
        self.HookCollection = HookCollection
        self.PcapSystem = PcapSystem
        self.Queue = Queue
        self.Frame = 0
        self.PacketArea = []
        self.Ignore = False

    def appendPacket(self, Packet):
        if not self.Queue.OverFlow():
            self.Frame += 1
            self.Queue.add()
            self.list.append(Packet)
            self.HookCollection.RunFunctionalHooks(Packet)
            if not self.Ignore:  # This is for when a packet is added then hook removes it
                for i in self.PacketArea:
                    i.updatePacketList(Packet)
                    i.updateList()  # Updates the PacketArea item list
            else:
                self.Ignore = False

    def SetPacketAreaRef(self, Area):
        self.PacketArea.append(Area)

    def FowardPacket(self, FrameName):
        for i in self.list:
            if i.GetFrame() == FrameName:
                if not i.GetIsPcap():
                    self.PcapSystem.AppendPacket(i)
                # send(i)
                self.list.remove(i)
                self.Queue.RemoveQueue()

    def FowardPacketWnumber(self, FrameIndex):
        if not self.list[FrameIndex].GetIsPcap():
            self.PcapSystem.AppendPacket(self.list[FrameIndex])
        send(self.list[FrameIndex].GetPacket())
        del self.list[FrameIndex]
        self.Queue.RemoveQueue()

    def DropPacketByHook(self, Frame):
        self.Ignore = True
        for i in self.list:
            if i.GetFrame() == Frame:
                self.list.remove(i)
                self.Queue.RemoveQueue()

    def DropPacket(self, Frame):
        for i in self.list:
            if i.GetFrame() == Frame:
                self.list.remove(i)
                self.Queue.RemoveQueue()

    def DropPacketWnumber(self, FrameIndex):
        del self.list[FrameIndex]
        self.Queue.RemoveQueue()

    def DropDisplayPacket(self, FrameIndex):
        for i in self.PacketArea:
            i.DropPacket(FrameIndex)

    def GetPacket(self, Frame):
        for i in self.list:
            if i.GetFrame() == Frame:
                return i

    def UpdateFrames(self):
        update = []
        value = 1
        for i in self.list:
            if i is not None:
                i.SetFrame(value)
                update.append(i)
                value += 1

        self.list = update

    def UpdatePacketValue(self, PacketIndex, LayerIndex, FieldName, NewVal):
        self.list[PacketIndex].EditFieldWnumber(LayerIndex, FieldName, NewVal)

    def UpdateLayerListDisplay(self, Frame, Layer):
        for i in self.PacketArea:
            i.UpdateModifiedPacket(Frame, Layer)







