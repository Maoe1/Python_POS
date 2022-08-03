from user import User
from product import Product
from order import Order
from orderItem import OrderItem
from tkinter import *
from tkinter.ttk import *
import frames
import sqlite3
from contextlib import closing
import os
from tkinter import messagebox

# database connection
conn = sqlite3.connect('db.db')


def show_frame(frame):
    frame.tkraise()

def find_current_order_id():
    try:
        with closing(conn.cursor()) as cursor:
            query = '''SELECT orderId FROM `Order`WHERE orderId = (select max(orderId) from `Order`)'''
            cursor.execute(query)
            curr_order_id = cursor.fetchone()
            if curr_order_id is None:
                return 0
            else:
                return curr_order_id[0]
    except sqlite3.OperationalError as e:
        print(str(e))


def find_current_order_item_id():
    try:
        with closing(conn.cursor()) as cursor:
            query = '''SELECT orderItemId FROM orderItem WHERE orderItemId = (select max(orderItemId) from orderItem)'''
            cursor.execute(query)
            curr_order_item_id = cursor.fetchone()
            if curr_order_item_id is None:
                return 0
            else:
                return curr_order_item_id[0]
    except sqlite3.OperationalError as e:
        print(str(e))


def add_box(product_list_box, selected_list_box):
    for i in product_list_box.curselection():
        selected_list_box.insert(END, product_list_box.get(i))
    return selected_list_box


def delete(selected_list_box):
    selected_item = selected_list_box.curselection()
    for item in selected_item[::-1]:
        selected_list_box.delete(item)
    return selected_list_box


def find_product_cost(name, list_products):
    for product in list_products:
        if product.get_name() == name:
            cost = product.get_price()
    return cost


def find_product_id(name, list_products):
    for product in list_products:
        if product.get_name() == name:
            product_id = product.get_id()
    return product_id





def fetch_user_data(list_users):

    try:
        with closing(conn.cursor()) as cursor:
            query = '''SELECT * FROM User'''
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                new_user = User(row[0], row[1], row[2])
                list_users.append(new_user)
            return list_users
    except sqlite3.OperationalError as e:
        print(str(e))


def fetch_product_data(list_products):
    try:
        with closing(conn.cursor()) as cursor:
         query = '''SELECT * FROM Product'''
         cursor.execute(query)
         rows = cursor.fetchall()
        for row in rows:
            new_product = Product(row[0], row[1], row[2], row[3])
            list_products.append(new_product)
        return list_products
    except sqlite3.OperationalError as e:
        print(str(e))



def fetch_order_data(list_orders):
    try:
        with closing(conn.cursor()) as cursor:
            query = '''SELECT * FROM `Order`'''
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                new_order = Order(row[0], row[1], row[2], row[3], row[4], row[5])
                list_orders.append(new_order)
            return list_orders
    except sqlite3.OperationalError as e:
        print(str(e))


def fetch_items_purchased(list_items_purchased):
    try:
        with closing(conn.cursor()) as cursor:
            query = '''SELECT * FROM `orderItem`'''
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                new_item_purchased = OrderItem(row[0], row[1], row[2], row[3], row[4])
                list_items_purchased.append(new_item_purchased)
            return list_items_purchased
    except sqlite3.OperationalError as e:
        print(str(e))


def print_users(list_users):
    for user in list_users:
        print(str(user.get_id()) + " " + str(user.get_fullname()))


def print_products(list_prodcuts):
    for product in list_prodcuts:
        print(str(product.get_id()) + " " + str(product.get_name()) + " " + str(product.get_price()))


def add_user(f_name, l_name, id, list_users):
    id_list = [user.get_id() for user in list_users]
    user_id = ''.join(id.get().split())
    first_name = ''.join(f_name.get().split()).lower()
    last_name = ''.join(l_name.get().split()).lower()
    if not user_id.isnumeric():
        print("Error: Id must be an integer")
        id.delete(0, END)
        return show_frame(frames.frame2)
    elif int(user_id) in id_list:
        print("Error: Id already exists")
        id.delete(0, END)
        return show_frame(frames.frame2)
    elif first_name.isnumeric() or last_name.isnumeric():
        print("Error: user name must be only letters!")
        f_name.delete(0, END)
        l_name.delete(0, END)
        return show_frame(frames.frame2)
    else:
        list_users.append(User(int(user_id), first_name, last_name))
        db_user = [int(user_id), first_name, last_name]
        try:
            with closing (conn.cursor())as cursor:
                query = ''' INSERT INTO User (userId, fname, lname) VALUES(?,?,?) '''
                cursor.execute(query, db_user)
                conn.commit()
        except sqlite3.OperationalError as e:
            print(str(e))

        f_name.delete(0, END)
        l_name.delete(0, END)
        id.delete(0, END)
        user_file = "user.txt"
        with open(user_file, 'a') as my_file:
            my_file.write(str(list_users[-1].get_id()) + " " + str(list_users[-1].get_fullname()))
            my_file.write("\n")
        return show_frame(frames.frame1), list_users


def find_username_by_id(id, list_users):
    for user in list_users:
        if user.get_id() == int(id):
            full_name = user.get_fullname()
    return full_name


def add_product(id, name, price, i, list_products, product_list_box):

    id_list = [product.get_id() for product in list_products]
    name_list = [product.get_name() for product in list_products]
    product_id = ''.join(id.get().split())
    product_price = ''.join(price.get().split())
    product_name = ''.join(name.get().split())

    if not product_id.isnumeric():
        paint("Error: Id must be a number!")
        id.delete(0, END)
        return show_frame(frames.frame3)
    elif  int(product_id) in id_list:
        print("Error: Id already exists!")
        id.delete(0, END)
        return show_frame(frames.frame3)
    elif not float(product_price):
        price.delete(0, END)
        return show_frame(frames.frame3)
    elif product_name.isnumeric() :
        print("Error: Please enter valid name for product")
        name.delete(0, END)
        return show_frame(frames.frame3)
    elif product_name.lower() in name_list:
        print("Error: name already exists")
        name.delete(0, END)
        return show_frame(frames.frame3)
    else:
        if int(i.get()) == 1:
            discount_trigger = "yes"
        else:
            discount_trigger = "no"

        product_price = round(float(product_price), 2)
        list_products.append(Product(int(product_id), str(product_name.lower()), float(product_price), str(discount_trigger)))
        db_product = [int(product_id), str(product_name.lower()), float(product_price), str(discount_trigger)]
        try:
            with closing (conn.cursor()) as cursor:
                query = ''' INSERT INTO Product(productId, name, price, discountTrigger) VALUES(?,?,?,?) '''
                cursor.execute(query, db_product)
                conn.commit()
        except sqlite3.OperationalError as e:
            print(str(e))

        id.delete(0, END)
        name.delete(0, END)
        price.delete(0, END)
        product_list_box.insert(END, product_name.lower())
        product_file = "product.txt"
        with open(product_file, 'a') as my_file:
            my_file.write(str(list_products[-1].get_id()) + " " + str(list_products[-1].get_name()) + " " + str(list_products[-1].get_price()))
            my_file.write("\n")

        return show_frame(frames.frame1), list_products


def is_discount_triggered(item, list_products):
    for product in list_products:
        if product.get_name() == item:
            if product.discount_offered() == "yes":
                return 1
            else:
                return 0


def make_order(user_id, selected_list_box, list_orders, list_users, list_products, list_items_purchased, reciept, reciepts):

    curr_order_id = find_current_order_id()
    curr_order_item_id = find_current_order_item_id()
    item_list = []
    combo_count = 0
    cost = 0

    # calculate cost based on combo items
    for j in selected_list_box.curselection():
        combo_count += is_discount_triggered(selected_list_box.get(j), list_products)
    for i in selected_list_box.curselection():
        item_list.append(selected_list_box.get(i))
        if combo_count > 1:
            if is_discount_triggered(selected_list_box.get(i), list_products) == 1:
                cost += find_product_cost(selected_list_box.get(i), list_products) * 0.86 #discount offered on combo items
            else:
                cost += find_product_cost(selected_list_box.get(i), list_products)
        else:
            cost += find_product_cost(selected_list_box.get(i), list_products)


    # check if user selected items from cart
    if item_list == []:
        print("Error: No items have been selected in cart!")
        messagebox.showerror("Error", "Please select from items from cart!")
        return  show_frame(frames.frame4)

    # Id validation
    id_list = [user.get_id() for user in list_users]
    id = ''.join(user_id.get())
    if not id.isnumeric():
        user_id.delete(0, END)
        raise ValueError("Error: Id must be an Integer")
        return show_frame(frames.frame4)
    elif not int(id) in id_list:
        print("Error: Id does not exist!")
        user_id.delete(0, END)
        selected_list_box.delete(0, END)
        return show_frame(frames.frame4)
    else:
        full_name = find_username_by_id(id, list_users)
        first, *last = full_name.split()
        quantity = len(item_list)
        curr_order_id = curr_order_id + 1
        cost = round(cost, 2)
        list_orders.append(Order(int(curr_order_id), int(id), str(first), str(*last), float(cost), int(quantity)))
        db_order = [int(curr_order_id), int(id),str(first), str(*last), float(cost), int(quantity)]
        try:
            with closing (conn.cursor()) as cursor:
                query = ''' INSERT INTO `Order`(orderId, userId, fname, lname, cost, quantity) VALUES(?,?,?,?,?,?) '''
                cursor.execute(query, db_order)
                conn.commit()
        except sqlite3.OperationalError as e:
            print(str(e))

        for item in item_list:
            curr_order_item_id = curr_order_item_id + 1
            product_id = find_product_id(item.lower(), list_products)
            product_price = find_product_cost(item.lower(), list_products)
            item_order = OrderItem(int(curr_order_item_id), int(curr_order_id), int(product_id), str(item.lower()), float(product_price))
            list_items_purchased.append(item_order)
            db_order_item = [int(curr_order_item_id), int(curr_order_id), int(product_id), str(item.lower()),float(product_price)]
            try:
                with closing(conn.cursor()) as cursor:
                   query = ''' INSERT INTO OrderItem(orderItemId, orderId, productId, productName, price) VALUES(?,?,?,?,?) '''
                   cursor.execute(query, db_order_item)
                   conn.commit()
            except sqlite3.OperationalError as e:
                print(str(e))
            order_item_file = "orderItem.txt"
            with open(order_item_file, 'a') as my_file:
                my_file.write(
                str(item_order.get_order_item_id()) + " " + str(item_order.get_order_id()) + " " + str(
                item_order.get_product_id()) + " " +
                str(item_order.get_product_name()) + " " + str(item_order.get_price()))
                my_file.write("\n")

        user_id.delete(0, END)
        selected_list_box.delete(0, END)

        order_file = "order.txt"
        with open(order_file, 'a') as my_file:
            my_file.write(str(list_orders[-1].get_order_id()) + " " + str(list_orders[-1].get_user_id()) + " " + str(
            list_orders[-1].get_fullname()) + " " + str(list_orders[-1].get_cost()))
            my_file.write("\n")

        # SAVE AND PRINT RECIEPT:
        reciept.config(text=list_orders[-1].print_order(), font=('Aerial 13'))
        reciepts.append(list_orders[-1].print_order())
        reciept_file = "reciepts.txt"
        with open(reciept_file, 'a') as my_file:
            my_file.write(str(list_orders[-1].print_order()))
            my_file.write("\n\n")
        return list_orders, list_items_purchased, reciepts, show_frame(frames.frame5)



def close():
   #win.destroy()
   frames.root.quit()