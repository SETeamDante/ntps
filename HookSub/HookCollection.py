class HookCollection:

    # Common class for all the hook collections that are going to be in the system
    # Initializing Hook Collection object with the require parameters
    def __init__(self, name, description, status, execNum):
        self.name = name
        self.description = description
        self.status = status
        self.execNum = execNum
        self.content = []
        self.index = -1

    # This method is to add the Hooks to a specific Hook Collection
    def addHookToCollection(self, hook, executionNumber):
        hook.inCollection = True
        hook.execNum = executionNumber
        hook.association += 1
        self.content.append(hook)
        return

    # This method is to remove Hooks from Hook Collections
    def removeHookFromCollection(self, hook):
        for i in self.content:
            if i.name is hook.name:
                hook.inCollection = False
                print("%s deleted from %s" % (hook.name, self.name))
                self.content.remove(i)
        return

    # This method is in charge of deleting the Hook Collection object from the system
    def removeHookCollection(self):
        print("%s collection deleted from system" % (self.name))
        del self

    # This method has been tested
    # This method is a debugger tool to print the Hook Collection
    def printCollection(self):
        print("The hook Collection name is: ", self.name)
        print("Hook Collection Description is: ", self.description)
        print("Collection status: ", self.status)
        print("Exec Num: ", self.execNum)
        print("Hooks from this collection: \n")
        for i in self.content:
            i.printHook()

    def RunFunctionalHooks(self, pkt):
        if self.status:
            for i in self.content:
                print(i)
                i.RunFunctionalHooks(pkt)
