class HookCollection():

    # Common class for all the hook collections that are going to be in the system
    # Initializing Hook Collection object with the require parameters
    def __init__(self, name, description, status, execNum):
        self.name = name
        self.description = description

        if status is "Enabled":
            self.status = True
        else:
            self.status = False

        self.execNum = execNum

    # This method is to add the Hooks to a specific Hook Collection
    def addHookToCollection(self):
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
