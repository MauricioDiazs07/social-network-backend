import pickle
import os
from PIL import Image
import re

MODEL_PATH = 'src/resources/models/model_read.pkl'

with open(MODEL_PATH, 'rb') as f:
        reader2 = pickle.load(f)

def validCredential(INE, width, height, path):
    cabeceraRecorte = INE.crop((width*0.0, height*0.0, width*1.0, height*0.5))
    cabeceraRecorte.save(path + "INE-cabecera.png")

    credencialValida = False
    result = reader2.readtext(path + "INE-cabecera.png", detail = 0)
    for element in result:
        if "INSTITUTO" in element or "NACIONAL" in element or "ELECTORAL" in element:
            return True
        
    return False
            
def ModeloIne(filename, path):
    INE = Image.open(filename)
    width, height = INE.width, INE.height

    for i in range(4):
        credencialValida = validCredential(INE, width, height, path)
        if credencialValida:
            break
        INE = INE.rotate(90)
    
    emision = 0
    
    if credencialValida:
        otrosRecorte = INE.crop((width*0.30, height*0.755, width*0.88, height*0.945))
        otrosRecorte.save(path + "INE-otros.png")
        result = reader2.readtext(path + "INE-otros.png", detail = 0)
        emision = result[-1].split()[-1]
        if emision.isnumeric(): 
            emision = int(emision)-10
        else: # podria estar ligeramente rotada
            INE = INE.rotate(-3)
            otrosRecorte = INE.crop((width*0.30, height*0.755, width*0.88, height*0.945))
            otrosRecorte.save(path + "INE-otros.png")
            result = reader2.readtext(path + "INE-otros.png", detail = 0)
            ''.join(result)
            emision = result[-1].split()[-1]
            if emision.isnumeric(): 
                emision = int(emision)-10
            else:
                credencialValida = False
            
    if credencialValida and int(emision) < 2020:
        INE.crop((width*0.075, height*0.36, width*0.31, height*0.85)).save(path + "INE-foto.png")
        
        INE.crop((width*0.28, height*0.26, width*0.7, height*0.46)).save(path + "INE-nombre.png")
        nombre = reader2.readtext(path + "INE-nombre.png", detail = 0)[1:]
        nombre = " ".join(nombre).upper()
        
        INE.crop((width*0.30, height*0.44, width*0.825, height*0.645)).save(path + "INE-domicilio.png")
        domicilio = reader2.readtext(path + "INE-domicilio.png", detail = 0)[1:]
        domicilio = " ".join(domicilio).upper()

        INE.crop((width*0.91, height*0.335, width*0.97, height*0.445)).convert('L').save(path + "INE-genero.png") 
        genero = reader2.readtext(path + f"INE-genero.png", detail = 0)
        for elemento in genero:
            if "H" in elemento:
                genero = "H"
            elif "M" in elemento:
                genero = "M"
        if type(genero) is list: genero = ""

        INE.crop((width*0.76, height*0.28, width*0.98, height*0.365)).save(path + "INE-fechaDeNacimiento.png")
        fechaDeNacimiento = reader2.readtext(path + "INE-fechaDeNacimiento.png", detail = 0)
        if len(fechaDeNacimiento) >= 1 and len(fechaDeNacimiento[-1]) >= 8:
            fechaDeNacimiento = fechaDeNacimiento[-1] 
            diaDeNacimiento = fechaDeNacimiento[0:2]
            mesDeNacimiento =  fechaDeNacimiento[3:5] if (fechaDeNacimiento[2] == "/") else fechaDeNacimiento[2:4]
            añoDeNacimiento = fechaDeNacimiento[-4:]
            fechaDeNacimiento = f"{añoDeNacimiento}-{mesDeNacimiento}-{diaDeNacimiento}"
        
        INE.crop((width*0.29, height*0.695, width*0.68, height*0.78)).save(path + "INE-curp.png")
        curp = reader2.readtext(path + "INE-curp.png", detail = 0)
        if (len(curp) >= 1):
            for i, element in enumerate(curp): #primer caso checa por el siguiente elemento despues de curp
                if element.upper() == "CURP" and len(curp) >= i+2:
                    curp = curp[i+1].upper().replace(" ", "")
            if type(curp) is list: #segundo caso solo toma el ultimo elemento de la lista
                curp = curp[-1].upper().replace(" ", "")

        INE.crop((width*0.49, height*0.635, width*0.82, height*0.725)).save(path + "INE-claveDeElector.png")
        INE.crop((width*0.855, height*0.685, width*0.98, height*0.805)).save(path + "INE-añoDeRegistro.png")
        INE.crop((width*0.39, height*0.76, width*0.50, height*0.84)).save(path + "INE-estado.png")
        INE.crop((width*0.615, height*0.76, width*0.70, height*0.84)).save(path + "INE-municipio.png")
        INE.crop((width*0.78, height*0.760, width*0.87, height*0.84)).save(path + "INE-seccion.png")
        INE.crop((width*0.43, height*0.835, width*0.52, height*0.93)).save(path + "INE-localidad.png")
        INE.crop((width*0.61, height*0.83, width*0.705, height*0.93)).save(path + "INE-emision.png")
        INE.crop((width*0.78, height*0.825, width*0.88, height*0.93)).save(path + "INE-vigencia.png")

    if credencialValida and int(emision) >= 2020:
        INE.crop((width*0.075, height*0.36, width*0.31, height*0.85)).save(path + "INE-foto.png")
        
        INE.crop((width*0.28, height*0.26, width*0.7, height*0.52)).save(path + "INE-nombre.png")
        nombre = reader2.readtext(path + "INE-nombre.png", detail = 0)
        if (len(nombre) >= 1):
            nombre = nombre[1:]
        nombre = [element.upper() for element in nombre if ( element.upper() != "DOMICILIO")]
        nombre = " ".join(nombre)

        INE.crop((width*0.30, height*0.49, width*0.825, height*0.705)).save(path + "INE-domicilio.png")
        domicilio = reader2.readtext(path + "INE-domicilio.png", detail = 0)
        if (len(domicilio) >= 1):
            domicilio = domicilio[1:]
        domicilio = " ".join(domicilio)

        INE.crop((width*0.83, height*0.25, width*0.98, height*0.38)).save(path + "INE-genero.png")
        genero = reader2.readtext(path + f"INE-genero.png", detail = 0)
        for elemento in genero:
            if "H" in elemento:
                genero = "H"
            elif "M" in elemento:
                genero = "M"
        if type(genero) is list: genero = ""

        INE.crop((width*0.30, height*0.74, width*0.67, height*0.855)).save(path + "INE-curp.png")
        curp = reader2.readtext(path + "INE-curp.png", detail = 0)
        if (len(curp) >= 1):
            for i, element in enumerate(curp): #primer caso checa por el siguiente elemento despues de curp
                if element.upper() == "CURP" and len(curp) >= i+2:
                    curp = curp[i+1].upper().replace(" ", "")
            if type(curp) is list: #segundo caso solo toma el ultimo elemento de la lista
                curp = curp[-1].upper().replace(" ", "")

        INE.crop((width*0.30, height*0.84, width*0.57, height*0.96)).save(path + "INE-fechaDeNacimiento.png")
        fechaDeNacimiento = reader2.readtext(path + "INE-fechaDeNacimiento.png", detail = 0)
        if len(fechaDeNacimiento) >= 1 and len(fechaDeNacimiento[-1]) >= 8:
            fechaDeNacimiento = fechaDeNacimiento[-1] 
            diaDeNacimiento = fechaDeNacimiento[0:2]
            mesDeNacimiento =  fechaDeNacimiento[3:5] if (fechaDeNacimiento[2] == "/") else fechaDeNacimiento[2:4]
            añoDeNacimiento = fechaDeNacimiento[-4:]
            fechaDeNacimiento = f"{añoDeNacimiento}-{mesDeNacimiento}-{diaDeNacimiento}"

        INE.crop((width*0.49, height*0.635, width*0.82, height*0.725)).save(path + "INE-claveDeElector.png")
        INE.crop((width*0.855, height*0.685, width*0.98, height*0.805)).save(path + "INE-añoDeRegistro.png")
        INE.crop((width*0.39, height*0.76, width*0.50, height*0.84)).save(path + "INE-estado.png")
        INE.crop((width*0.615, height*0.76, width*0.70, height*0.84)).save(path + "INE-municipio.png")
        INE.crop((width*0.78, height*0.760, width*0.87, height*0.84)).save(path + "INE-seccion.png")
        INE.crop((width*0.43, height*0.835, width*0.52, height*0.93)).save(path + "INE-localidad.png")
        INE.crop((width*0.61, height*0.83, width*0.705, height*0.93)).save(path + "INE-emision.png")
        INE.crop((width*0.78, height*0.825, width*0.88, height*0.93)).save(path + "INE-vigencia.png")
    
    INE.crop((width*0.30, height*0.76, width*0.50, height*0.84)).save(path + f"INE-estado.png")
    estado = reader2.readtext(path + f"INE-estado.png", detail = 0)
    if type(estado) is list:
        if len(estado) == 0:
            estado = ""
        else:
            estado = estado[-1]
    if estado == "01": estado = "AGUASCALIENTES"
    elif estado == "02": estado = "BAJA CALIFORNIA"
    elif estado == "03": estado = "BAJA CALIFORNIA SUR"
    elif estado == "04": estado = "CAMPECHE"
    elif estado == "05": estado = "COAHUILA"
    elif estado == "06": estado = "COLIMA"
    elif estado == "07": estado = "CHIAPAS"
    elif estado == "08": estado = "CHIHUAHUA"
    elif estado == "09": estado = "CIUDAD DE MEXICO"
    elif estado == "10": estado = "DURANGO"
    elif estado == "11": estado = "GUANAJUATO"
    elif estado == "12": estado = "GUERRERO"
    elif estado == "13": estado = "HIDALGO"
    elif estado == "14": estado = "JALISCO"
    elif estado == "15": estado = "MEXICO"
    elif estado == "16": estado = "MICHOACAN"
    elif estado == "17": estado = "MORELOS"
    elif estado == "18": estado = "NAYARIT"
    elif estado == "19": estado = "NUEVO LEON"
    elif estado == "20": estado = "OAXACA"
    elif estado == "21": estado = "PUEBLA"
    elif estado == "22": estado = "QUERETARO"
    elif estado == "23": estado = "QUINTANA ROO"
    elif estado == "24": estado = "SAN LUIS POTOSI"
    elif estado == "25": estado = "SINALOA"
    elif estado == "26": estado = "SONORA"
    elif estado == "27": estado = "TABASCO"
    elif estado == "28": estado = "TAMAULIPAS"
    elif estado == "29": estado = "TLAXCALA"
    elif estado == "30": estado = "VERACRUZ"
    elif estado == "31": estado = "YUCATAN"
    elif estado == "32": estado = "ZACATECAS"
    # else: estado = domicilio.split()[-1] if type(domicilio) is str else "error"
    if estado == "CDMX" or estado.replace(".", "") == "DF": estado = "CIUDAD DE MEXICO"
    if estado not in "AGUASCALIENTES BAJA CALIFORNIA SUR CAMPECHE COAHUILA CIUDAD DE MEXICO \
        DURANGO GUNAJUATO GUERRERO HIDALGO JALISCO MEXICO MICHOACAN MORELOS NAYARIT\
        NUEVO LEON OAXACA PUEBLA QUERETARO QUINTANA ROO SAN LUIS POTOSI SINALOA SONORA \
        TABASCO TAMAULIPAS TLAXCALA VERACRUZ YUCATAN ZACATECAS":
        estado = ""

    try:
        os.remove("INE-cabecera.png")
        os.remove("INE-foto.png")
        os.remove("INE-nombre.png")
        os.remove("INE-domicilio.png")
        os.remove("INE-fechaDeNacimiento.png")
        os.remove("INE-genero.png")
        os.remove("INE-curp.png")
        os.remove("INE-claveDeElector.png")
        os.remove("INE-añoDeRegistro.png")
        os.remove("INE-estado.png")
        os.remove("INE-municipio.png")
        os.remove("INE-seccion.png")
        os.remove("INE-localidad.png")
        os.remove("INE-emision.png")
        os.remove("INE-vigencia.png")
        os.remove("INE-otros.png")
    except:
        pass

    if not credencialValida:
        return {}

    datos = {
            "nombre": nombre,
            "domicilio": domicilio,
            "genero": curp[10],
            "fechaDeNacimiento": fechaDeNacimiento,
            "curp": curp,
            "estado": estado
            }
    
    return datos