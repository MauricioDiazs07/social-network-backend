from flask import Blueprint, jsonify, request
from src.utils.AmazonS3 import upload_file_to_s3
from src.models.ShareModel import ShareModel
from src.models.entities.share import Share, Multimedia
import uuid
from decouple import config

main = Blueprint('share_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/upload', methods = ['POST'])
def create_share():

    try:
        if len(request.files) == 0 and request.form['description'] == '':
            return jsonify(
                {'Error': 'Data not found'}
            )

        profile_id = request.form['profile_id']
        description = request.form['description']
        share_type = request.form['share_type']
        share = Share(None, profile_id, share_type, description)
        share_id = ShareModel.create_share(share)
        print(request.files)
        if len(request.files) > 0:
            for fileitem in request.files:
                file = request.files[fileitem]
                if file and allowed_file(file.filename):
                    new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
                    upload_file_to_s3(file,new_name)
                    url = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
                    multimedia = Multimedia(share_id, share_type, url, file.filename.rsplit('.',1)[1].lower())
                    ShareModel.create_multimedia(multimedia)

        return jsonify({'message': share_id})
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/get/<int:share_id>/', methods = ['GET'])
def get_share(share_id):
    try:
        shares = ShareModel.get_share(share_id)
        multimedia = ShareModel.get_multimedia(share_id)
        return jsonify({
            "share": shares,
            "multimedia": multimedia
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/list', methods = ['GET'])
def list_share():
    try:
        shares_all = []
        shares = ShareModel.get_all()
        for share in shares:
            multimedia = ShareModel.get_multimedia(share["share_id"])
            shares_all.append({
                "share": share,
                "multimedia": multimedia
            })
        return shares_all
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/delete/<int:share_id>/', methods = ['DELETE'])
def delete_share(share_id):
    try:
        ShareModel.delete_share(share_id)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
