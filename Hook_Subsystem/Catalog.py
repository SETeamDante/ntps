class Catalog():

    def sortCatalog(self, option, list):  # To be asked(Diego)

        #     sort in ascending order
        if option is "ascending":
            list.sort()

        #     sort in descending order
        if option is "descending":
            list.sort(reverse=True)

    def searchCatalog(self, list, searchVal):

        for i in list:
            if (i is searchVal):
                return i

        return "Not found"
