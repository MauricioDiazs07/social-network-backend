from flask import Blueprint, jsonify, request
from src.models.DataModel import DataModel
from decouple import config

main = Blueprint('data_blueprint', __name__)


@main.route('/',  methods = ['GET'])
def update_users_data():
    try:
        interests = DataModel.get_interest()
        print(interests)
        interests_count = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0 }
        for interest in interests:
            print(interest)
            if interest == 1:
                interests_count["1"] = interests_count["1"] + 1
            elif interest == 2:
                interests_count["2"] = interests_count["2"] + 1
            elif interest == 3:
                interests_count["3"] = interests_count["3"] + 1
            elif interest == 4:
                interests_count["4"] = interests_count["4"] + 1
            elif interest == 5:
                interests_count["5"] = interests_count["5"] + 1
            elif interest == 6:
                interests_count["6"] = interests_count["6"] + 1
            elif interest == 7:
                interests_count["7"] = interests_count["7"] + 1

        return jsonify({
            'interests': interests_count        
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500