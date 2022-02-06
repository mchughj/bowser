
class google:
    @staticmethod
    def shortName():
        return "g"

    @staticmethod
    def description():
        return "Standard google search"

    @staticmethod
    def bare():
        return "http://www.google.com"

    @staticmethod
    def arged(argList):
        return "http://www.google.com/search?q=", argList
