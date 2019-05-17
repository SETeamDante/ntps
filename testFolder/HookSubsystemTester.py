from Hook import Hook
from HookCollection import HookCollection
from HookCatalog import HookCatalog
from HookCollectionCatalog import HookCollectionCatalog

hookCt = HookCatalog()  # type: HookCatalog

nameC = "Test Collection" # input("Name of hook collection: ")
descriptionC = "Description" # input("description: ")
status = "Disabled" # input("Enabled/Disabled: ")
execNum = 1  # input("Execution #: ")
testCollection = HookCollection(nameC, descriptionC, status, execNum)
hookCCt = HookCollectionCatalog()
hookCCt.addHookCollection(testCollection)

for i in range(0,10):
    # name = input("Name of hook:")
    # description = input("description:")
    # path = input("enter hook path:")
    name = "name"+str(i)
    description = "des"+str(i)
    path = "/Users/Timmy/Desktop/Dummy.py"
    testHook = Hook(name, description, path)  # type: Hook
    if testHook.checkHookProtocol():
        # testCollection.addHookToCollection(testHook, i)
        hookCt.addHook(testHook)

# testHook.checkHookProtocol()
# testHook.activateHook()
# print("\n")
# testHook.disableHook()
# print("\n")
# hookCt.printHC()
# print("\n")
# hookCt.sortHooks()
# hookCt.removeHook(testHook)
# hookCt.searchHook()
# testCollection.removeHookFromCollection(testHook)
# testCollection.printCollection()
# print("\n")
# hookCt.printHC()
# print("\n")
# hookCCt.printHCC()


