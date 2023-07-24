from typing import Dict

class SignUp():
    def __init__(
            self,
            email: str,
            password: str,
            name: str,
            gender: str,
            state: str,
            municipality: str,
            colony: str,
            street: str,
            int_number: str,
            ext_number: str,
            birthdate: str,
            curp: str,
            identification_photo: str
    ) -> None:
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

    def to_JSON(self) -> Dict[str, str]:
        return {
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