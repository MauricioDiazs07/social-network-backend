
class Master():

    def __init__(self, name, description, profile_photo) -> None:
        self.name = name
        self.description = description
        self.profile_photo = profile_photo

    def to_JSON(self):
        return {
            'name': self.name,
            'description': self.description,
            'profile_photo': self.profile_photo
        }