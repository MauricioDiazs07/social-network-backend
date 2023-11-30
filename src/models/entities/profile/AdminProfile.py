class AdminProfile():

    def __init__(self, id,name, phone_number, area_code,password, master_id) -> None:
        self.id = id
        self.phone_number = phone_number
        self.area_code = area_code
        self.password = password
        self.gender = 'N'
        self.name = name
        self.description = None
        self.email = None
        self.role_id = 2
        self.profile_photo = None
        self.master_id = master_id


    def to_JSON(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'area_code': self.area_code,
            'password': self.password,
            'gender': self.gender,
            'name': self.name,
            'description': self.description,
            'email': self.email,
            'role_id': self.role_id,
            'profile_photo': self.profile_photo,
            'master_id': self.master_id
        }