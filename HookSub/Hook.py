from importlib.machinery import SourceFileLoader
from inspect import signature, isfunction


class Hook:

    # Common class for all the hooks that are going to be in the system
    # Initializing Hook object with the require parameters
    def __init__(self, name, description, path):
        self.name = name
        self.description = description
        self.path = path
        self.status = False
        self.loader = SourceFileLoader("ntps_hooks_(%s)" % name, path)
        self.module = self.loader.load_module()
        self.inCollection = False
        self.execNum = 0
        self.validHook = False

    # This method has been tested
    # This method is in charge of deleting the Hook object from the system
    def removeHook(self):
        print("%s deleted from system" % self.name)
        del self

    # This method would enabled the hook to be executed
    # Possible solution running hooks on their own threads
    # Need to fix
    def activateHook(self):
        if self.validHook is True and self.inCollection is True:
            print("Hook %s is enabled" % self.name)
            self.status = True
            tryHook = self.module.hook
            self.runHook(tryHook)
        elif self.inCollection is True and self.validHook is False:
            print("Hook %s is not a valid Hook" % self.name)
        else:
            print("Hook %s does not belong to a collection and can't be enabled!" % self.name)

    def disableHook(self):
        print("%s is disabled" % self.name)
        self.status = False

    def runHook(self, hookMethod):
        print("%s is running" % self.name)
        if self.status is True:
            print(hookMethod(5, 5))

    def checkHookProtocol(self):
        try:
            if isfunction(self.module.hook):
                sign = signature(self.module.hook)
                print(sign.parameters)  # Debugging tool
                self.validHook = True
                return True

        except Exception:
            print("Error!")  # Hook Error Overlay here
            print("This hook does not follow protocol\n")

        self.removeHook()
        return False

    # This method has been tested
    # This method is a debugger tool to print the Hooks
    def printHook(self):
        print("The hook name is: ", self.name)
        print("Hook Description is: ", self.description)
        print("Hook Path: ", self.path)
        print("Status: ", self.status)
        print("In collection: ", self.inCollection)
        print("Execution Number: ", self.execNum)