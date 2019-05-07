import HookCollection
import Catalog


class HookCatalog(Catalog):
    hookCollectionCatalog = []

    def addHook(self, name, description, path):
        hookC = HookCollection()  # type: HookCollection
        hookC.name = name
        hookC.description = description
        hookC.path = path
        for i in range():
            self.hookCollectionCatalog.append(hookC)
        pass

    def sortHookCollection(self):
        option = "ascending"
        super().sortCatalog(option, self.hookCollectionCatalog)

    def searchHookCollection(self):
        hookCollectionName = "Dummy Collection"
        super().searchCatalog(self.hookCatalog, hookCollectionName)
