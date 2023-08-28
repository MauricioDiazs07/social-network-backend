class Profile():

    def __init__(self, email, name,gender, profile_photo, description ) -> None:
        self.email = email
        self.name = name
        self.gender = gender
        self.profile_photo = profile_photo
        self.description = description

    def to_JSON(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'email': self.email,
            'profile_photo': self.profile_photo,
            'description': self.description
        }