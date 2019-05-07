import Hook
import Catalog


class HookCatalog(Catalog):
    hookCatalog = []

    def addHook(self, name, description, path):
        hook = Hook()  # type: Hook
        hook.name = name
        hook.description = description
        hook.path = path
        for i in range():
            self.hookCatalog.append(hook)
        pass

    def sortHooks(self):
        option = "ascending"
        super().sortCatalog(option, self.hookCatalog)

    def searchHook(self):
        hookName = "Dummy.py"
        super().searchCatalog(self.hookCatalog, hookName)