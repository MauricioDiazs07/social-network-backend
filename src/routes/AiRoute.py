from flask import Blueprint, jsonify, request
from src.utils.ModeloINE import ModeloIne
import base64
import os
import uuid

main = Blueprint('ai_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
RESOURCES_PATH = 'src/resources/img/'

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