from flask_restful import reqparse

class CompositeFilter:
    def __init__(self, *args):
        self.filters = list(args)
    
    def satisfies_filters(self, item, parsed_args):
        flag = True
        for filter in self.filters:
            flag = flag and filter.satisfies(item, parsed_args)
        return flag

class Filter:
    def satisfies(self, item):
        pass

class ProductName(Filter):
    def satisfies(self, item, parsed_args):
        #parser = reqparse.RequestParser()
        #parser.add_argument('item_name')
        #parsed_args = parser.parse_args()
        return item['item_name'] == parsed_args['item_name'] if parsed_args['item_name'] else True
        
class MinQuantity(Filter):
    def satisfies(self, item, parsed_args):
        #parser = reqparse.RequestParser()
        #parser.add_argument('min_quantity')
        #parsed_args = parser.parse_args()
        return int(item['quantity']) > int(parsed_args['min_quantity']) if parsed_args['min_quantity'] else True
        
class SupplierID(Filter):
    def satisfies(self, item, parsed_args):
        #parser = reqparse.RequestParser()
        #parser.add_argument('supplier_id')
        #parsed_args = parser.parse_args()
        return int(item['supplier_id']) == int(parsed_args['supplier_id']) if parsed_args['supplier_id'] else True
