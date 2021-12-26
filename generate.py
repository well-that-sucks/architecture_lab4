from singletondb import *
import pyodbc as db
import random

def generate_random_str():
    str = ''
    for i in range(10):
        char = chr(random.randint(97, 122))
        str += char
    return str


descriptions = ['Whiskey', 'Cidr', 'Beer', 'Liquor', 'Vodka', 'Rome']

#conn = DBConnection.get_instance().conn
#with conn.cursor() as cursor:
#    for i in range(3, 100001):
#        cursor.execute('''INSERT INTO Items(ItemID, ItemName, ItemDescription, QuantityAvailable, Price, SupplierID) VALUES(%s, '%s', '%s', %s, %s, %s)'''%(str(i), generate_random_str(), descriptions[random.randint(0, 5)], str(random.randint(10, 1000)), str(random.randint(100, 1000)), str(random.randint(1, 10))))
#conn.commit()

conn = db.connect('Driver={SQL Server};Server=DESKTOP-69AKAQS;Database=Service1;Trusted_Connection=yes;')
#with conn.cursor() as cursor:
#    for i in range(100001, 150001):
#        cursor.execute('''INSERT INTO Prices(ItemID, ItemName, Price) VALUES(%s, '%s', %s)'''%(str(i), generate_random_str(), str(random.randint(100, 1000))))
#        cursor.execute('''INSERT INTO Details(ItemID, ItemDescription, QuantityAvailable, SupplierID) VALUES(%s, '%s', %s, %s)'''%(str(i), descriptions[random.randint(0, 5)], str(random.randint(10, 1000)), str(random.randint(1, 10))))
#
#conn.commit()
with conn.cursor() as cursor:
    cursor.execute(f'SELECT * FROM Details WHERE ItemID = {100001}')
    items = cursor.fetchall()
item = {'item_id': items[0][0], 'description': items[0][1], 'quantity': items[0][2], 'supplier_id': items[0][3]}
print(item)
