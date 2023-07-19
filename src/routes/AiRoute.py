from flask import Blueprint, jsonify, request
from src.utils.modeloINE import ModeloINE

main = Blueprint('ai_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/ine', methods = ['POST'])
def createPost():
    if 'INE' not in request.files:
        return jsonify(
            {'Error': 'No INE key in request.files'}
        )
        
    file = request.files['INE']

    if file.filename == '':
        return jsonify(
            {'Error': 'No selected file'}
        )

    if file and allowed_file(file.filename):
        datos = ModeloINE(file.filename)
        return jsonify(
            {
                'name': datos["nombre"],
                'gender': datos["genero"],
                'state': datos["estado"],
                'municipality': 'Coyoacan',
                'colony': 'Churubusco',
                'street': 'Aguayo ',
                'int_number': '12',
                'ext_number': '0',
                'birthday': datos["fechaDeNacimiento"],
                'curp': datos["curp"],
                # datos["domicilio"] no es usado
            }
        )
        
    else:
        return jsonify(
            {'Error': 'File type not accepted, please try again'}
        )