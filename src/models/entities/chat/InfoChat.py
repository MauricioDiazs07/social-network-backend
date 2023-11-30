class InfoChat:

    def __init__(self, sender_id, text, name, profile_photo, creation_date, chat_sender) -> None:
        self.sender_id = sender_id
        self.text = text
        self.name = name
        self.profile_photo = profile_photo
        self.creation_date = creation_date
        self.type = 'sender' if sender_id == chat_sender else 'receiver' 

    def to_JSON(self):
        return {
            'sender_id': self.sender_id,
            'message': self.text,
            'name': self.name,
            'profile_photo': self.profile_photo,
            'time': self.creation_date,
            'type': self.type
        }