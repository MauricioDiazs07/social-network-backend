from flask import Blueprint, jsonify, request
from src.utils.AmazonS3 import upload_file_to_s3
from src.models.ShareModel import ShareModel
from src.models.MultimediaModel import MultimediaModel
from src.models.InteractionModel import InteractionModel
from src.models.entities.share import CreateShare
from src.models.entities.multimedia import MultimediaOut
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
        share = CreateShare(profile_id, share_type, description)
        share_id = ShareModel.create_share(share)
        print(request.files)
        if len(request.files) > 0:
            for fileitem in request.files:
                file = request.files[fileitem]
                if file and allowed_file(file.filename):
                    new_name = uuid.uuid4().hex + '.' + file.filename.rsplit('.',1)[1].lower()
                    upload_file_to_s3(file,new_name)
                    url = 'https://{}.s3.{}.amazonaws.com/{}'.format(config('AWS_BUCKET_NAME'),config('REGION_NAME'),new_name)
                    multimedia = MultimediaOut(share_id, share_type, url, file.filename.rsplit('.',1)[1].lower())
                    MultimediaModel.create_multimedia(multimedia)

        return jsonify({'message': share_id})
    
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/get/<int:share_id>', methods = ['GET'])
def get_share(share_id):
    try:
        shares = ShareModel.get_share(share_id)
        multimedia = MultimediaModel.get_multimedia(share_id)
        comment = InteractionModel.get_comment(share_id)
        likes = InteractionModel.get_likes(share_id)
        print(likes)
        shares['multimedia'] = {"count": len(multimedia), "data": multimedia}
        shares['comments'] = {"count": len(comment), "data": comment}
        shares['likes'] = {"count": len(likes), "data": likes}
        return shares
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/list', methods = ['GET'])
def list_share():
    try:
        shares = ShareModel.get_all_share()
        multimedias = MultimediaModel.get_all_multimedia()
        comments = InteractionModel.get_all_comments();
        likes = InteractionModel.get_all_likes()
        post = []
        for share in shares:
            post_multimedia = []
            post_comment = []
            post_like = []
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
                if 'share_id' in like and share['id'] == like['share_id']:
                    like.pop('share_id')
                    like.pop('share_type')
                    post_like.append(like)        
            share['multimedia'] = {"count": len(post_multimedia), "data": post_multimedia}
            share['comments'] = {"count": len(post_comment), "data": post_comment}
            share['likes'] = {"count": len(post_like), "data": post_like}
            post.append(share)
        return post
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    

@main.route('/delete/<int:share_id>', methods = ['DELETE'])
def delete_share(share_id):
    try:
        ShareModel.delete_share(share_id)
        MultimediaModel.delete_multimedia(share_id)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
