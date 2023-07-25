from flask import Blueprint, jsonify, request
from src.models.entities.auth import Login, SignUp
from src.models.AuthModel import AuthModel
from src.utils.Security import Security
from src.utils._support_functions import \
                                    format_date_to_DB, \
                                    getGender, \
                                    getState, \
                                    getMunicipality
import hashlib

main = Blueprint('auth_blueprint', __name__)

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
        email = request.json['email']
        password = request.json['password']
        name = request.json['name']
        gender = request.json['gender']
        state_id = request.json['state']
        municipality_id = request.json['municipality']
        address = request.json['address']
        birthday = request.json['birthday']
        curp = request.json['curp']
        identification_photo = request.json['identification_photo']
        phone = request.json['phone']
        profile_id = hashlib.shake_256(email.encode('utf-8')).hexdigest(16)

        # process information for database
        birthday = format_date_to_DB(birthday)
        gender = getGender(gender)
        state = getState(state_id)
        municipality = getMunicipality(state_id, municipality_id)

        signup = SignUp(profile_id,email,password,name,gender,state,municipality,address,birthday,curp,identification_photo,phone)

        affected_row = AuthModel.signup(signup)

        if affected_row == 1:
            return jsonify(signup.email)
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500