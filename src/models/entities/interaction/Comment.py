class Comment():

    def __init__(self, profile_id, share_id, share_type, text, feeling_id, feeling_percentage) -> None:
        self.profile_id = profile_id
        self.share_id = share_id
        self.share_type = share_type
        self.text = text
        self.feeling_id = feeling_id;
        self.feeling_percentage = feeling_percentage;

    def to_JSON(self):
        return {
            'profile_id': self.profile_id,
            'share_id': self.share_id,
            'share_type': self.share_type,
            'text': self.text,
            'feeling_id': self.feeling_id,
            'feeling_percentage': self.feeling_percentage
        }