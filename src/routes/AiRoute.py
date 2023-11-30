from flask import Blueprint, jsonify, request
from src.utils.ModeloINE import ModeloIne
import base64
import os
import uuid
import os
import proto
import json
from google.cloud import vision
import re
from src.models.entities.states.States import STATES, MUNICIPALITIES

main = Blueprint('ai_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
RESOURCES_PATH = 'src/resources/img/'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='vision_key.json'


def replaceChars(text):
    text = text.replace("Á", "A")
    text = text.replace("É", "E")
    text = text.replace("Í", "I")
    text = text.replace("Ó", "O")
    text = text.replace("Ú", "U")

    return text


def allowed_file(filename: str) -> bool:
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkIfPathExists(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)

@main.route('/ine', methods=['POST'])
def createPost():
    # if ine not in request, throws an error
    if 'INE' not in request.json:
        return jsonify(
            {'Error': 'No INE key in request.files'}
        )
        
    file = request.json['INE']
    data = file['data']

    # resources img path
    checkIfPathExists(RESOURCES_PATH)

    # unique ine path generation
    uuid_ = uuid.uuid4()
    path = RESOURCES_PATH + f'ine_{uuid_}/'
    file_name = f'INE_{uuid_}.png'
    checkIfPathExists(path)

    img = base64.b64decode(data)

    # save image
    with open(path + file_name, 'wb') as f:
            f.write(img)

    if file['path'] == '':
        return jsonify(
            {'Error': 'No selected file'}
        )

    if file and allowed_file(file['path']):
        datos = ModeloIne(path + file_name, path)
        if not datos:
            return jsonify({'ok': False})
        return jsonify(datos)
        
    else:
        return jsonify(
            {'Error': 'File type not accepted, please try again'}
        )
    

@main.route('/ine2', methods=['POST'])
def googleOCR():
    vision_client = vision.ImageAnnotatorClient()
    curp = ''
    cumple = ''
    cp = 0

    content = request.files['ine'].read()
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = proto.Message.to_json(response)
    mydict = json.loads(texts)

    clean = []
    patron = re.compile('[0-9]{2}\/[0-9]{2}\/[0-9]{4}')
    patron2 = re.compile('[A-Z]{4}[0-9]{6}[A-Z]{6}[0-9]{2}')

    data_ine = mydict['textAnnotations'][0]['description'].split("\n")
    for data in data_ine:
        space = data.split(" ")
        if len(space) != 0:
            for i in space:
                clean.append(i)
                if patron.search(i):
                    cumple = i
                if patron2.search(i):
                    curp = i
                
        else:
            clean.append(space)

    clean = [replaceChars(x) for x in clean]

    out = {}
    for j in clean[clean.index('DOMICILIO') + 1:clean.index('CLAVE')]:
        if j.isdigit():
            cp = clean.index(j)

    try:
        clean.index('EMISION')
        out['section'] = clean[clean.index('SECCION') + 1]
        out['municipality'] = clean[clean.index('MUNICIPIO') + 1]
        out['state'] = clean[clean.index('ESTADO') + 1]
    except:
        patron3 = re.compile('^[0-9]{4}$')
        todo = clean[clean.index('SECCION'):]
        me = " ".join(clean[cp + 1:clean.index('CLAVE')]).split(',')
        if (len(me) == 1):
            me = " ".join(clean[cp + 1:clean.index('CLAVE')]).split('.')
        
        index = (list(STATES.values()).index(".".join(me[1:]).strip().replace(".","")))
        out['state'] = list(STATES.keys())[index]
        out['municipality'] = list(MUNICIPALITIES[out['state']].keys())[list(MUNICIPALITIES[out['state']].values()).index(me[0])]
        
        for k in todo:
            if patron3.search(k):
                out['section'] = k
                break

    out['name'] = " ".join(clean[clean.index('NOMBRE') + 1:clean.index('DOMICILIO')])
    out['curp'] = curp
    out['gender'] = curp[10] if curp != '' else ''
    out['birthday'] = cumple
    out['address'] = " ".join(clean[clean.index('DOMICILIO') + 1: cp + 1])
    
    return jsonify(out)