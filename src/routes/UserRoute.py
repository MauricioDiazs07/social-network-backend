from flask import Blueprint, jsonify, request
from src.models.UserModel import UsersModel
from src.utils.Security import Security
from src.models.entities.user.User import User

main = Blueprint('user_blueprint', __name__)

@main.route('/update',  methods = ['PATCH'])
def update_users_data():
    try:
        profile_id = request.json['profile_id']
        email = request.json['email']
        phone_number = request.json['phone_number']
        
        users = UsersModel.get_users()
        return jsonify(users)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
   


@main.route('/<profile_id>', )
def get_user_data(profile_id):
    try:
        user = UsersModel.get_user_data(profile_id)
        return jsonify(user)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
   

