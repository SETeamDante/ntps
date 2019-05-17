from scapy.all import fuzz
import threading
import copy
import time
from scapy.all import *

class Fuzzer:
    def __init__(self, PktList):
        self.PktList = PktList
        self.fuzzertThreath = None
        self.pkt = None
        self.on = False

    def SelectPkt(self, pkt, Lyr, fld):
        self.fuzzertThreath = threading.Thread(target=self.FuzzPacket, args=(pkt, Lyr,fld))

    def StartFuzzer(self):
        self.on = True
        self.fuzzertThreath.start()

    def FuzzPacket(self, pkt, Lyr, fld):
        while(self.on):
            print("boop")
            FuzzDumy = eval("fuzz("+Lyr+"())")
            val = eval("FuzzDumy["+Lyr+"]."+fld)
            newPkt = copy.copy(pkt)
            newPkt.EditField(Lyr, fld, val)
            print(newPkt.GetFieldListNamesAndValues(Lyr))
            newPkt.AddtoPktList(self.PktList)
            time.sleep(1)

    def StopFuzzer(self):
        self.on = False