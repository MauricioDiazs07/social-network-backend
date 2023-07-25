from src.models.entities.auth.INEInfo import INEInfo
from src.utils._support_functions import format_date_to_front, format_date_to_DB
from typing import Dict
from PIL import Image
import pickle
import shutil

MODEL_PATH = 'src/resources/models/model_read.pkl'

with open(MODEL_PATH, 'rb') as f:
        reader2 = pickle.load(f)

def validCredential(
        width: int,
        height: int,
        path: str,
        INE
    ) -> bool:
    cabeceraRecorte = INE.crop((width*0.0, height*0.0, width*1.0, height*0.5))
    cabeceraRecorte.save(path + "INE-cabecera.png")

    result = reader2.readtext(path + "INE-cabecera.png", detail = 0)
    for element in result:
        if "INSTITUTO" in element or "NACIONAL" in element or "ELECTORAL" in element:
            return True
        
    return False

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
    
def removeFolder(path: str) -> None:
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
    saveCropCredential(width*0.30, height*0.78, width*0.50, height*0.9, path, "INE-estado.png", INE)
    estado = reader2.readtext(path + f"INE-estado.png", detail = 0)
    try:
        estado = estado[-1]
        estado_id = estado

        return estado_id
    except Exception as ex:
        print(ex)
        return "", ""
            
def ModeloIne(
        filename: str,
        path: str
    ) -> Dict[str, str]:
    INE = Image.open(filename)
    width, height = INE.width, INE.height

    for i in range(4):
        credencialValida = validCredential(width, height, path, INE)
        if credencialValida:
            break
        INE = INE.rotate(90)
    
    emision = 0
    if credencialValida:
        saveCropCredential(width*0.30, height*0.755, width*0.88, height*0.945, path, "INE-otros.png",  INE)
        result = reader2.readtext(path + "INE-otros.png", detail = 0)
        emision = result[-1].split()[-1]
        if emision.isnumeric(): 
            emision = int(emision)-10
        else: # podria estar ligeramente rotada
            INE = INE.rotate(-3)
            saveCropCredential(width*0.30, height*0.755, width*0.88, height*0.945, path, "INE-otros.png", INE)
            result = reader2.readtext(path + "INE-otros.png", detail = 0)
            ''.join(result)
            emision = result[-1].split()[-1]
            if emision.isnumeric(): 
                emision = int(emision)-10
            else:
                credencialValida = False

    if not credencialValida:
        removeFolder(path)
        return {}

    if credencialValida and int(emision) < 2020:
        saveCropCredential(width*0.28, height*0.26, width*0.7, height*0.46, path, "INE-nombre.png", INE)
        nombre = reader2.readtext(path + "INE-nombre.png", detail = 0)[1:]
        nombre = " ".join(nombre).upper()
        
        saveCropCredential(width*0.30, height*0.44, width*0.825, height*0.69, path, "INE-domicilio.png", INE)
        domicilio = reader2.readtext(path + "INE-domicilio.png", detail = 0)[1:]
        domicilio = " ".join(domicilio).upper()

        saveCropCredential(width*0.76, height*0.28, width*0.98, height*0.365, path, "INE-fechaDeNacimiento.png", INE)
        fechaDeNacimiento = reader2.readtext(path + "INE-fechaDeNacimiento.png", detail = 0)
        if len(fechaDeNacimiento) >= 1 and len(fechaDeNacimiento[-1]) >= 8:
            fechaDeNacimiento = fechaDeNacimiento[-1] 
            diaDeNacimiento = fechaDeNacimiento[0:2]
            mesDeNacimiento =  fechaDeNacimiento[3:5] if (fechaDeNacimiento[2] == "/") else fechaDeNacimiento[2:4]
            añoDeNacimiento = fechaDeNacimiento[-4:]
            fechaDeNacimiento = f"{añoDeNacimiento}-{mesDeNacimiento}-{diaDeNacimiento}"
        
        saveCropCredential(width*0.29, height*0.705, width*0.68, height*0.79, path, "INE-curp.png", INE)
        curp = reader2.readtext(path + "INE-curp.png", detail = 0)

        if (len(curp) >= 1):
            for i, element in enumerate(curp): #primer caso checa por el siguiente elemento despues de curp
                if element.upper() == "CURP" and len(curp) >= i+2:
                    curp = curp[i+1].upper().replace(" ", "")
            if type(curp) is list: #segundo caso solo toma el ultimo elemento de la lista
                curp = curp[-1].upper().replace(" ", "")

        try:
            genero = curp[10]
        except:
            saveCropCredential(width*0.91, height*0.33, width*0.97, height*0.445, path, "INE-genero.png", INE)
            genero = reader2.readtext(path + f"INE-genero.png", detail = 0)
            for elemento in genero:
                if "H" in elemento:
                    genero = "H"
                elif "M" in elemento:
                    genero = "M"
            if type(genero) is list:
                genero = ""

        saveCropCredential(width*0.615, height*0.76, width*0.70, height*0.84, path, "INE-municipio.png", INE)
        municipality = reader2.readtext(path + "INE-municipio.png", detail=0)
        try:
            municipality = ' '.join(municipality)
        except:
            municipality = ''

    if credencialValida and int(emision) >= 2020:
        saveCropCredential(width*0.28, height*0.26, width*0.7, height*0.52, path, "INE-nombre.png", INE)
        nombre = reader2.readtext(path + "INE-nombre.png", detail = 0)
        if (len(nombre) >= 1):
            nombre = nombre[1:]
        nombre = [element.upper() for element in nombre if ( element.upper() != "DOMICILIO")]
        nombre = " ".join(nombre)

        saveCropCredential(width*0.30, height*0.49, width*0.825, height*0.705, path, "INE-domicilio.png", INE)
        domicilio = reader2.readtext(path + "INE-domicilio.png", detail = 0)
        if (len(domicilio) >= 1):
            domicilio = domicilio[1:]
        domicilio = " ".join(domicilio)

        saveCropCredential(width*0.30, height*0.74, width*0.67, height*0.855, path, "INE-curp.png", INE)
        curp = reader2.readtext(path + "INE-curp.png", detail = 0)
        if (len(curp) >= 1):
            for i, element in enumerate(curp): #primer caso checa por el siguiente elemento despues de curp
                if element.upper() == "CURP" and len(curp) >= i+2:
                    curp = curp[i+1].upper().replace(" ", "")
            if type(curp) is list: #segundo caso solo toma el ultimo elemento de la lista
                curp = curp[-1].upper().replace(" ", "")

        try:
            genero = curp[10]
        except:
            saveCropCredential(width*0.83, height*0.25, width*0.98, height*0.38, path, "INE-genero.png", INE)
            genero = reader2.readtext(path + f"INE-genero.png", detail = 0)
            for elemento in genero:
                if "H" in elemento:
                    genero = "H"
                elif "M" in elemento:
                    genero = "M"
            if type(genero) is list: genero = ""

        saveCropCredential(width*0.30, height*0.84, width*0.57, height*0.96, path, "INE-fechaDeNacimiento.png", INE)
        fechaDeNacimiento = reader2.readtext(path + "INE-fechaDeNacimiento.png", detail = 0)
        if len(fechaDeNacimiento) >= 1 and len(fechaDeNacimiento[-1]) >= 8:
            fechaDeNacimiento = fechaDeNacimiento[-1] 
            diaDeNacimiento = fechaDeNacimiento[0:2]
            mesDeNacimiento =  fechaDeNacimiento[3:5] if (fechaDeNacimiento[2] == "/") else fechaDeNacimiento[2:4]
            añoDeNacimiento = fechaDeNacimiento[-4:]
            fechaDeNacimiento = f"{añoDeNacimiento}-{mesDeNacimiento}-{diaDeNacimiento}"

        saveCropCredential(width*0.615, height*0.76, width*0.70, height*0.84, path, "INE-municipio.png", INE)
        municipality = reader2.readtext(path + "INE-municipio.png", detail=0)
        try:
            municipality = ' '.join(municipality)
        except:
            municipality = ''
    
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
                        curp
                )
    
    return ine_info.to_JSON()