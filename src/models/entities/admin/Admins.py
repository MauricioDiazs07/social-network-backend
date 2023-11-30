class Admins:

    def __init__(self, admin_id, area_code, phone_number,name) -> None:
        self.admin_id = admin_id
        self.area_code = area_code
        self.phone_number = phone_number
        self.name = name

    def to_JSON(self):
        return {
            'admin_id': self.admin_id,
            'area_code': self.area_code,
            'phone_number': self.phone_number,
            'name': self.name
        }