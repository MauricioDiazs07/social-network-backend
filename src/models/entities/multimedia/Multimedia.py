class Multimedia():

    def __init__(self, share_id, share_type, archive_url, archive_type) -> None:
        self.share_id = share_id
        self.share_type = share_type
        self.archive_url = archive_url
        self.archive_type = archive_type

    def to_JSON(self):
        return {
            'share_id': self.share_id,
            'share_type': self.share_type,
            'archive_url': self.archive_url,
            'archive_type': self.archive_type
        }