from singletondb import *

class OrdersDB:
    def __init__(self):
        self.conn = DBConnection.get_instance().conn
    
    def select_all(self, obj, info):
        #Work on it
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Orders')
            orders = cursor.fetchall()
        orders_dict = []
        for order in orders:
            orders_dict.append({'order_id': order[0], 'customer_id': order[1], 'item_id': order[2], 'quantity': order[3], 'price': order[4], 'is_confirmed': order[5], 'dmethod_id': order[6], 'address': order[7]})
        return {'success': True, 'order': orders_dict}
    
    def insert(self, obj, info, order_id, customer_id, item_id, quantity, price, is_confirmed, dmethod_id, address):
        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO Orders(OrderID, CustomerID, ItemID, Quantity, Price, IsConfirmed, DeliveryMethodID, DeliveryAddress) VALUES(%s, %s, %s, %s, %s, %s, %s, '%s')'''%(str(order_id), str(customer_id), str(item_id), str(quantity), str(price), str(is_confirmed), str(dmethod_id), address))
        self.conn.commit()
        order_dict = {'order_id': order_id, 'customer_id': customer_id, 'item_id': item_id, 'quantity': quantity, 'price': price, 'is_confirmed': is_confirmed, 'dmethod_id': dmethod_id, 'address': address}
        return {'success': True, 'order': [order_dict]}