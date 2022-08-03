class Product:
    def __init__(self, id, name, price, discount_trigger):
        self.id = id
        self.name = name
        self.price = price
        self.discount_trigger = discount_trigger


    def get_id(self):
        return self.id

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name

    def discount_offered(self):
        return self.discount_trigger