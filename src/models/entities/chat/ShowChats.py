class ShowChats:

    def __init__(self, name,sender_id, receiver_id, message, time, imageUrl) -> None:
        self.name = name
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.time = time
        self.imageUrl = imageUrl
        self.pending = 0
    
    def to_JSON(self):
        return {
            'name': self.name,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'message': self.message,
            'time': self.time,
            'imageUrl': self.imageUrl,
            'pending': self.pending
        }