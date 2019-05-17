def hook(pkt):
    if pkt.hasLayer('DNS'):
        pkt.EditField('DNS', 'sport', 44444)
        print(pkt.GetFieldValue('DNS', 'sport'))  # debugging tool

