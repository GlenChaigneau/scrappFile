class Notary:

    def __init__(self, name, address, phone, web):
        self.name = name
        self.address = address
        self.phone = phone
        self.web = web

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_phone(self):
        return self.phone

    def get_web(self):
        return self.web

