class InfoChat:

    def __init__(self, sender_id, text, name, profile_photo, creation_date) -> None:
        self.sender_id = sender_id
        self.text = text
        self.name = name
        self.profile_photo = profile_photo
        self.creation_date = creation_date

    def to_JSON(self):
        return {
            'sender_id': self.sender_id,
            'text': self.text,
            'name': self.name,
            'profile_photo': self.profile_photo,
            'creation_date': self.creation_date
        }