
class foo:
    @staticmethod
    def shortName():
        return "foo"

    @staticmethod
    def description():
        return "A completely dummy and test service"

    @staticmethod
    def bare():
        return "https://patents.justia.com/"

    @staticmethod
    def arged(argList):
        return "https://patents.justia.com/search?q=", argList
