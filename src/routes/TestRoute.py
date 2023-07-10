from flask import Blueprint, jsonify, request
from src.utils.Security import Security

main = Blueprint('access_blueprint', __name__)

@main.route('/user')
def test_user():
    has_access = Security.verify_user_token(request.headers)

    if has_access:
        try:
            return jsonify({"message": "Puedes acceder al endpoint de usuarios"})
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
@main.route('/admin')
def test_admin():
    has_access = Security.verify_admin_token(request.headers)

    if has_access:
        try:
            return jsonify({"message": "Puedes acceder al endpoint de admin"})
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401
    
@main.route('/influex')
def test_influex():
    has_access = Security.verify_influex_token(request.headers)

    if has_access:
        try:
            return jsonify({"message": "Puedes acceder al endpoint de influex"})
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        response = jsonify({'message': 'Unauthorized'})
        return response, 401