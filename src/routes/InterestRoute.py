from flask import Blueprint, jsonify, request
from src.models.InterestModel import InterestModel
from src.models.entities.interest import Interest

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
    

@main.route('/update', methods = ['POST'])
def update_interest():
    try:
        profile_id = request.json['profile_id']
        interest_list = request.json['interest']
        interest = Interest(profile_id, interest_list)
        InterestModel.clean_interests(interest)

        values = []
        if len(interest_list) > 0:
            for interest in interest_list:
                values.append((profile_id, interest))
            InterestModel.add_interests(values)

        return jsonify({'success': values})
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500