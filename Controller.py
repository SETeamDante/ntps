from PacketSub.Packet import Packet
from PacketSub.PacketList import PacketList
from PacketSub.PcapClass import PcapClass
from PacketSub.Queueue import Queueue
from PacketSub.Fuzzer import Fuzzer
from HookSub.HookCollectionCatalog import HookCollectionCatalog
from HookSub.HookCatalog import HookCatalog
from HookSub.HookCollection import HookCollection
from HookSub.Hook import Hook

class Controller:

    def __init__(self, pktList, Queueue, PcapSystem, Fuzzer, HookCatalog, HookCollectionCatalog):
        self.pktList = pktList
        self.Queueue = Queueue
        self.PcapSystem = PcapSystem
        self.Fuzzer = Fuzzer
        self.hookCatalog = HookCatalog
        self.hookCollectionCatalog = HookCollectionCatalog
