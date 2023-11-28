import uuid
import bcrypt
import hashlib
from flask import Blueprint, jsonify, request
from src.models.MasterModel import MasterModel
from src.models.entities.auth import Login, SignUp
from src.models.entities.profile.MasterProfile import MasterProfile
from src.models.entities.profile.AdminProfile import AdminProfile
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

def hash_password(password):
    # Generar un salt aleatorio y hashear la contraseña con el salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hash_password):
    # Verifica si la contraseña en texto plano coincide con la contraseña encriptada
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

@main.route('/verified', methods = ['POST'])
def verified_accound():
    profile_id = request.json['profile_id']
    result = AuthModel.verified_accound(profile_id)
    if result > 0:
        return jsonify({
            'message': 'Cuenta verificada'
        })
    else:
        response = jsonify({
            'message': 'Error al verificar'
        })
        return response, 500

@main.route('/login', methods = ['POST'])
def login():
    phone = request.json['phoneNumber']
    pre_password = request.json['password']
    password = hash_password(pre_password)
    login = Login(phone, password)
    authenticated_user = AuthModel.login(login)
    if authenticated_user != None and verify_password(pre_password, authenticated_user.password):
        print(authenticated_user.role_id)
        if authenticated_user.role_id[0] == 2:
            authenticated_user = MasterModel.get_login_info(authenticated_user.id)
            authenticated_user.role_id = [2]
            print(authenticated_user)
        encoded_token = Security.generate_token(authenticated_user)
        verified_phone = None
        if authenticated_user.role_id[0] == 1:
            verified_phone = AuthModel.check_verified(authenticated_user.id)
        return jsonify({
            'profile_id': authenticated_user.id,
            'email': authenticated_user.email,
            'role_id': authenticated_user.role_id,
            'verified_phone': verified_phone,
            'token': encoded_token
            })
    else:
        response = jsonify({'message': 'No registrado'})
        return response, 401
    
    
@main.route('/signup', methods = ['POST'])
def sign_up():
    try:
        phone = request.form['phone']
        area_code = request.form['area_code']
        pre_password = request.form['password']
        password = hash_password(pre_password)
        name = request.form['name']
        gender = request.form['gender']
        state_id = request.form['state']
        municipality_id = request.form['municipality']
        address = request.form['address']
        birthday = request.form['birthday']
        curp = request.form['curp']
        email = request.form['email']
        section = request.form['section']
        if email == '':
            email = None
        profile_id = hashlib.shake_256(phone.encode('utf-8')).hexdigest(16)
        # process information for database
        birthday = format_date_to_DB(birthday)
        gender = getGender(gender)
        state = getState(state_id)
        municipality = getMunicipality(state_id, municipality_id)
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
        signup = SignUp(profile_id,email,password,name,gender,state,municipality,address,birthday,curp,identification_photo,phone,profile_photo,section,area_code)
        affected_row = AuthModel.signup(signup)
        if affected_row == 1:
            return jsonify({
                'message': 'OK',
                'user': email,
                'profile_id': profile_id
            })
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        MultimediaModel.delete_multimedia(profile_id,'IDENTIFICATION')
        if profile_id != None:
            MultimediaModel.delete_multimedia(profile_id,'PROFILE')
        return jsonify({'message': str(ex)}), 500
    

@main.route('/master', methods = ['POST'])
def create_master():
    try:
        phone_number = request.json['phone_number']
        area_code = request.json['area_code']
        pre_password = request.json['password']
        password = hash_password(pre_password)
        gender = request.json['gender']
        name = request.json['name']
        description = request.json['description']
        email = request.json['email']

        id = hashlib.shake_256(phone_number.encode('utf-8')).hexdigest(16)

        master = MasterProfile(id,phone_number, area_code,password,gender,name,description,email)
        affected_row = AuthModel.create_master(master)
        if affected_row == 1:
            return jsonify({
                'phone_number': phone_number,
                'id': id
            })
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/admin', methods = ['POST'])
def create_admin():
    try:
        phone_number = request.json['phone_number']
        area_code = request.json['area_code']
        pre_password = request.json['password']
        password = hash_password(pre_password)
        master_id = request.json['master_id']

        id = hashlib.shake_256(phone_number.encode('utf-8')).hexdigest(16)

        master = AdminProfile(id,phone_number,area_code,password,master_id)
        affected_row = AuthModel.create_admin(master)
        if affected_row == 1:
            return jsonify({
                'phone_number': phone_number,
                'id': id
            })
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500