from flask import Blueprint, jsonify, request
from models.UserModel import UsersModel
from utils.Security import Security

main = Blueprint('user_blueprint', __name__)

@main.route('/')
def get_users():

    has_access = Security.verify_token(request.headers)

    if has_access:
        try:
            users = UsersModel.get_users()
            return jsonify(users)
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401

@main.route('/test')
def test():
    try:
        result = UsersModel.test()
        return jsonify({'message': result})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500