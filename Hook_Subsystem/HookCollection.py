class HookCollection():

    def __init__(self, name, description, status, execNum):
        self.name = name
        self.description = description
        self.status = status
        self.execNum = execNum

    def addHookCollection(name, description, status, execNum):
        hookCollection = HookCollection()
        hookCollection.name = name
        hookCollection.description = description
        hookCollection.status = status
        hookCollection.execNum = execNum

    def removeHookCollection(self):
        print("%s collection deleted" % (self.name))
        object.__del__(self)
