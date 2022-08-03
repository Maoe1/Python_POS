from user import User
import sqlite3
from contextlib import closing
class Order(User):

    def __init__(self,order_id, user_id, f_name, l_name, cost, quantity):
        super().__init__(user_id, f_name, l_name)
        self.user_id = user_id
        self.cost = cost
        self.order_id = order_id
        self.quantity = quantity


    def get_order_id(self):
        return self.order_id

    def get_user_id(self):
        return self.user_id

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def get_list_items(self):
        new_list = []
        conn = sqlite3.connect('db.db')
        try:
            with closing(conn.cursor()) as cursor:
                query = '''SELECT productName FROM OrderItem WHERE orderId = ?'''
                db_id = self.get_order_id()
                cursor.execute(query, [db_id])
                items = cursor.fetchall()
                for x in items:
                    new_list.append(*x)
                new_list = ', '.join(new_list)
        except sqlite3.OperationalError as e:
            print(str(e))
        return new_list




    def  print_order(self):
        s = ""
        s +="\n*-----************ ORDER RECIEPT ************------------*\n"
        s +="\n||     Order number: " + str(self.get_order_id()) + '\n'
        s +="\n||     User Name: " + str(super().get_fullname()) +'\n'
        s +="\n||     Number of Items: " + str(self.get_quantity()) +'\n'
        s +="\n||     Total Cost: " + str(self.get_cost())+'\n'
        s +="\n       Items baught: " + str(self.get_list_items())+'\n'
        s+="\n*---------------------------------------------------------------------*"
        return s

        #print("*-----************ ORDER RECIEPT ************------------*")
        #print("||     Order number:" + str(self.get_order_id()))
        #print("||     User Name: " + str(super().get_fullname()))
        #print("||     number of items: " + str(self.get_quantity()))
        #print("||     Total Cost: " + str(self.get_cost()))
        #print("      Items baught:" + str(self.get_list_items()))
        #print("*--------------------------------------------------------*")

