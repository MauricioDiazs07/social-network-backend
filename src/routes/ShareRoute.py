from flask import Blueprint, jsonify, request
from src.utils.AmazonS3 import upload_file_to_s3, delete_file_from_s3
from src.models.ShareModel import ShareModel
from src.models.MultimediaModel import MultimediaModel
from src.models.InteractionModel import InteractionModel
from src.models.entities.share import CreateShare
from src.models.entities.multimedia import Multimedia
from src.models.InterestModel import InterestModel
from src.utils._support_functions import reformatCreatedDate
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
        share_interest = request.form['interests'].split(";")
        share = CreateShare(profile_id, share_type, description)
        share_id = ShareModel.create_share(share)

        values = []
        if len(share_interest) > 0:
            for interest_value in share_interest:
                values.append((share_id, interest_value))
            InterestModel.add_share_interests(values)
       
        if len(request.files) > 0:
            for fileitem in request.files:
                file = request.files[fileitem]
                if file and allowed_file(file.filename):
                    new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
                    upload_file_to_s3(file,new_name)
                    url = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
                    multimedia = Multimedia(profile_id, share_id, share_type, url, file.filename.rsplit('.',1)[1].lower())
                    MultimediaModel.create_multimedia(multimedia)

        return jsonify({'message': share_id})
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/update', methods = ['POST'])
def update_share():
    try:
        share_id = request.json['share_id']
        description = request.json['description']
        share_id = ShareModel.update_share(share_id,description)
        return jsonify({'message': share_id})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/get', methods = ['GET'])
def get_share():
    try:
        share_id = str(request.json['share_id'])
        share_type = request.json['share_type']
        share = ShareModel.get_share(share_id)
        print(share)
        if share == None:
            return {"message": "Share not fount"}
        multimedia = MultimediaModel.get_multimedia(share_id,share_type)
        print(multimedia)
        comment = InteractionModel.get_comment(share_id)
        likes = InteractionModel.get_likes(share_id)
        interest = InterestModel.get_share_interests(share_id)
        print(interest)
        autolike = False
        for like in likes:
            if like['profile_id'] == share['profileId']:
                autolike = True
                break
        share['interest'] = interest
        share['multimedia'] = {"count": len(multimedia), "data": multimedia}
        share['comments'] = {"count": len(comment), "data": comment}
        share['likes'] = {"count": len(likes), "data": likes, "like": autolike}
        return share
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/list/post', methods = ['POST'])
def list_share():
    try:
        profile_id = request.json['profile_id']
        shares = ShareModel.get_all_share()
        multimedias = MultimediaModel.get_all_multimedia()
        comments = InteractionModel.get_all_comments()
        likes = InteractionModel.get_all_likes()
        interests = InterestModel.get_all_share_interests()
        post = []
        history = []
        for share in shares:
            if share['shareType'] == 'POST':
                autoLike = False
                post_multimedia = []
                post_comment = []
                post_like = []
                post_interest = []
                for interest in interests:
                    if 'share_id' in interest and str(share['id']) == str(interest['share_id']):
                        post_interest.append(interest['id'])
                for multimedia in multimedias:
                    if 'share_id' in multimedia and str(share['id']) == multimedia['share_id']:
                        multimedia.pop('share_id')
                        multimedia.pop('share_type')
                        multimedia.pop('profile_id')
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
                        if like['profile_id'] == profile_id:
                            autoLike = True
                share['multimedia'] = {"count": len(post_multimedia), "data": post_multimedia}
                share['comments'] = {"count": len(post_comment), "data": post_comment}
                share['likes'] = {"count": len(post_like), "data": post_like, "like": autoLike}
                share['interest'] = post_interest
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
        profile = []
        data = []
        for his in history:
            if his['profileId'] not in profile:
                profile.append(his['profileId'])
                recuperado = list(dic for dic in history if dic['profileId'] == his['profileId'])
                historys = []
                for rec in recuperado:
                    d = {
                        'type':  rec['multimedia']['archive_type'],
                        'content':  rec['multimedia']['archive_url'],
                        'finish': 0
                    }
                    historys.append(d)

                perfil = {
                    'profileId': recuperado[0]['profileId'],
                    'profileImage': recuperado[0]['profileImage'],
                    'name': recuperado[0]['name'],
                    'historys': historys,
                    'description': recuperado[0]['text'],
                    'id': recuperado[0]['id']
                }
                data.append(perfil)
        return jsonify({
            'POST': post,
            'HISTORY': data
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/profile/<profile_id>', methods = ['GET'])
def list_share_from_profile(profile_id):
    try:
        shares = ShareModel.get_shares_from_profile(profile_id)
        multimedias = MultimediaModel.get_all_multimedia()
        comments = InteractionModel.get_all_comments()
        likes = InteractionModel.get_all_likes()
        post = []
        for share in shares:
            if share['shareType'] == 'POST':
                post_multimedia = []
                post_comment = []
                post_like = []
                autoLike = False
                for multimedia in multimedias:
                    if 'share_id' in multimedia and share['id'] == multimedia['share_id']:
                        multimedia.pop('share_id')
                        multimedia.pop('share_type')                      
                        post_multimedia.append(multimedia)
                for comment in comments:
                    if 'share_id' in comment and share['id'] == comment['share_id']:
                        comment.pop('share_id')
                        comment.pop('share_type')
                        post_comment.append(comment)
                for like in likes:
                    print(like)
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
                post.append(share)
        return post
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500



@main.route('/delete', methods = ['DELETE'])
def delete_share():
    try:
        share_id = request.json['shareId']
        share_type = request.json['shareType']
        ShareModel.delete_share(share_id)
        multimedia = MultimediaModel.get_multimedia(share_id,share_type)
        print(multimedia)
        for archive in multimedia:
            file = archive['archive_url'].split("/")[-1]
            print(file)
            delete_file_from_s3(file)
        MultimediaModel.delete_multimedia(share_id,share_type)
        InteractionModel.delete_all_comments(share_id)
        InteractionModel.delete_all_likes(share_id)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
