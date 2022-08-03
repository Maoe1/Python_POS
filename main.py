from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import frames
import functions
import sqlite3
import os
from user import User
from product import Product
from order import Order
from orderItem import OrderItem

# object lists
list_users = []
list_products = []
list_orders = []
item_list = []
selected_list = []
list_items_purchased = []
reciepts = []



# database connection to retrieve data
db_file = "db.db"
conn = sqlite3.connect(db_file)
file_exists = os.path.exists(db_file)

try:
    cursor = conn.cursor()
    if  file_exists:
        cursor.execute('''CREATE TABLE IF NOT EXISTS`Order`("orderId"	INTEGER NOT NULL,"userId"	INTEGER NOT NULL,"fname"	TEXT,
        "lname"	TEXT,"cost"	REAL,"quantity"	INTEGER,
        FOREIGN KEY("userId") REFERENCES "User"("userId"),
        PRIMARY KEY("orderId" AUTOINCREMENT));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS"OrderItem" (
        "orderItemId"	INTEGER NOT NULL,
        "orderId"	INTEGER NOT NULL,
        "productId"	INTEGER NOT NULL,
        "productName"	INTEGER,
        "price"	REAL NOT NULL,
        FOREIGN KEY("productId") REFERENCES "Product"("productId"),
        FOREIGN KEY("orderId") REFERENCES "Order"("orderId"),
        PRIMARY KEY("orderItemId"));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS "Product" (
        "productId"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL UNIQUE,
        "price"	REAL NOT NULL,
        "discountTrigger"	TEXT,
        PRIMARY KEY("productId" AUTOINCREMENT));''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS "User" (
        "userId"	INTEGER NOT NULL UNIQUE,
        "fname"	TEXT NOT NULL,
        "lname"	TEXT NOT NULL,
        PRIMARY KEY("userId" AUTOINCREMENT));''')
        conn.commit()
except FileExistsError:
    print("File does not exist!")
except:
    print("some error")

# read reciepts from file to list?

# fetch data
functions.fetch_user_data(list_users)
functions.fetch_product_data(list_products)
functions.fetch_order_data(list_orders)
functions.fetch_items_purchased(list_items_purchased)

style=Style()
style.theme_use('clam')
style.configure("Vertical.TScrollbar", background="green", bordercolor="black", arrowcolor="#87a96b")
style.configure("BW.TLabel", background="#87a96b",  font=("Courier", 12))
# ===============================frame1============================================
# welcome text
welcome_title = Label(frames.frame1, text="Welcome to my Online Store!",background="#004953", foreground="white", style="BW.TLabel",font="Raleway")
welcome_title.place(relx=0.5, rely=0.1, anchor=CENTER)

# menu buttons
menu_button1 = Button(frames.frame1, text="Add User",style="BW.TLabel", width = 50, command=lambda: functions.show_frame(frames.frame2))
menu_button1.config(width=60)
menu_button1.place(relx=0.5, rely=0.3, anchor=CENTER)
menu_button2 = Button(frames.frame1, text="Add Item",style="BW.TLabel", command=lambda: functions.show_frame(frames.frame3))
menu_button2.config(width=60)
menu_button2.place(relx=0.5, rely=0.4, anchor=CENTER)
menu_button3 = Button(frames.frame1, text="Make Order", style="BW.TLabel", command=lambda: functions.show_frame(frames.frame4))
menu_button3.config(width=60)
menu_button3.place(relx=0.5, rely=0.5, anchor=CENTER)
menu_button4 = Button(frames.frame1, style="BW.TLabel", text="Exit", command=lambda: functions.close())
menu_button4.config(width=60)
menu_button4.place(relx=0.5, rely=0.6, anchor=CENTER)

functions.show_frame(frames.frame1)
# ===============================FRAME #2============================================
frame2_title = Label(frames.frame2, text="Add User", font=("Courier", 14), background="#004953", foreground="white",style="BW.TLabel")
frame2_title.grid(row=0, column=0,
                  columnspan=1, rowspan=1, padx=5, pady=5)

first_name_label = Label(frames.frame2, text="Enter first name:",style="BW.TLabel",background="#004953", foreground="white", font=("Courier", 12)).grid(row=2, column=0, sticky=W,pady=2)
last_name_label = Label(frames.frame2, text="Enter last name: ",style="BW.TLabel", background="#004953",foreground="white",font=("Courier", 12)).grid(row=3, column=0,sticky=W, pady=2)
id_label = Label(frames.frame2, text="Enter id:        ",style="BW.TLabel", background="#004953",foreground="white",font=("Courier", 12)).grid(row=4, column=0, sticky=W,pady=2)
first_name = Entry(frames.frame2, width=35, style="BW.TLabel",font=("Courier", 12))
last_name = Entry(frames.frame2, width=35,style="BW.TLabel", font=("Courier", 12))
user_id = Entry(frames.frame2, width=35,style="BW.TLabel", font=("Courier", 12))
first_name.grid(row=2, column=1, pady=2)
last_name.grid(row=3, column=1, pady=2)
user_id.grid(row=4, column=1, pady=2)
submit = Button(frames.frame2, style="BW.TLabel", text="Submit",command=lambda: functions.add_user(first_name, last_name, user_id, list_users))
submit.grid(row=5, column=0, pady=2)
cancel = Button(frames.frame2, style="BW.TLabel", text="Cancel", command=lambda: functions.show_frame(frames.frame1)). \
    grid(row=5, column=1, sticky=W, pady=2)

error= Label(frames.frame2)


# ===============================FRAME #3============================================


frame3_title = Label(frames.frame3, text="Add Product",style="BW.TLabel",background="#004953",foreground="white", font=("Courier", 14))
frame3_title.grid(row=0, column=0,
                  columnspan=1, rowspan=1, padx=5, pady=5)

product_name_label = Label(frames.frame3, text="Enter name: ",background="#004953",foreground="white", font=("Courier", 12)).grid(row=1, column=0, sticky=W, pady=2)
product_price_label = Label(frames.frame3, text="Enter price:", background="#004953",foreground="white",font=("Courier", 12)).grid(row=2, column=0, sticky=W, pady=2)
product_id_label = Label(frames.frame3, text="Enter id:   ", background="#004953",foreground="white", font=("Courier", 12)).grid(row=3, column=0, sticky=W, pady=2)
i=IntVar()
product_discount_checkbox = Checkbutton(frames.frame3,  width=30,text='Discount Trigger',variable=i).grid(row=4, column=1, sticky=W, pady=2)
product_name = Entry(frames.frame3, width=35, style="BW.TLabel", font=("Courier", 12))
product_price = Entry(frames.frame3, width=35, style="BW.TLabel",font=("Courier", 12))
product_id = Entry(frames.frame3, width=35,style="BW.TLabel", font=("Courier", 12))
product_name.grid(row=1, column=1, pady=2)
product_price.grid(row=2, column=1, pady=2)
product_id.grid(row=3, column=1, pady=2)

submit = Button(frames.frame3, text="Submit", style="BW.TLabel", command=lambda: functions.add_product(product_id, product_name, product_price, i, list_products, product_list_box))
submit.grid(row=5, column=0, pady=2)
cancel = Button(frames.frame3, text="Cancel", style="BW.TLabel", command=lambda: functions.show_frame(frames.frame1))
cancel.grid(row=5, column=1, sticky=W, pady=2)

# ===============================FRAME #4============================================
frame4_title = Label(frames.frame4,text="Make Order",background="#004953",foreground="white",style="BW.TLabel", font=("Courier", 14))
frame4_title.grid(row=0, column=0,columnspan=1, rowspan=1, padx=5, pady=5)
order_user_id_label = Label(frames.frame4, text="Enter user ID: ",background="#004953",foreground="white",style="BW.TLabel", font=("Courier", 10))
order_user_id_label.grid(row=10, column=0, sticky=W, pady=2)
cart_label = Label(frames.frame4,background="#004953",foreground="white", text="|| Cart ||",style="BW.TLabel", font=("Courier", 10))
cart_label.grid(row=1, column=4, sticky=W, pady=2)
products_name_label = Label(frames.frame4,background="#004953",foreground="white", text="Prodcuts",style="BW.TLabel",font=("Courier", 10))
products_name_label.grid(row=1, column=1, sticky=W, pady=2)
order_user_id = Entry(frames.frame4, font=("Courier", 10), style="BW.TLabel")
prodcut_list = [product.get_name() for product in list_products]
# for scrolling vertically
yscrollbar = Scrollbar(frames.frame4, orient="vertical")
yscrollbar.grid(row=2, column=2, sticky='ns')
product_list_box = Listbox(frames.frame4, selectmode="multiple", selectforeground='#004953', activestyle='none', yscrollcommand=yscrollbar.set)
product_list_box.grid(row=2, column=1, sticky=W, pady=2)
product_list_box.configure(background="#004953", foreground="white", font=('Aerial 13'))
for product in prodcut_list:
    product_list_box.insert(END, product)
selected_list_box = Listbox(frames.frame4, selectmode="multiple")
selected_list_box.grid(row=2, column=4, sticky=W, pady=2)
selected_list_box.configure(background="#004953", foreground="white", font=('Aerial 13'))
order_user_id.grid(row=10, column=1, pady=2)
add = Button(frames.frame4,style="BW.TLabel", text="Add Items",command=lambda: functions.add_box(product_list_box, selected_list_box))
add.grid(row=2, column=3, pady=2)
delete = Button(frames.frame4, text="Delete", style="BW.TLabel",command=lambda: functions.delete(selected_list_box))
delete.grid(row=4, column=4,pady=2)
submit = Button(frames.frame4, text="Purchase",style="BW.TLabel", command=lambda: functions.make_order(
    order_user_id, selected_list_box, list_orders, list_users, list_products, list_items_purchased, reciept, reciepts))
submit.grid(row=10, column=3)
cancel = Button(frames.frame4, text="Cancel",style="BW.TLabel", command=lambda: functions.show_frame(frames.frame1))
cancel.grid(row=10, column=4)

# ===============================FRAME #5============================================
frame5_title = Label(frames.frame5, text="Reciept", font=("Courier", 14), style="BW.TLabel")
frame5_title.grid(row=0, column=0,columnspan=1, rowspan=1, padx=5, pady=5)
reciept = Label(frames.frame5, text="")
reciept.grid(row= 0, column = 1)
cancel = Button(frames.frame5, style="BW.TLabel", text="Back", command=lambda: functions.show_frame(frames.frame1)). \
    grid(row=10, column=3, sticky=W, pady=2)

frames.root.mainloop()
