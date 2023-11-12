from flask import Blueprint, jsonify, request
from src.models.InteractionModel import InteractionModel
from src.models.entities.interaction import Comment, Like
from src.utils.ModeloSentimientos import Clasifica

main = Blueprint('interaction_blueprint', __name__)


@main.route('/comment', methods = ['POST'])
def create_comment():
    try:
        profile_id = request.json['profile_id']
        share_id = request.json['share_id']
        share_type = request.json['share_type']
        text = request.json['text']
        feeling_id,feeling_percentage = Clasifica(text)
        comment = Comment(profile_id,share_id,share_type,text,feeling_id,feeling_percentage)
        InteractionModel.create_comment(comment)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update', methods = ['POST'])
def update_commet():
    id = request.json['id']
    text = request.json['comment']
    InteractionModel.update_comment(id, text)
    return jsonify({
        "message": "OK"
    })

@main.route('/delete/<int:id>', methods = ['DELETE'])
def delete_commet(id):
    InteractionModel.delete_comment(id)
    return jsonify({
        "message": "OK"
    })

@main.route('/like', methods = ['POST'])
def like():
    try:
        profile_id = request.json['profile_id']
        share_id = request.json['share_id']
        share_type = request.json['share_type']
        like = Like(profile_id,share_id,share_type)
        InteractionModel.add_like(like)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/dislike', methods = ['DELETE'])
def dislike():
    try:
        profile_id = request.json['profile_id']
        share_id = request.json['share_id']
        share_type = request.json['share_type']
        like = Like(profile_id,share_id,share_type)
        InteractionModel.dislike(like)
        return jsonify({
            "message": "DISLIKE"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
