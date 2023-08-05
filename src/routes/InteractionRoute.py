from flask import Blueprint, jsonify, request
from src.models.InteractionModel import InteractionModel
from src.models.entities.interaction import Comment, Like

main = Blueprint('interaction_blueprint', __name__)


@main.route('/comment', methods = ['POST'])
def create_comment():
    try:
        profile_id = request.json['profile_id']
        share_id = request.json['share_id']
        share_type = request.json['share_type']
        text = request.json['text']
        comment = Comment(profile_id,share_id,share_type,text)
        InteractionModel.create_comment(comment)
        return jsonify({
            "message": "OK"
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/update', methods = ['POST'])
def update_commet():
    return jsonify({
        "message": "Comentario modificado"
    })

@main.route('/delete', methods = ['DELETE'])
def delete_commet():
    return jsonify({
        "message": "Comentario borrado"
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


@main.route('/dislike', methods = ['POST'])
def dislike():
    return jsonify({
        "message": "Like borrado"
    })
