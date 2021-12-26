import requests
from specification import *
from flask_restful import reqparse
from itemsdb import ItemsDB
import multiprocessing
from functools import partial
from itertools import repeat
import time

def filter_element(parsed_args, item):
    item_filter = CompositeFilter(ProductName(), MinQuantity(), SupplierID())
    if item_filter.satisfies_filters(item, parsed_args):
        return item
    return None   

class Items:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)
    
    def add_items(self, another_item):
        self.items += another_item.items
        return self

    def remove(self, idx):
        del self.items[idx]
    
    def set(self, new_items):
        self.items = new_items

    def filter(self, parsed_args):
        #item_filter = CompositeFilter(ProductName(), MinQuantity(), SupplierID())
        start_time = time.time()
        with multiprocessing.Pool(4) as pool:
            #new_items = pool.starmap(filter_element, zip(self.items, repeat(parsed_args), repeat(item_filter)))
            new_items = pool.map(partial(filter_element, parsed_args), self.items)  
        new_items = [x for x in new_items if x]
        print(time.time() - start_time)
        return new_items

        #start_time = time.time()
        #filtered_items = []
        #for item in self.items:
        #    if item_filter.satisfies_filters(item, self.parsed_args):
        #        filtered_items.append(item)
        #print(time.time() - start_time)
        #return filtered_items
        

class AbstractItemBuilder:
    def get_from_source(self):
        pass

    def get_items(self):
        pass

    def filter(self):
        pass

class FirstServiceItemBuilder(AbstractItemBuilder):
    def __init__(self):
        self.item = Items()

    def get_items(self):
        t_item = self.item
        self.item = Items()
        return t_item

    def get_from_source(self):
        self.item.set(requests.get('http://127.0.0.1:5001/search/').json()['items'])

    def filter(self):
        self.item.set(self.item.filter())

class SecondServiceItemBuilder(AbstractItemBuilder):
    def __init__(self):
        self.item = Items()

    def get_items(self):
        t_item = self.item
        self.item = Items()
        return t_item

    def get_from_source(self):
        items_partial = []
        for page in range(1, 2):
            items_paged = requests.get(f'http://127.0.0.1:5002/price-list?page={page}').json()['items']
            items_partial = items_partial + items_paged
        items_full = []
        for item in items_partial:
            response = requests.get('http://127.0.0.1:5002/details/' + str(item['item_id'])).json()
            new_item = dict(item)
            new_item.update(response)
            items_full.append(new_item)
        self.item.set(items_full)
        ## Fix this

    def filter(self):
        self.item.set(self.item.filter())

class DatabaseItemBuilder(AbstractItemBuilder):
    def __init__(self):
        self.item = Items()

    def get_items(self):
        t_item = self.item
        self.item = Items()
        return t_item

    def get_from_source(self):
        items_table = ItemsDB()
        result = items_table.select_all()
        items_transformed = []
        for row in result:
            dict = {'item_id': row[0], 'item_name': row[1], 'description': row[2], 'quantity': row[3], 'price': row[4], 'supplier_id': row[5]}
            items_transformed.append(dict)
        self.item.set(items_transformed)

    def filter(self):
        self.item.set(self.item.filter())

class BuilderManager:
    def __init__(self):
        self.builder = None
    
    def get_builder(self):
        return self.builder
    
    def set_builder(self, builder):
        self.builder = builder
    
    def build(self):
        self.builder.get_from_source()
        #self.builder.filter()
    