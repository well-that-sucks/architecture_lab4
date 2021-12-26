import pyodbc as db

class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def get_instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `get_instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

@Singleton
class DBConnection(object):

    def __init__(self):
        self.conn = db.connect('Driver={SQL Server};Server=DESKTOP-69AKAQS;Database=AlcoholShop;Trusted_Connection=yes;')

    def __str__(self):
        return self.conn