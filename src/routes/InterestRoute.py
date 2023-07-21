from flask import Blueprint, jsonify, request
from src.models.InterestModel import InterestModel

main = Blueprint('interest_blueprint', __name__)

@main.route('/list', methods = ['GET'])
def interest_list():
    try:
        interest = InterestModel.get_all()
        return jsonify(interest)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

@main.route('/add', methods = ['POST'])
def add_interest():
    try:
        values = []
        for interest in request.json['interest']:
            values.append((request.json['profile_id'], interest))
        InterestModel.add_interests(values)
        return jsonify({'success': values})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    