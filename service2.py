from flask import Flask
from flask_restful import Api
from flask_restful import reqparse
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
        self.conn = db.connect('Driver={SQL Server};Server=DESKTOP-69AKAQS;Database=Service1;Trusted_Connection=yes;')

    def __str__(self):
        return self.conn

if __name__ == '__main__':

    conn = DBConnection.get_instance().conn
    app = Flask(__name__)
    api = Api(app)
    @app.route('/price-list/', methods = ['GET'])
    def proc_pricelist():
        parser = reqparse.RequestParser()
        parser.add_argument('page')
        parsed_args = parser.parse_args()
        items_dict = []
        if parsed_args['page']:
            min_id = (int(parsed_args['page']) - 1) * 5000 + 100001
            max_id = int(parsed_args['page']) * 5000 + 100000
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM Prices WHERE ItemID >= {min_id} AND ItemID <= {max_id}')
                items = cursor.fetchall()
            for item in items:
                items_dict.append({'item_id': item[0], 'item_name': item[1], 'price': item[2]})
        return {'items': items_dict}
    
    @app.route('/details/<int:id>', methods = ['GET'])
    def proc_details(id):
        with conn.cursor() as cursor:
            cursor.execute(f'SELECT * FROM Details WHERE ItemID = {id}')
            items = cursor.fetchall()
        item = 'No such item with this id'
        if len(items) >= 1:
            item = {'item_id': items[0][0], 'description': items[0][1], 'quantity': items[0][2], 'supplier_id': items[0][3]}
        return item

    app.run(port = 5002, debug = True)
    DBConnection.get_instance().conn.close()