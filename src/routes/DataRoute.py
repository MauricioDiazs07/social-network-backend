from flask import Blueprint, jsonify, request
from src.models.DataModel import DataModel
from src.models.InterestModel import InterestModel
import datetime

main = Blueprint('data_blueprint', __name__)


@main.route('/',  methods=['GET'])
def all_data():
    try:
        interests = DataModel.get_interest()
        genders = DataModel.get_gender()
        birthdates, seccion = DataModel.get_birthdate_and_seccion()
        interest_all = InterestModel.get_all()
        print(seccion)
        ages = calculate_ages(birthdates)
        ages_classified = classified_ages(ages)
        interests_count = count_data(interests)
        interest_count_des = add_count(interests_count,interest_all)

        gender_count = count_data(genders)
        seccion_count = count_data(seccion)

        return jsonify({
            'interests': interest_count_des,
            'gender': gender_count,
            'seccion': {
                'array': seccion,
                "count": seccion_count
            },
            'age': ages_classified
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/seccion/<seccion>',  methods=['GET'])
def seccion_data(seccion):
    try:
        interest_all = InterestModel.get_all()
        interests = DataModel.get_interests_by_seccion(seccion)
        interests_count = count_data(interests)
        interest_count_des = add_count(interests_count,interest_all)
        
        return jsonify({
            'interests': interest_count_des
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    


@main.route('/interest/<interest_id>',  methods=['GET'])
def interest_data(interest_id):
    try:
        seccion = DataModel.get_seccions_by_interest_id(interest_id)
        print(seccion)
        seccion_count = count_data(seccion)

        return jsonify({
            'seccion_count': seccion_count
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


def add_count(interests_count,interest_all):
    data = []
    for interest in interest_all:
        if interest['id'] in interests_count:
            interest['count'] = interests_count[interest['id']]
            data.append(interest)
        else:
            interest['count'] = 0
            data.append(interest)
    return data

def calculate_ages(birthdates):
    today = datetime.date.today()
    ages = []
    for birthdate in birthdates:
        age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))
        ages.append(age)
    return ages


def classified_ages(ages):
    data = {
        "Menor o igual 10 años": 0,
        "11 - 20 años": 0,
        "21 - 30 años": 0,
        "31 - 40 años": 0,
        "41 - 50 años": 0,
        "51 - 60 años": 0,
        "61 - 70 años": 0,
        "71 - 80 años": 0,
        "Mayor 80 años": 0
    }

    for age in ages:
        if age < 10:
            data["Menores 10 años"] += 1
        elif age >= 11 and age <= 20:
            data["11 - 20 años"] += 1
        elif age >= 21 and age <= 30:
            data["21 - 30 años"] += 1
        elif age >= 31 and age <= 40:
            data["31 - 40 años"] += 1
        elif age >= 41 and age <= 50:
            data["41 - 50 años"] += 1
        elif age >= 51 and age <= 60:
            data["51 - 60 años"] += 1
        elif age >= 61 and age <= 70:
            data["61 - 70 años"] += 1
        elif age >= 71 and age <= 80:
            data["71 - 80 años"] += 1
        elif age >= 81:
            data["Mayor 80 años"] += 1

    return data
