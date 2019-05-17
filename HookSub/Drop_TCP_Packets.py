def hook(pktList):

    for i in range(1, pktList.list.__len__()):
        pkt = pktList.GetPacket(i)
        if pkt.hasLayer('TCP'):
            pktList.DropPacket(i)
            print("Frame: ", i)

    pktList.UpdateFrames()

