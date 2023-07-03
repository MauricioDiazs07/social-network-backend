from flask import Blueprint, jsonify, request
from models.UserModel import UsersModel
from utils.Security import Security
from models.entities.User import User

main = Blueprint('user_blueprint', __name__)

@main.route('/')
def get_users():

    has_access = Security.verify_influex_token(request.headers)

    if has_access:
        try:
            users = UsersModel.get_users()
            return jsonify(users)
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401


@main.route('/self', methods = ['POST'])
def get_user():
    try:
        email = request.json['email']
        user = User(None, email, None, None, None, None, None, None, None)
        user = UsersModel.get_user(user)
        return jsonify(user)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
   

