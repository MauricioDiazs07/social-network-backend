class Chat:

    def __init__(self, sender_id, receiver_id, text) -> None:
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.text = text

    def to_JSON(self):
        return {
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'text': self.text
        }