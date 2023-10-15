from flask import Blueprint, jsonify, request
from src.models.DataModel import DataModel
import datetime

main = Blueprint('data_blueprint', __name__)

@main.route('/',  methods = ['GET'])
def update_users_data():
    try:
        interests = DataModel.get_interest()
        genders = DataModel.get_gender()
        birthdates, seccion = DataModel.get_birthdate_and_seccion()

        ages = calculate_ages(birthdates)

        interests_count = count_data(interests)
        gender_count = count_data(genders)
        seccion_count = count_data(seccion)
        ages_count = count_data(ages)
        
        return jsonify({
            'interests': interests_count,
            'gender': gender_count,
            'seccion': seccion_count,
            'age': ages_count
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


def count_data(array):
    data_count = {}
    for element in array:
        if element != None:
            if element in data_count:
                data_count[element] += 1
            else:
                data_count[element] = 1
    return data_count

def calculate_ages(birthdates):
    today = datetime.date.today()
    ages = []
    for birthdate in birthdates:
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        ages.append(age)
    return ages;