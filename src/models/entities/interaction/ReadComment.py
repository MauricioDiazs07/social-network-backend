class ReadComment():

    def __init__(self, id, name, profile_id, profile_photo,text, share_id, share_type, creation_date ) -> None:
        self.id = id
        self.name = name
        self.profile_id = profile_id
        self.profile_photo = profile_photo
        self.text = text
        self.share_id = share_id
        self.share_type = share_type
        self.creation_date = creation_date

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'profile_id': self.profile_id,
            'profile_photo': self.profile_photo,
            'comment': self.text,
            'share_id': self.share_id,
            'share_type': self.share_type,
            'creation_date': self.creation_date
        }