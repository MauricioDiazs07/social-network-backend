class Like():

    def __init__(self, profile_id, share_id, share_type) -> None:
        self.profile_id = profile_id
        self.share_id = share_id
        self.share_type = share_type

    def to_JSON(self):
        return {
            'profile_id': self.profile_id,
            'share_id': self.share_id,
            'share_type': self.share_type
        }