class ShareMultimedia():

    def __init__(self, id, profile_id, share_type, description, archive_url, archive_type, creation_date) -> None:
        self.id = id
        self.profile_id = profile_id
        self.share_type = share_type
        self.description = description
        self.archive_url = archive_url
        self.archive_type = archive_type
        self.creation_date = creation_date

    def to_JSON(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'share_type': self.share_type,
            'description': self.description,
            'archive_url': self.archive_url,
            'archive_type': self.archive_type,
            'creation_date': self.creation_date,
        }