from scapy.utils import PcapWriter
from scapy.all import rdpcap
from Packet import Packet


class PcapClass:
    def __init__(self):
        self.Filename = "PacketCapture"
        self.LivePcap = None

    def CreateLivePacket(self):
        self.LivePcap = PcapWriter(self.Filename+".pcap", append=True, sync=True)

    def AppendPacket(self, pkt):
        if self.LivePcap is not None:
            self.LivePcap.write(pkt.GetPacket())

    def ChangeName(self, NewName):
        if self.LivePcap is None:
            self.FileName = NewName

    def LoadPcap(self, PcapFileDirectory, PktList):
        if self.LivePcap is None:
            self.LivePcap = rdpcap(PcapFileDirectory)
            frame = 1
            for i in self.LivePcap:
                Packet(i, frame, PktList, True)
                frame += 1






