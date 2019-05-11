from HookCollection import HookCollection
from Catalog import Catalog


class HookCollectionCatalog(Catalog):

    def __init__(self):
        self.hookCollectionCatalog = []

    def addHookCollection(self, name, description, status, execNum):
        hookC = HookCollection(name, description, status, execNum)  # type: HookCollection
        self.hookCollectionCatalog.append(hookC)

    def removeHookCollection(self, hookC):
        for i in self.hookCollectionCatalog:
            if (i.name is hookC.name):
                print("%s deleted from list" % (hookC.name))
                hookC.removeHookCollection()
                self.hookCollectionCatalog.remove(i)

    # Method tested
    # Using sorting function from Catalog super class
    def sortHookCollection(self):
        option = input("Sort (ascending/descending): ")
        super().sortCatalog(option, self.hookCollectionCatalog)

    # Method tested
    # Using search function from Catalog super class
    def searchHookCollection(self):
        hookCollectionName = input("Hook Collection name you want to search: ")
        super().searchCatalog(self.hookCollectionCatalog, hookCollectionName)

    # Method tested (Debugging tool)
    def printHCC(self):
        super().printCatalog(self.hookCollectionCatalog, False)