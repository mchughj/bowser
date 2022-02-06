
class patents:
    @staticmethod
    def shortName():
        return "patent"

    @staticmethod
    def description():
        return "Patent search"

    @staticmethod
    def bare():
        return "https://patents.justia.com/"

    @staticmethod
    def arged(argList):
        return "https://patents.justia.com/search?q=", argList
