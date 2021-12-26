from flask import Flask
from flask_restful import Api
from specification import *
import time

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    @app.route('/search/', methods = ['GET'])
    def proc():
        #time.sleep(20)
        hardcoded_itemset = [{'item_id': 200001, 'item_name': 'Hike', 'description': 'Beer', 'quantity': 200, 'price': 10, 'supplier_id': 2},
                            {'item_id': 200002, 'item_name': 'Jagermeister', 'description': 'Liquor', 'quantity': 15, 'price': 40, 'supplier_id': 3}, 
                            {'item_id': 200003, 'item_name': 'Oakheart', 'description': 'Rome', 'quantity': 10, 'price': 20, 'supplier_id': 1},
                            {'item_id': 200004, 'item_name': 'Jim Beam White', 'description': 'Whiskey', 'quantity': 18, 'price': 25, 'supplier_id': 1},
                            {'item_id': 200005, 'item_name': 'Smirnoff', 'description': 'Vodka', 'quantity': 156, 'price': 35, 'supplier_id': 3}]
        
        #item_filter = CompositeFilter(ProductName(), MinQuantity(), SupplierID())
        #filtered_items = []
        #for item in hardcoded_itemset:
        #    if item_filter.satisfies_filters(item):
        #        filtered_items.append(item)
        
        return {'items': hardcoded_itemset}

    app.run(port = 5001, debug = True)