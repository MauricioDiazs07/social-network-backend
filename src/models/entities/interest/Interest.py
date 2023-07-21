class Interest():
    
    def __init__(self, profile_id, list_interests) -> None:
        self.profile_id = profile_id
        self.list_interests = list_interests

    def to_JSON(self):
        return {
            'profile_id': self.profile_id,
            'list_interests': self.list_interests
        }