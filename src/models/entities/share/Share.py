class Share():

    def __init__(self, share_id, name, profile_id, profile_photo, description,share_type,creation_date) -> None:
        self.share_id = share_id
        self.name = name
        self.profile_id = profile_id
        self.profile_photo = profile_photo
        self.description = description
        self.share_type = share_type
        self.creation_date = creation_date
        

    def to_JSON(self):
        return {
            'id': self.share_id,
            'name': self.name,
            'profileId': self.profile_id,
            'profileImage': self.profile_photo,
            'text': self.description,
            'shareType': self.share_type,
            'creationDate': self.creation_date
        }