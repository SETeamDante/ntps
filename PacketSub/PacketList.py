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
        if self.Queue.OverFlow():
            self.Frame += 1
            self.Queue.add()
            self.list.append(Packet)
            self.HookCollection.RunFunctionalHooks(Packet)
            if self.Ignore == False:
                for j in self.PacketArea:
                    j.updatePacketList(Packet)
                    j.updateList()
            else:
                self.Ignore = False

    def SetPacketAreaRef(self, Area):
        self.PacketArea.append(Area)

    def FowardPacket(self, Frame):
        for i in self.list:
            if i.GetFrame() == Frame:
                if not i.GetIsPcap():
                    self.PcapSystem.AppendPacket(i)
                # send(i)
                self.list.remove(i)
                self.Queue.RemoveQueue()

    def DropPacket(self, Frame):
        self.Ignore = True
        for i in self.list:
            if i.GetFrame() == Frame:
                print("Packet Drop")
                self.list.remove(i)
                self.Queue.RemoveQueue()

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






