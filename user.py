
class User:
    def __init__(self, id, f_name, l_name):
        self.f_name = f_name
        self.l_name = l_name
        self.id = id

    def get_fullname(self):
        return self.f_name.title() + " " + self.l_name.title()

    def get_id(self):
        return self.id
