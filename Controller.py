from PacketSub.Packet import Packet
from PacketSub.PacketList import PacketList
from PacketSub.PcapClass import PcapClass
from PacketSub.Queueue import Queueue
from PacketSub.Fuzzer import Fuzzer

class Controller:

    def __init__(self, pktList, Queueue, PcapSystem, Fuzzer):
        self.pktList = pktList
        self.Queueue = Queueue
        self.PcapSystem = PcapSystem
        self.Fuzzer = Fuzzer