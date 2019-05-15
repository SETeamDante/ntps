from HookSub.Catalog import Catalog


class HookCatalog(Catalog):

    def __init__(self):
        self.hookCatalog = []

    # This method is to add hooks to the system
    def addHook(self, hook):
        self.hookCatalog.append(hook)

    # This method is to delete hooks from the system
    def removeHook(self, hook):
        for i in self.hookCatalog:
            if i.name is hook.name:
                print("%s deleted from list" % (hook.name))
                hook.removeHook()
                self.hookCatalog.remove(i)

    # Method tested
    # Using sorting function from Catalog super class
    def sortHooks(self):
        option = input("Sort (ascending/descending): ")
        super().sortCatalog(option, self.hookCatalog)

    # Method tested
    # Using search function from Catalog super class
    def searchHook(self):
        hookName = input("Hook name you want to search: ")
        super().searchCatalog(self.hookCatalog, hookName)

    # Method tested (Debugging tool)
    def printHC(self):
        super().printCatalog(self.hookCatalog, True)