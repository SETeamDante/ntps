from PacketSub.Queueue import Queueue
from PacketSub.PcapClass import PcapClass
from PacketSub.PacketList import PacketList
from Change_TCPSourcePort import hook

if __name__ == '__main__':
    queue = Queueue()
    pcapT = PcapClass()
    pktList = PacketList(pcapT, queue)
    pcapT.LoadPcap("/Users/Timmy/Desktop/Software 2/Hook_Subsystem/PacketSub/test.pcap", pktList)

    print(pktList.list.__len__())
    for i in range(1, pktList.list.__len__()):
        # print(i)
        # print(pktList.GetPacket(i))
        pkt = pktList.GetPacket(i)
        # hook(pkt)
        print(pkt.GetLayerListNames())

        # print(pktList.DropPacket('TCP'))
        # print(pkt.GetFieldListNamesAndValues())

    # if pkt.hasLayer('TCP'):
    #     # pktList.DropPacket('TCP')
    #     pkt.EditField('TCP', 'sport', 55555)
    #     if pkt.GetFieldValue('TCP', 'flags') == 'S':
    #         print("Kill me please")
    # print(pkt.GetFieldValue('TCP', 'sport'))
    # print(pkt.GetFieldListNamesAndValues('TCP'))
    #
    # for i in range(1, pktList.list.__len__()):
    #     pkt = pktList.GetPacket(i)
    #     if pkt.hasLayer('TCP'):
    #         print(pkt.GetLayerListNames())
