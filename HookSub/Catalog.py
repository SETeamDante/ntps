import operator


class Catalog(): # The catalog class is ready for integration

    # This method has been tested
    # Method to sort in ascending or descending order any of the catalogs using "operator"
    def sortCatalog(self, option, list):

        #     sort in ascending order
        if option is "ascending":
            list.sort(key=operator.attrgetter('name'))

        #     sort in descending order
        else:
            list.sort(key=operator.attrgetter('name'), reverse=True)

    # This method has been tested
    # In charge of looking through all the Hooks/Hook Collection and display a match to the search query
    def searchCatalog(self, list, searchVal):
        for i in list:
            if i.name == searchVal:
                i.printHook()
                return

        print("Not found")

    # Debuggging tool
    def printCatalog(self, list, type):
        if type is True:
            for i in list:
                i.printHook()
        else:
            for i in list:
                i.printCollection()