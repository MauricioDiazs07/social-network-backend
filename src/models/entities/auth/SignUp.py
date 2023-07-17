class SignUp():

    def __init__(self,profile_id,email,password,name,gender,state,municipality,colony,street,int_number,ext_number,birthdate,curp,identification_photo):
        self.id = profile_id;
        self.email = email
        self.password = password
        self.name = name
        self.gender = gender
        self.state = state
        self.municipality = municipality
        self.colony = colony
        self.street = street
        self.int_number = int_number
        self.ext_number = ext_number
        self.birthdate = birthdate
        self.curp = curp
        self.identification_photo = identification_photo

    def to_JSON(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'gender': self.gender,
            'state': self.state,
            'municipality': self.municipality,
            'colony': self.colony,
            'street': self.street,
            'int_number': self.int_number,
            'ext_number': self.ext_number,
            'birthdate': self.birthdate,
            'curp': self.curp,
            'identification_photo': self.identification_photo
        }