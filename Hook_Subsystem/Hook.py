# from threading import Thread possible solution to running the hooks


class Hook:

    # Common class for all the hooks that are going to be in the system
    # Initializing Hook object with the require parameters
    def __init__(self, name, description, path):
        self.name = name
        self.description = description
        self.path = path
        self.status = False
        self.code = open(path, 'r+').read()
        self.inCollection = False
        # self.lifetime = None

    # This method has been tested
    # This method is in charge of deleting the Hook object from the system
    def removeHook(self):
        print("%s deleted from system" % self.name)
        del self

    # This method would enabled the hook to be executed
    # Possible solution running hooks on their own threads
    # Need to fix
    def activateHook(self):
        if self.inCollection is True:
            print("Hook %s is enabled" % self.name)
            self.status = True
            # try:
            #     self.lifetime = Thread(target=self.runHook(), args=[]).start()
            #     self.lifetime.join()
            # except:
            #     pass

            # self.lifetime.start()

            # self.runHook()
        else:
            print("Hook %s does not belong to a collection and can't be enabled!" % self.name)

    def disableHook(self):
        print("%s is disabled" % self.name)
        self.status = False

    def runHook(self):
        print("%s is running" % self.name)
        while True:
            if self.status is True:
                exec(self.code)  # Needs fixing
                # self.status = False
            continue

    # This method has been tested
    # This method is a debugger tool to print the Hooks
    def printHook(self):
        print("The hook name is: ", self.name)
        print("Hook Description is: ", self.description)
        print("Hook Path: ", self.path)
        print("Status: ", self.status)
        print("In collection: ", self.inCollection)
