from typing import Dict

class SignUp():
    def __init__(
            self,
            profile_id,
            email,
            password,
            name,
            gender,
            state,
            municipality,
            address,
            birthdate,
            curp,
            identification_photo,
            phone,
            profile_photo,
            section
        ) -> None:
        self.id = profile_id
        self.email = email
        self.password = password
        self.name = name
        self.gender = gender
        self.state = state
        self.municipality = municipality
        self.address = address
        self.birthdate = birthdate
        self.curp = curp
        self.identification_photo = identification_photo
        self.phone = phone
        self.profile_photo = profile_photo
        self.section = section

    def to_JSON(self) -> Dict[str, str]:
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'gender': self.gender,
            'state': self.state,
            'municipality': self.municipality,
            'address': self.address,
            'birthdate': self.birthdate,
            'curp': self.curp,
            'identification_photo': self.identification_photo,
            'phone': self.phone,
            'profile_photo': self.profile_photo,
            'section': self.section
        }