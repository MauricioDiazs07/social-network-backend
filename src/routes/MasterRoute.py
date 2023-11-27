import uuid
from decouple import config
from flask import Blueprint, jsonify, request
from src.models.ShareModel import ShareModel
from src.models.MasterModel import MasterModel
from src.models.MultimediaModel import MultimediaModel
from src.models.InteractionModel import InteractionModel
from src.models.entities.multimedia import Multimedia
from src.models.MultimediaModel import MultimediaModel
from src.utils._support_functions import reformatCreatedDate
from src.utils.AmazonS3 import \
                            upload_file_to_s3, \
                            delete_file_from_s3

main = Blueprint('masters_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/',  methods=['PUT'])
def update_master_data():
    try:
        profile_id = request.form['profile_id']
        name = request.form['name']
        email = request.form['email']
        description = request.form['description']
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

                MasterModel.update_photo(profile_id,name,email,description,profile_photo)
                return jsonify({
                    'message': 'OK',
                    'profile_photo': profile_photo
                })
        else:
            MasterModel.update(profile_id,name,email,description)
            return jsonify({
                'message': 'OK'
            })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<profile_id>', )
def get_master_data(profile_id):
    try:
        master = MasterModel.get_info(profile_id)
        shares = ShareModel.get_shares_from_profile(profile_id)
        multimedias = MultimediaModel.get_all_multimedia()
        comments = InteractionModel.get_all_comments()
        likes = InteractionModel.get_all_likes()
        post = []
        history = []
        for share in shares:
            if share['shareType'] == 'POST':
                post_multimedia = []
                post_comment = []
                post_like = []
                autoLike = False
                for multimedia in multimedias:
                    if 'share_id' in multimedia and str(share['id']) == str(multimedia['share_id']):
                        multimedia.pop('share_id')
                        multimedia.pop('share_type')                      
                        post_multimedia.append(multimedia)
                for comment in comments:
                    if 'share_id' in comment and share['id'] == comment['share_id']:
                        comment.pop('share_id')
                        comment.pop('share_type')
                        post_comment.append(comment)
                for like in likes:
                    if 'share_id' in like and share['id'] == like['share_id']:
                        like.pop('share_id')
                        like.pop('share_type')
                        post_like.append(like)
                        if like['profile_id'] == share['profileId']:
                            autoLike = True
                share['multimedia'] = {"count": len(post_multimedia), "data": post_multimedia}
                share['comments'] = {"count": len(post_comment), "data": post_comment}
                share['likes'] = {"count": len(post_like), "data": post_like, "like": autoLike}
                share['creationDate'] = reformatCreatedDate(share['creationDate'])
                share.pop('name')
                share.pop('profileId')
                share.pop('profileImage')
                post.append(share)
            if share['shareType'] == 'HISTORY':
                post_multimedia = []
                for multimedia in multimedias:
                    if 'share_id' in multimedia and str(share['id']) == multimedia['share_id']:
                        multimedia.pop('share_id')
                        multimedia.pop('share_type')
                        multimedia.pop('profile_id')
                        post_multimedia.append(multimedia)
                share['multimedia'] = post_multimedia[0]
                history.append(share)
        master['post'] = post
        master['history'] = history
        return master
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500