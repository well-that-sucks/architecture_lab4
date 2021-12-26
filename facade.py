from itembuilder import *
from flask_restful import reqparse

class Facade:
    def __init__(self, cache):
        self.items_db = ItemsDB()
        self.cache = cache

    def get(self, obj, info, item_name = None, min_quantity = None, supplier_id = None):
        args = {'item_name': item_name, 'min_quantity': min_quantity, 'supplier_id': supplier_id}
        return {'success': True, 'item': self.cache.get_cache(args)}


    def update(self, obj, info, item_id, item_name, description, quantity, price, supplier_id):
        item = {'item_id': item_id, 'item_name': item_name, 'description': description, 'quantity': quantity, 'price': price, 'supplier_id': supplier_id}
        self.items_db.update(item)
        return {'success': True, 'item': [item]}

    def delete(self, obj, info, item_id):
        self.items_db.delete(item_id)
        return {'success': True}

    def insert(self, obj, info, item_id, item_name, description, quantity, price, supplier_id):
        item = {'item_id': item_id, 'item_name': item_name, 'description': description, 'quantity': quantity, 'price': price, 'supplier_id': supplier_id}
        self.items_db.insert(item)
        return {'success': True, 'item': [item]}