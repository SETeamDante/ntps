def hook(pkt):

    if pkt.hasLayer('TCP'):
        pkt.pktList.DropPacket(pkt.Frame)
        print("Frame: ", pkt.Frame)
        print("Drop Packet")
        pkt.pktList.UpdateFrames()

