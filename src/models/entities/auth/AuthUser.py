class AuthUser():

    def __init__(self, email, name, user_type):
        self.email = email
        self.name = name
        self.user_type = user_type

    def to_JSON(self):
        return {
            'email': self.email,
            'name': self.name,
            'user_type': self.user_type
        }