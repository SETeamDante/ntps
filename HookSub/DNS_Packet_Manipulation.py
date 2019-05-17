def hook(pkt):
    if pkt.hasLayer('DNS'):
        pkt.EditField('UDP', 'sport', 44444)
        print(pkt.GetFieldValue('UDP', 'sport'))  # debugging tool

