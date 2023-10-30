class Login():

    def __init__(self, phone, password):
        self.phone = phone
        self.password = password

    def to_JSON(self):
        return {
            'phone': self.phone,
            'password': self.password
        }