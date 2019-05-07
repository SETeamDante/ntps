class Hook:

    # Common class for all the hooks that are going to be in the system

    def __init__(self, name, description, path):
        self.name = name
        self.description = description
        self.path = path
        self.status = False

    def removeHook(self):
        print("%s deleted" % (self.name))
        object.__del__(self)

    def activateHook(self):
        self.status = True
        # while self.status is True (maybe)
        exec(self.path)

    def disableHook(self):
        self.status = False
