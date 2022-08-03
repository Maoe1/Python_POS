class OrderItem:

    def __init__(self,order_item_id, order_id, product_id, product_name, price):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.price = price
        self.product_name = product_name

    def get_order_item_id(self):
        return self.order_item_id

    def get_order_id(self):
        return self.order_id

    def get_product_id(self):
        return self.product_id

    def get_product_name(self):
        return self.product_name

    def get_price(self):
        return self.price
