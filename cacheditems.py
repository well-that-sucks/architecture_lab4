import multiprocessing as mp

from flask_restful import reqparse

from singletondb import *
from itembuilder import *

class ItemsCache():
    def __init__(self):
        self.cache = []

    def update(self):
        q1 = mp.Queue()
        p1 = mp.Process(target = self.main_items, args = (q1))
        q2 = mp.Queue()
        p2 = mp.Process(target = self.service1_items, args = (q2))
        q3 = mp.Queue()
        p3 = mp.Process(target = self.service2_items, args = (q3))
        p1.start()
        p2.start()
        p3.start()
        main_items = q1.get()
        service1_items = q2.get()
        service2_items = q3.get()
        p1.join()
        p2.join()
        p3.join()
        self.cache = main_items.add_items(service1_items).add_items(service2_items)
        print('Cache init finished')
    
    def main_items(self, q):
        builder_manager = BuilderManager()
        builder = DatabaseItemBuilder()
        builder_manager.set_builder(builder)
        builder_manager.build()
        items_from_db = builder.get_items()
        q.put(items_from_db)

    def service1_items(self, q):
        builder_manager = BuilderManager()
        builder = FirstServiceItemBuilder()
        builder_manager.set_builder(builder)
        builder_manager.build()
        items_from_service1 = builder.get_items()
        q.put(items_from_service1)

    def service2_items(self, q):
        builder_manager = BuilderManager()
        builder = SecondServiceItemBuilder()
        builder_manager.set_builder(builder)
        builder_manager.build()
        items_from_service2 = builder.get_items()
        q.put(items_from_service2)

    def get_cache(self, args):
        #item_filter = CompositeFilter(ProductName(), MinQuantity(), SupplierID())
        #filtered_items = []
        #for item in self.cache:
        #    if item_filter.satisfies_filters(item, parsed_args):
        #        filtered_items.append(item)
        
        return self.cache.filter(args)