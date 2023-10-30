from typing import Dict

class INEInfo():
    def __init__(
            self,
            name: str,
            gender: str,
            state: str,
            municipality: str,
            address: str,
            birthday: str,
            curp: str,
            section: str
    ) -> None:
        self.name = name
        self.gender = gender
        self.state = state
        self.municipality = municipality
        self.address = address
        self.birthday = birthday
        self.curp = curp
        self.section = section

    def to_JSON(self) -> Dict[str, str]:
        return {
            'name': self.name,
            'gender': self.gender,
            'state': self.state,
            'municipality': self.municipality,
            'address': self.address,
            'birthday': self.birthday,
            'curp': self.curp,
            'section': self.section
        }