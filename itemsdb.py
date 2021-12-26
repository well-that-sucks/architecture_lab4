from singletondb import *

class ItemsDB:
    def __init__(self):
        self.conn = DBConnection.get_instance().conn
    
    def select_all(self):
        #Work on it
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Items')
            items = cursor.fetchall()
        return items

    def insert(self, new_item):
        #print(new_item)
        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO Items(ItemID, ItemName, ItemDescription, QuantityAvailable, Price, SupplierID) VALUES(%s, '%s', '%s', %s, %s, %s)'''%(str(new_item['item_id']), new_item['item_name'], new_item['description'], str(new_item['quantity']), str(new_item['price']), str(new_item['supplier_id'])))
        self.conn.commit()

    def delete(self, item_id):
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM Items WHERE ItemID = ' + str(item_id))
        self.conn.commit()
    
    def update(self, item):
        with self.conn.cursor() as cursor:
            cursor.execute('''UPDATE Items SET ItemName = '%s', ItemDescription = '%s', QuantityAvailable = %s, Price = %s, SupplierID = %s WHERE ItemID = %s'''%(item['item_name'], item['description'], str(item['price']), str(item['quantity']), str(item['supplier_id']), str(item['item_id'])))
        self.conn.commit()