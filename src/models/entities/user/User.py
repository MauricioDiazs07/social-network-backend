class User():

    def __init__(self, full_name, email,usr_password, gender, state, municipality, birthday, role_id, level_id) -> None:
        self.full_name = full_name
        self.email = email
        self.usr_password = usr_password
        self.gender = gender
        self.state = state
        self.municipality = municipality
        self.birthday = birthday
        self.role_id = role_id
        self.level_id = level_id

    def to_JSON(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'usr_password': self.usr_password,
            'gender': self.gender,
            'state': self.state,
            'municipality': self.municipality,
            'birthday': self.birthday,
            'role_id': self.role_id,
            'level': self.level_id
        }