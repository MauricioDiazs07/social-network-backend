class MasterProfile():

    def __init__(self, id, phone_number, area_code,password, gender, name, description,email ) -> None:
        self.id = id
        self.phone_number = phone_number
        self.area_code = area_code
        self.password = password
        self.gender = gender
        self.name = name
        self.description = description
        self.email = email
        self.role_id = 3
        self.profile_photo = None


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
            'profile_photo': self.profile_photo
        }