class User():

    def __init__(self, name,birthday,gender,state,municipality, email, phone_number , profile_photo ) -> None:
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.state = state
        self.municipality = municipality
        self.email = email
        self.phone_number = phone_number
        self.profile_photo = profile_photo

    def to_JSON(self):
        return {
            'name': self.name,
            'birthday': self.birthday,
            'gender': self.gender,
            'state': self.state,
            'municipality': self.municipality,
            'email': self.email,
            'phone_number': self.phone_number,
            'profile_photo': self.profile_photo,
        }