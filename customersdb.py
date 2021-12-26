from singletondb import *

class CustomersDB:
    def __init__(self):
        self.conn = DBConnection.get_instance().conn
    
    def select_all(self, obj, info):
        #Work on it
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT * FROM Customers')
            customers = cursor.fetchall()
        customers_dict = []
        for customer in customers:
            customers_dict.append({'customer_id': customer[0], 'full_name': customer[1], 'phone': customer[2], 'email': customer[3], 'age': customer[4], 'passport_id': customer[5], 'account_id': customer[6]})
        return {'success': True, 'customer': customers_dict}
    
    def insert(self, obj, info, customer_id, full_name, phone, email, age, passport_id, account_id):
        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO Customers(CustomerID, FullName, Phone, Email, Age, PassportID, AccountID) VALUES(%s, '%s', '%s', '%s', %s, %s, %s)'''%(str(customer_id), full_name, phone, email, str(age), str(passport_id), str(account_id)))
        self.conn.commit()
        customer_dict = {'customer_id': customer_id, 'full_name': full_name, 'phone': phone, 'email': email, 'age': age, 'passport_id': passport_id, 'account_id': account_id}
        return {'success': True, 'customer': [customer_dict]}