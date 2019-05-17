def hook(pkt):
    if pkt.hasLayer('TCP'):
        pkt.EditField('TCP', 'sport', 55555)

