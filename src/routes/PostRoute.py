from flask import Blueprint, jsonify, request
from src.utils.helpers import upload_file_to_s3

main = Blueprint('post_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods = ['POST'])
def createPost():
    if 'user_file' not in request.files:
        return jsonify(
            {'Error': 'No user_file key in request.files'}
        )
        
    file = request.files['user_file']

    if file.filename == '':
        return jsonify(
            {'Error': 'No selected file'}
        )

    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file) 
        
        if output:
            return jsonify(
            {'Message': 'Success upload'}
        )

        else:
            return jsonify(
            {'Error': 'Unable to upload, try again'}
        )
        
    else:
        return jsonify(
            {'Error': 'File type not accepted,please try again'}
        )
    

@main.route('/test', methods = ['POST'])
def createTest():

    print(request.files)
    print(request.form['description'])

    if 'files' not in request.files and request.form['description'] == '':
        return jsonify(
            {'Error': 'Data not found'}
        )

    
    return jsonify(
            {'Message': 'Test'}
        )