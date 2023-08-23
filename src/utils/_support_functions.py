from src.models.entities.states.States import STATES, MUNICIPALITIES
from datetime import datetime
import math
import re

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
form_names = ['NOMBRE', 'DOMICILIO', 'CURP', 'ESTADO', 'MUNICIPIO', 'SECCION', 'LOCALIDAD', 'EMISION', 'VIGENCIA', 'UN ', 'INE', 'CLAVE DE ELECIUR', 'ANO 0E rEGISTRU', 'ANO 0E REGISTRU', 'FECHA DE NACIMIENTO', 'ANO DE REGISTRO', 'FECHA DE NACIMIEN', 'AÑODEREGISTRO', 'AÑODEREGISTF', 'ÑO DE REGISTRO']

def format_date_to_front(date: str) -> str:
    try:
        day = date.split("/")[0]
        month = date.split("/")[1]
        month = months[int(month)-1]
        month = month[0].upper() + month[1:]
        year = date.split("/")[2]
        return f'{day}-{month}-{year}'
    except:
        return ''

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

def preprocessText(text: str) -> str:
    """
        Removes extra information in a text field from INE

        Inputs:
            text: read field from credential

        Outputs:
            string - clean text
        
    """
    text = text.replace('á', 'a')
    text = text.replace('é', 'e')
    text = text.replace('í', 'i')
    text = text.replace('ó', 'o')
    text = text.replace('ú', 'u')

    for word in form_names:
        text = text.replace(word, '')

    return text.strip()

def replaceNum(text: str) -> str:
    text = text.lower()
    text = text.replace("s", "5")
    text = text.replace("o", "0")
    text = text.replace("ô", "6")
    text = text.replace("i", "1")
    text = text.replace("l", "1")
    text = text.replace("g", "6")
    text = text.replace("z", "2")
    text = text.replace("b", "8")

    return text

def validateCURP(
    curp: str,
    birthDate: str
) -> str:
    curp = curp.split()
    for element in curp:
        if len(element) == 18:
            curp = element
            break

    if (type(curp) == list):
        return ''
    
    bd_part = birthDate.split("/")[::-1]
    bd_part = ''.join([x[-2:] for x in bd_part])
    curp = curp[:4] + replaceNum(curp[4:10]) + curp[10:]

    if (replaceNum(curp[4:10]) != bd_part):
        curp = curp[:4] + bd_part + curp[10:]

    curp = curp[:-2] + replaceNum(curp[-2:])

    return curp

def validateGender(gend: str) -> str:
    if "H" in gend:
        gend = "H"
    elif "M" in gend:
        gend = "M"
    else:
        gend = ""

    return gend

def validateCode(code: str, reps: int) -> str:
    code = replaceNum(code)
    re_ ='^(\d{' + str(reps) + '})$'
    re_ = re.match(re_, code)

    if (re_):
        return code
    else:
        return ''
    
def reformatCreatedDate(date: datetime) -> str:
    current_date = datetime.today()
    time_diff = current_date - date
    time_diff_hours = time_diff.seconds / 3600
    time_diff_min = time_diff.seconds - (math.floor(time_diff_hours) * 3600)
    time_diff_min = round(time_diff_min / 60)

    if (time_diff.days == 0 and time_diff_hours < 1 and time_diff_min < 2):
        return 'Ahora'

    elif (time_diff.days == 0):
        time = round(time_diff_hours) if time_diff_hours >= 1 else time_diff_min
        measure = 'horas' if time_diff_hours >= 1 else 'minutos'
        return f'Hace {time} {measure}'

    elif (time_diff.days == 1):
        return 'Ayer'
    
    else:
        date = f'{date.day}/{date.month}/{date.year}'
        return format_date_to_front(date)