from flask import Blueprint, jsonify, request
from src.utils.ModeloINE import ModeloIne
import base64

main = Blueprint('ai_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
RESOURCES_PATH = 'src/resources/img/'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/ine', methods = ['POST'])
def createPost():
    if 'INE' not in request.json:
        return jsonify(
            {'Error': 'No INE key in request.files'}
        )
        
    file = request.json['INE']
    data = file['data']
    path = RESOURCES_PATH + 'INE.png'

    # data_as_dictionary = json.loads(data)
    img = base64.b64decode(data)

    # imgdata = base64.b64decode(data)
    with open(path, 'wb') as f:
            f.write(img)

    # img.save(path)

    if file['path'] == '':
        return jsonify(
            {'Error': 'No selected file'}
        )

    if file and allowed_file(file['path']):
        datos = ModeloIne(path, RESOURCES_PATH)

        if not datos:
            return jsonify({'ok': False})

        return jsonify(
            {
                'name': datos["nombre"],
                'gender': datos["genero"],
                'state': datos["estado"],
                'municipality': 'Coyoacan',
                'address': datos["domicilio"],
                'birthday': datos["fechaDeNacimiento"],
                'curp': datos["curp"]
            }
        )
        
    else:
        return jsonify(
            {'Error': 'File type not accepted, please try again'}
        )