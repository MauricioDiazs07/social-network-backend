class AuthUser():

    def __init__(self, profile_id, email, name, role_id, password):
        self.id = profile_id
        self.email = email
        self.name = name
        self.role_id = role_id,
        self.password = password

    def to_JSON(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role_id': self.role_id,
            'password': self.password
        }