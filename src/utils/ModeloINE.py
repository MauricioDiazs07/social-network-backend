from src.models.entities.auth.INEInfo import INEInfo
from src.utils._support_functions import format_date_to_front,\
                                         preprocessText, \
                                         validateCURP, \
                                         validateGender, \
                                         validateCode
from typing import Dict
from PIL import Image
import pickle
import shutil

MODEL_PATH = 'src/resources/models/model_read.pkl'
img_names = {
    "header": "INE-cabecera.png",
    "state": "INE-estado.png",
    "name": "INE-nombre.png",
    "address": "INE-domicilio.png",
    "birthDate": "INE-fechaDeNacimiento.png",
    "curp": "INE-curp.png",
    "gender": "INE-genero.png",
    "municipality": "INE-municipio.png",
    "section": "INE-seccion.png",
    "others": "INE-otros.png"
}
pos = {
    "old": {
        "name": [0.28, 0.26, 0.7, 0.46],
        "address": [0.30, 0.44, 0.825, 0.69],
        "birthDate": [0.76, 0.28, 0.98, 0.365],
        "curp": [0.29, 0.705, 0.68, 0.79],
        "gender": [0.91, 0.33, 0.97, 0.445],
        "municipality": [0.615, 0.76, 0.70, 0.84],
        "section": [0.68, 0.75, 0.87, 0.83],
    },
    "new": {
        "name": [0.28, 0.26, 0.7, 0.52],
        "address": [0.30, 0.49, 0.825, 0.705],
        "birthDate": [0.30, 0.84, 0.57, 0.96],
        "curp": [0.30, 0.74, 0.67, 0.855],
        "gender": [0.83, 0.25, 0.98, 0.38],
        "municipality": [0.615, 0.76, 0.70, 0.84],
        "section": [0.68, 0.75, 0.87, 0.83],
    }
}

with open(MODEL_PATH, 'rb') as f:
    reader2 = pickle.load(f)

def saveCropCredential(
        c_width_start: float,
        c_height_start: float,
        c_width_end: float,
        c_height_end: float,
        path: str,
        file_name: str,
        INE
    ) -> None:
    INE.crop((c_width_start, c_height_start, c_width_end, c_height_end)) \
        .save(path + file_name)

def validCredential(
        width: int,
        height: int,
        path: str,
        INE
    ) -> bool:
    """
        Checks if the lecture of the credential has information

        Inputs:
            width: width of the image
            height: height of the image
            path: path of the img resources
            INE: image

        Outputs:
            boolean - True if the lecture has information, otherwise, False
        
    """
    saveCropCredential(width*0.0, height*0.0, width*1.0, height*0.5, path, img_names['header'], INE)
    result = reader2.readtext(path + img_names['header'], detail = 0)

    for element in result:
        if "INSTITUTO" in element or "NACIONAL" in element or "ELECTORAL" in element:
            return True
        
    return False
    
def removeFolder(path: str) -> None:
    """
        Removes a folder from system

        Inputs:
            path: path of the folder
        
    """
    try:
        shutil.rmtree(path)
    except Exception as ex:
        print("The path couldn't be removed", ex)

def getState(
        width: str,
        height: str,
        path: str,
        INE
) -> str:
    """
        Gets the state from the credential

        Inputs:
            width: width of the image
            height: height of the image
            path: path of the img resources
            INE: image

        Outputs:
            str - state code from credential
        
    """
    saveCropCredential(width*0.30, height*0.78, width*0.50, height*0.9, path, img_names['state'], INE)
    estado = reader2.readtext(path + img_names['state'], detail = 0)
    try:
        estado = estado[-1]
        estado_id = estado

        return estado_id
    except Exception as ex:
        print(ex)
        return "", ""
    
def readField(
        path: str,
        file_name: str
) -> str:
    """
        read an specific field of the credential

        Inputs:
            path: path of the img resources
            file_name: name of the file

        Outputs:
            str - 
    """
    text_ = reader2.readtext(path + file_name, detail = 0)
    print(file_name, text_)

    if (type(text_) == list):
        text_ = " ".join(text_).upper()

    if (file_name == img_names['gender']):
        text_ = validateGender(text_)

    if (file_name == img_names['state']):
        text_ = validateCode(text_, reps=2)
    
    if (file_name == img_names['municipality']):
        text_ = validateCode(text_, reps=3)

    if (file_name == img_names['section']):
        text_ = validateCode(text_, reps=4)

    return preprocessText(text_)
    
def extractInformation(
        width: str,
        height: str,
        path: str,
        pos: Dict,
        INE
) -> str:
    """
        Crops the INE img and extracts the information by parts

        Inputs:
            width: width of the image
            height: height of the image
            path: path of the img resources
            INE: image

        Outputs:
            boolean - True if the lecture has information, otherwise, False
        
    """
    saveCropCredential(width*pos['name'][0], height*pos['name'][1], width*pos['name'][2], height*pos['name'][3], path, img_names['name'], INE)
    nombre = readField(path, img_names['name'])
    
    saveCropCredential(width*pos['address'][0], height*pos['address'][1], width*pos['address'][2], height*pos['address'][3], path, img_names['address'], INE)
    domicilio = readField(path, img_names['address'])

    saveCropCredential(width*pos['birthDate'][0], height*pos['birthDate'][1], width*pos['birthDate'][2], height*pos['birthDate'][3], path, img_names['birthDate'], INE)
    fechaDeNacimiento = readField(path, img_names['birthDate'])
    
    saveCropCredential(width*pos['curp'][0], height*pos['curp'][1], width*pos['curp'][2], height*pos['curp'][3], path, img_names['curp'], INE)
    curp = readField(path, img_names['curp'])
    curp = validateCURP(curp, fechaDeNacimiento)

    try:
        genero = curp[10]
    except:
        saveCropCredential(width*pos['gender'][0], height*pos['gender'][1], width*pos['gender'][2], height*pos['gender'][3], path, img_names['gender'], INE)
        genero = readField(path, img_names['gender'])

    saveCropCredential(width*pos['municipality'][0], height*pos['municipality'][1], width*pos['municipality'][2], height*pos['municipality'][3], path, img_names['municipality'], INE)
    municipality = readField(path, img_names['municipality'])

    saveCropCredential(width*pos['section'][0], height*pos['section'][1], width*pos['section'][2], height*pos['section'][3], path, img_names['section'], INE)
    seccion = readField(path, img_names['section'])

    return nombre, domicilio, fechaDeNacimiento, curp, genero, municipality, seccion
            
def ModeloIne(
        filename: str,
        path: str
    ) -> Dict[str, str]:
    """
        Function that reads the information from the INE

        Inputs:
            filename: name of the img stored
            path: path of the img resources

        Outputs:
            Dict - dict with INEInfo class structure
        
    """
    INE = Image.open(filename)
    width, height = INE.width, INE.height
 
    for _ in range(4):
        credencialValida = validCredential(width, height, path, INE)
        if credencialValida:
            break
        INE = INE.rotate(90)
    
    emision = 0
    if credencialValida:
        saveCropCredential(width*0.30, height*0.755, width*0.88, height*0.945, path, img_names['others'],  INE)
        result = reader2.readtext(path + img_names['others'], detail = 0)
        emision = result[-1].split()[-1]
        if emision.isnumeric(): 
            emision = int(emision)-10
        else: # podria estar ligeramente rotada
            INE = INE.rotate(-3)
            saveCropCredential(width*0.30, height*0.755, width*0.88, height*0.945, path, img_names['others'], INE)
            result = reader2.readtext(path + img_names['others'], detail = 0)
            ''.join(result)
            emision = result[-1].split()[-1]
            if emision.isnumeric(): 
                emision = int(emision)-10
            else:
                credencialValida = False

    if not credencialValida:
        removeFolder(path)
        return {}

    if int(emision) < 2020:
        print("1")
        pos_ = pos['old']

    if int(emision) >= 2020:
        print("2")
        pos_ = pos['new']
        
    nombre, domicilio, fechaDeNacimiento, curp, genero, municipality, seccion = extractInformation(width, height, path, pos_, INE)
    
    estado = getState(
        width,
        height,
        path,
        INE
    )

    removeFolder(path)

    ine_info = INEInfo(
                        nombre,
                        genero,
                        estado,
                        municipality,
                        domicilio,
                        format_date_to_front(fechaDeNacimiento),
                        curp,
                        seccion
                )
    
    return ine_info.to_JSON()