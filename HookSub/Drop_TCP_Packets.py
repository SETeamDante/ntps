def hook(pkt):

    if pkt.hasLayer('TCP'):
        pkt.pktList.DropPacketByHook(pkt.Frame)
        print("Frame: ", pkt.Frame)
        print("Drop Packet")
        pkt.pktList.UpdateFrames()

