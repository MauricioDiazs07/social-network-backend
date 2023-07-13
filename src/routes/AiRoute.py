from flask import Blueprint, jsonify, request

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
        return jsonify(
            {
                'name': 'Jonathan Yair Vazquez',
                'gender': 'M',
                'state': 'CDMX',
                'municipality': 'Coyoacan',
                'colony': 'Churubusco',
                'street': 'Aguayo ',
                'int_number': '12',
                'ext_number': '0',
                'birthday': '1998-12-14',
                'curp': 'VAUJ981214HMCZRN00',
            }
        )
        
    else:
        return jsonify(
            {'Error': 'File type not accepted, please try again'}
        )