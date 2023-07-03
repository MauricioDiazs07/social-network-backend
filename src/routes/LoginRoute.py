from flask import Blueprint, jsonify, request
from models.entities.User import User
from models.UserModel import UsersModel
from utils.Security import Security

main = Blueprint('login_blueprint', __name__)

@main.route('/', methods = ['POST'])
def login():
    email = request.json['email']
    usr_password = request.json['password']
    user = User(None, email, usr_password, None, None, None, None, None, None)
    authenticated_user = UsersModel.login_user(user)
    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token})
    else:
        response = jsonify({'message': 'No registrado'})
        return response, 401