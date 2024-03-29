from flask import Blueprint, jsonify, request
from src.utils.AmazonS3 import upload_file_to_s3, delete_file_from_s3
from src.models.ShareModel import ShareModel
from src.models.MasterModel import MasterModel
from src.models.MultimediaModel import MultimediaModel
from src.models.InteractionModel import InteractionModel
from src.models.entities.share import CreateShare
from src.models.entities.multimedia import Multimedia
from src.models.InterestModel import InterestModel
from src.utils._support_functions import reformatCreatedDate
from src.recommender.order_results import sort_by_distances
from src.recommender.embedding.oneHot._simple import simpleOneHot
from decouple import config
import uuid
import random


main = Blueprint('share_blueprint', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/interest', methods = ['POST'])
def feed_interest():
    try:
        profile_id = request.json['profile_id']
        page_size = request.json['page_size']
        post_history = request.json['post_history']
        interest_id = request.json['interest_id']

        if not post_history:
            share_interest = ShareModel.get_share_from_interest(interest_id, page_size)
        else:
            share_interest = ShareModel.get_share_from_interest_filter(interest_id, post_history, page_size)

        posts = [str(post['id']) for post in share_interest]
        multimedias = MultimediaModel.get_all_multimedia_filter(posts)
        comments = InteractionModel.get_all_comments_filter(posts)
        likes = InteractionModel.get_all_likes_filter(posts)
        share_interests = InterestModel.get_all_share_interests_filter(posts)
        post = []
        for share in share_interest:
            autoLike = False
            post_multimedia = []
            post_comment = []
            post_like = []
            post_interest = []
            for interest in share_interests:
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
        return jsonify({
            'post': post,
            'interest_id': interest_id
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/feed', methods = ['POST'])
def feed_home():
    try:
        profile_id = request.json['profile_id']
        page_size = request.json['page_size']
        post_history = request.json['post_history']

        profile_interest = InterestModel.get_interests(profile_id)
        interest = InterestModel.get_all()
        share_interests = InterestModel.get_all_share_interests()

        interest_list = [x['id'] for x in interest]
        user_interest = [interest['interest_id'] for interest in profile_interest['interest_list']]
        user_onehot = simpleOneHot(interest_list,[user_interest])[0]

        id_a_tipos = {}
        for elemento in share_interests:
            id_actual = elemento['share_id']
            tipo_actual = elemento['id']

            if id_actual in id_a_tipos:
                id_a_tipos[id_actual].append(tipo_actual)
            else:
                id_a_tipos[id_actual] = [tipo_actual]

        post_final_oneHot = {}
        for share, interest_type in id_a_tipos.items():
            if share not in post_history:
                post_final_oneHot[str(share)] = simpleOneHot(interest_list, [interest_type])[0]
        post_short = []
        if len(post_final_oneHot) != 0:
            post_short = sort_by_distances(user_embedding=user_onehot, posts_embeddings=post_final_oneHot)
            print(post_short)
        post_interest_short= [int(data['post']) for data in post_short if data['similarity'] > 0]
        post_not_interest = [int(data['post']) for data in post_short if data['similarity'] == 0]

        num_random = round(page_size/5)
        num_post_interest = page_size - num_random;
        post_list = post_interest_short[0:num_post_interest]
        if len(post_list) != num_post_interest:
            num_random = page_size - len(post_list)
            if num_random >= len(post_not_interest):
                num_random = len(post_not_interest)
        post_random = random.sample(post_not_interest, num_random)

        i_random = random.randint(0, len(post_list))
        post_list[i_random:i_random] = post_random

        print('post interest:', post_interest_short)
        print('post not interest:', post_not_interest)
        print('post not interest random:', post_random)
        print('final post list: ',post_list)

        shares = ShareModel.get_all_share()
        multimedias = MultimediaModel.get_all_multimedia()
        comments = InteractionModel.get_all_comments()
        likes = InteractionModel.get_all_likes()
        post = []
        history = []
        for share in shares:
            if share['id'] in post_list:
                if share['shareType'] == 'POST':
                    autoLike = False
                    post_multimedia = []
                    post_comment = []
                    post_like = []
                    post_interest = []
                    for interest in share_interests:
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
                        'finish': 0,
                        'id': rec['id']
                    }
                    historys.append(d)

                perfil = {
                    'profileId': recuperado[0]['profileId'],
                    'profileImage': recuperado[0]['profileImage'],
                    'name': recuperado[0]['name'],
                    'historys': historys,
                    'description': recuperado[0]['text'],
                }
                data.append(perfil)
        return jsonify({
            'POST': sorted(post, key=lambda x: post_list.index(x['id'])),
            'HISTORY': data
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

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

        if share_type != 'HISTORY':
            share_interest = request.form['interests'].split(";")
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

@main.route('/get', methods = ['POST'])
def get_share():
    try:
        profile_id = request.json['profile_id']
        share_id = str(request.json['share_id'])
        share_type = request.json['share_type']
        share = ShareModel.get_share(share_id)
        if share == None:
            return {"message": "Share not fount"}
        multimedia = MultimediaModel.get_multimedia(share_id,share_type)
        comment = InteractionModel.get_comment(share_id)
        likes = InteractionModel.get_likes(share_id)
        interest = InterestModel.get_share_interests(share_id)
        print(interest)
        interest_list = [inter['interest_id'] for inter in interest]
        autolike = False
        for like in likes:
            if like['profile_id'] == profile_id:
                autolike = True
                break
        share['interest'] = interest_list
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
    

@main.route('/delete', methods = ['DELETE'])
def delete_share():
    try:
        share_id = request.json['shareId']
        share_type = request.json['shareType']
        InterestModel.delete_share_interest(share_id)
        ShareModel.delete_share(share_id)
        multimedia = MultimediaModel.get_multimedia(share_id,share_type)
        for archive in multimedia:
            file = archive['archive_url'].split("/")[-1]
            delete_file_from_s3(file)
        MultimediaModel.delete_multimedia(share_id,share_type)
        InteractionModel.delete_all_comments(share_id)
        InteractionModel.delete_all_likes(share_id)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500