from flask import Blueprint, jsonify, request
from models.entities.auth import Login, SignUp
from models.AuthModel import AuthModel
from utils.Security import Security

main = Blueprint('auth_blueprint', __name__)

@main.route('/login', methods = ['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    login = Login(email, password)

    authenticated_user = AuthModel.login(login)
    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token})
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
        state = request.json['state']
        municipality = request.json['municipality']
        colony = request.json['colony']
        street = request.json['street']
        int_number = request.json['int_number']
        ext_number = request.json['ext_number']
        birthday = request.json['birthday']
        curp = request.json['curp']
        identification_photo = request.json['identification_photo']
        signup = SignUp(email,password,name,gender,state,municipality,colony,street,int_number,ext_number,birthday,curp,identification_photo)

        affected_row = AuthModel.signup(signup)

        if affected_row == 1:
            return jsonify(signup.email)
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500