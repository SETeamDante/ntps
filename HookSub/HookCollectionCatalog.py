from HookSub.Catalog import Catalog


class HookCollectionCatalog(Catalog):

    def __init__(self):
        self.hookCollectionCatalog = []

    # This method is to add hook collections to the system
    def addHookCollection(self, hookCollection):
        self.hookCollectionCatalog.append(hookCollection)

    # This method is to delete hook collections from the system
    def removeHookCollection(self, hookCollection):
        for i in self.hookCollectionCatalog:
            if (i.name is hookCollection.name):
                print("%s deleted from list" % (hookCollection.name))
                hookCollection.removeHookCollection()
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

    def RunFunctionalHooks(self, pkt):
        for i in self.hookCollectionCatalog:
            i.RunFunctionalHooks(pkt)
