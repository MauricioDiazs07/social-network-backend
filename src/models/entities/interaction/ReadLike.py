class ReadLike():

    def __init__(self, profile_id, name, share_id, share_type) -> None:
        self.profile_id = profile_id
        self.name = name
        self.share_id = share_id
        self.share_type = share_type

    def to_JSON(self):
        return {
            'profile_id': self.profile_id,
            'name': self.name,
            'share_id': self.share_id,
            'share_type': self.share_type
        }