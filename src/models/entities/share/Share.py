class Share():

    def __init__(self, profile_id, share_type, description) -> None:
        self.profile_id = profile_id
        self.share_type = share_type
        self.description = description

    def to_JSON(self):
        return {
            'profile_id': self.profile_id,
            'description': self.description
        }