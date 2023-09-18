import uuid
import hashlib
from flask import Blueprint, jsonify, request
from src.models.entities.auth import Login, SignUp
from src.models.AuthModel import AuthModel
from src.utils.Security import Security
from src.models.entities.multimedia import Multimedia
from src.models.MultimediaModel import MultimediaModel
from src.utils.AmazonS3 import upload_file_to_s3  
from decouple import config
from src.utils._support_functions import \
                                    format_date_to_DB, \
                                    getGender, \
                                    getState, \
                                    getMunicipality
          
main = Blueprint('auth_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/login', methods = ['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    login = Login(email, password)

    authenticated_user = AuthModel.login(login)
    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({
            'profile_id': authenticated_user.id,
            'email': authenticated_user.email,
            'role_id': authenticated_user.role_id,
            'token': encoded_token
            })
    else:
        response = jsonify({'message': 'No registrado'})
        return response, 401
    
@main.route('/signup', methods = ['POST'])
def sign_up():
    try:
        phone = request.form['phone']
        password = request.form['password']
        name = request.form['name']
        gender = request.form['gender']
        state_id = request.form['state']
        municipality_id = request.form['municipality']
        address = request.form['address']
        birthday = request.form['birthday']
        curp = request.form['curp']
        email = request.form['email']
        profile_id = hashlib.shake_256(phone.encode('utf-8')).hexdigest(16)
        
        file = request.files['identification_photo']
        if file and allowed_file(file.filename):
            new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
            upload_file_to_s3(file,new_name)
            identification_photo = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
            multimedia = Multimedia(profile_id,profile_id, 'IDENTIFICATION', identification_photo, file.filename.rsplit('.',1)[1].lower())
            MultimediaModel.create_multimedia(multimedia)
        
        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
                upload_file_to_s3(file,new_name)
                profile_photo = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
                multimedia = Multimedia(profile_id, profile_id, 'PROFILE', profile_photo, file.filename.rsplit('.',1)[1].lower())
                MultimediaModel.create_multimedia(multimedia)
        else:
            profile_photo = None
        
        # process information for database
        birthday = format_date_to_DB(birthday)
        gender = getGender(gender)
        state = getState(state_id)
        municipality = getMunicipality(state_id, municipality_id)
        
        signup = SignUp(profile_id,email,password,name,gender,state,municipality,address,birthday,curp,identification_photo,phone,profile_photo)
        affected_row = AuthModel.signup(signup)
        if affected_row == 1:
            return jsonify({
                'message': 'OK',
                'user': email
            })
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        MultimediaModel.delete_multimedia(profile_id)
        if profile_id != None:
            MultimediaModel.delete_multimedia(profile_id)
        return jsonify({'message': str(ex)}), 500