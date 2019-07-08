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
        self.fuzzertThreath = threading.Thread(target=self.FuzzPacket, args=(pkt, Lyr, fld))

    def StartFuzzer(self):
        self.on = True
        self.fuzzertThreath.start()

    def FuzzPacket(self, pkt, Lyr, fld):
        while(self.on):
            FuzzDumy = eval("fuzz("+Lyr+"())")
            newPkt = copy.copy(pkt)
            if fld:
                for i in fld:
                    val = eval("FuzzDumy[" + Lyr + "]." + i)
                    newPkt.EditField(Lyr, i, val)
                newPkt.Frame = self.PktList.list[len(self.PktList.list)-1].Frame + 1
                newPkt.AddtoPktList(self.PktList)
                time.sleep(1)
            else:
                for i in newPkt.GetFieldListNames(Lyr):
                    val = eval("FuzzDumy[" + Lyr + "]." + i)
                    newPkt.EditField(Lyr, i, val)
                newPkt.Frame = self.PktList.list[len(self.PktList.list)-1].Frame + 1
                newPkt.AddtoPktList(self.PktList)
                time.sleep(1)

    def StopFuzzer(self):
        self.on = False
