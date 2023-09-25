from flask import Blueprint, jsonify, request
from src.models.UserModel import UsersModel
from src.models.entities.multimedia import Multimedia
from src.models.MultimediaModel import MultimediaModel
import uuid
from decouple import config
from src.utils.AmazonS3 import \
                            upload_file_to_s3, \
                            delete_file_from_s3

main = Blueprint('user_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/update',  methods = ['PATCH'])
def update_users_data():
    try:
        profile_id = request.form['profile_id']
        email = request.form['email']
        phone_number = request.form['phone_number']

        print('profile_id', profile_id)
        print('email', email)
        print('phone_number', phone_number)

        if 'profile_photo' in request.files:
            file = request.files['profile_photo']
            if file and allowed_file(file.filename):
                multimedia = MultimediaModel.get_multimedia(profile_id, 'PROFILE')
                if len(multimedia) != 0:
                    for archive in multimedia:
                        file_name = archive['archive_url'].split("/")[-1]
                        delete_file_from_s3(file_name)
                    MultimediaModel.delete_multimedia(profile_id, 'PROFILE')
                new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
                upload_file_to_s3(file,new_name)
                profile_photo = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
                multimedia = Multimedia(profile_id,profile_id, 'PROFILE', profile_photo, profile_photo.rsplit('.',1)[1].lower())
                MultimediaModel.create_multimedia(multimedia)
                UsersModel.update_data_photo_user(profile_id,email,phone_number,profile_photo)
                return jsonify({
                    'message': 'OK',
                    'profile_photo': profile_photo
                })
        else:
            UsersModel.update_user(profile_id,email,phone_number)
            return jsonify({
                'message': 'OK'
            })
    except Exception as ex:
        print(ex)
        return jsonify({'message': str(ex)}), 500


@main.route('/<profile_id>', )
def get_user_data(profile_id):
    try:
        user = UsersModel.get_user_data(profile_id)
        return jsonify(user)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
   

@main.route('/<profile_id>', methods = ['DELETE'])
def delete_user_data(profile_id):
    try:
        multimedia = MultimediaModel.get_all_multimedia_from_profile(profile_id)
        print(multimedia)
        for archive in multimedia:
            file = archive['archive_url'].split("/")[-1]
            delete_file_from_s3(file)
        MultimediaModel.delete_all_multimedia(profile_id)
        UsersModel.delete_user_data(profile_id)
        return {
            'message': 'OK'
        }
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500




@main.route('/phone/<phone>', methods = ['DELETE'])
def delete_user_data_by_phone(phone):
    try:
        profile_id = UsersModel.get_id_by_phone(phone)
        print(profile_id)
        multimedia = MultimediaModel.get_all_multimedia_from_profile(profile_id)
        print(multimedia)
        for archive in multimedia:
            file = archive['archive_url'].split("/")[-1]
            delete_file_from_s3(file)
        MultimediaModel.delete_all_multimedia(profile_id)
        UsersModel.delete_user_data(profile_id)
        return {
            'message': 'OK'
        }
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500