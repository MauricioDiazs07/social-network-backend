import uuid
import bcrypt
import hashlib
from flask import Blueprint, jsonify, request
from src.models.entities.profile.MasterProfile import MasterProfile
from src.models.entities.profile.AdminProfile import AdminProfile
from src.models.AdminModel import AdminModel

main = Blueprint('admin_blueprint', __name__)

def hash_password(password):
    # Generar un salt aleatorio y hashear la contraseña con el salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

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
        affected_row = AdminModel.create_master(master)
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
        name = request.json['name']
        phone_number = request.json['phone_number']
        area_code = request.json['area_code']
        pre_password = request.json['password']
        password = hash_password(pre_password)
        master_id = request.json['master_id']

        id = hashlib.shake_256(phone_number.encode('utf-8')).hexdigest(16)

        master = AdminProfile(id,name,phone_number,area_code,password,master_id)
        affected_row = AdminModel.create_admin(master)
        if affected_row == 1:
            return jsonify({
                'name': name,
                'phone_number': phone_number,
                'id': id
            })
        else:
            response = jsonify({'message': 'Error al registrarse'})
            return response, 500
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/admin/list', methods = ['POST'])
def list_admins():
    try:
        master_id = request.json['master_id']
        admins = AdminModel.list_admins(master_id)
        return admins
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/admin/', methods = ['DELETE'])
def delete_admin():
    try:
        admin_id = request.json['admin_id']
        AdminModel.delete_admin(admin_id)
        return jsonify({
            'message': 'ok'
        })
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500