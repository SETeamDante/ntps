from scapy.all import send

class PacketList:
    def __init__(self, HookCollection, PcapSystem, Queue):
        self.list = []
        self.HookCollection = HookCollection
        self.PcapSystem = PcapSystem
        self.Queue = Queue
        self.Frame = 0


    def appendPacket(self, Packet):
        if self.Queue.OverFlow():
            self.Frame += 1
            self.Queue.add()
            self.HookCollection.RunFunctionalHooks(Packet)
            self.list.append(Packet)


    def FowardPacket(self, Frame):
        for i in self.list:
            if i.GetFrame() == Frame:
                if not i.GetIsPcap():
                    self.PcapSystem.AppendPacket(i)
                # send(i)
                self.list.remove(i)
                self.Queue.RemoveQueue()

    def DropPacket(self, Frame):
        for i in self.list:
            if i.GetFrame() == Frame:
                if i.GetIsPcap():
                    pass
                else:
                    print("boo[")
                    self.list.remove(i)
                    self.Queue.RemoveQueue()

    def GetPacket(self, Frame):
        for i in self.list:
            if i.GetFrame() == Frame:
                return i






