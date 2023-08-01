class Share():

    def __init__(self, share_id, profile_id, share_type, description) -> None:
        self.share_id = share_id
        self.profile_id = profile_id
        self.share_type = share_type
        self.description = description

    def to_JSON(self):
        return {
            'share_id': self.share_id,
            'profile_id': self.profile_id,
            'share_type': self.share_type,
            'description': self.description
        }