from scapy.layers.inet import TCP
from scapy.sendrecv import send


def hook(pkt):
    if pkt.hasLayer('TCP') and pkt.GetFieldValue('TCP', 'flags') == 'S':
        packetSA = IP(dst=pkt.GetFieldValue('IP', 'src'), src=pkt.GetFieldValue('IP', 'dst')) / TCP(
            sport=pkt.GetFieldValue('TCP', 'dport'),
            dport=pkt.GetFieldValue('TCP', 'sport')
            , flags='SA', seq=123456,
            ack=pkt.GetFieldValue('TCP', 'seq')+1)

        send(packetSA)
        print(packetSA.show(True))
