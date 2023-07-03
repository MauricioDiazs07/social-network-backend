from flask import Blueprint, jsonify, request
from models.entities.User import User
from models.UserModel import UsersModel

main = Blueprint('signup_blueprint', __name__)

@main.route('/', methods = ['POST'])
def sign_up():
    try:
        name = request.json['full_name']
        email = request.json['email']
        usr_password = request.json['password']
        gender = request.json['gender']
        state = request.json['state']
        municipality = request.json['municipality']
        birthday = request.json['birthday']
        user = User(name, email, usr_password, gender, state, municipality, birthday, 0, 'user') # Solo para crear usuarios
        affected_row = UsersModel.add_user(user)

        if affected_row == 1:
            return jsonify(user.email)
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500