from src.models.entities.states.States import STATES, MUNICIPALITIES

months = [
  'enero',
  'febrero',
  'marzo',
  'abril',
  'mayo',
  'junio',
  'julio',
  'agosto',
  'septiembre',
  'octubre',
  'noviembre',
  'diciembre'
]

def format_date_to_front(date: str) -> str:
    day = date[-2:]
    month = date[5:7]
    month = months[int(month)-1]
    month = month[0].upper() + month[1:]
    year = date[:4]
    return f'{day}-{month}-{year}'

def format_date_to_DB(date: str) -> str:
    day = date.split("-")[0]
    month = date.split("-")[1]
    month = months.index(month.lower()) + 1
    month = month if month >= 10 else f'0{month}'
    year = date.split("-")[2]
    return f'{year}-{month}-{day}'

def getGender(gender_: str) -> str:
    if gender_ == 'female':
        return 'M'
    
    return 'H'

def getState(state_: str) -> str:
    return STATES[state_]

def getMunicipality(state_:str, mun_: str) -> str:
    return MUNICIPALITIES[state_][mun_]