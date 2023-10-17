from flask import Blueprint, jsonify, request
from src.models.DataModel import DataModel
from src.models.InterestModel import InterestModel
import datetime

main = Blueprint('data_blueprint', __name__)

@main.route('/',  methods=['GET'])
def all_data():
    try:
        interests = DataModel.get_interest()
        interest_all = InterestModel.get_all()
        interests_count = count_data(interests)
        interest_count_des = add_count(interests_count,interest_all)
        interest_data = rename_interest(interest_count_des)

        genders = DataModel.get_gender()
        gender_count = create_object_data(genders)

        birthdates, section = DataModel.get_birthdate_and_section()
        ages_classified = classified_ages(birthdates)
        section_count = create_object_data_sorted(section)

        return jsonify({
            'interests': {
                'array': [dicc['marker'] for dicc in interest_data],
                'data': interest_data
            },
            'gender': gender_count,
            'section': {
                # Ordenar
                'array': sorted(section),
                "data": section_count
            },
            'age': ages_classified
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/section/<section>',  methods=['GET'])
def seccion_data(section):
    try:

        interests = DataModel.get_interests_by_section(section)
        interest_all = InterestModel.get_all()
        interests_count = count_data(interests)
        interest_count_des = add_count(interests_count,interest_all)
        interest_data = rename_interest(interest_count_des)
        
        return jsonify({
            'interests': interest_data
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    


@main.route('/interest/<interest_id>',  methods=['GET'])
def interest_data(interest_id):
    try:
        section = DataModel.get_sections_by_interest_id(interest_id)
        section_count = create_object_data_sorted(section)

        return jsonify({
            'seccion_count': section_count
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


def create_object_data(array):
    data_count = {}
    for element in array:
        if element != None:
            if element in data_count:
                data_count[element] += 1
            else:
                data_count[element] = 1

    list_dicc= [{"label": clave, "value": valor} for clave, valor in data_count.items()]
    return list_dicc

def create_object_data_sorted(array):
    data_count = {}
    for element in array:
        if element != None:
            if element in data_count:
                data_count[element] += 1
            else:
                data_count[element] = 1

    list_dicc= [{"marker": clave, "y": valor} for clave, valor in data_count.items()]
    list_dicc_sorted = sorted(list_dicc, key=lambda x: int(x["marker"]))

    for indice, diccionario in enumerate(list_dicc_sorted):
        diccionario["x"] = indice

    return list_dicc_sorted


def rename_interest(interest_count_des):
    data = []
    for interest in interest_count_des:
        obj = {
            'y': interest['count'],
            'x': interest['id'] - 1,
            'marker': interest['description']
               }
        data.append(obj)
    return data

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

def classified_ages(birthdates):

    today = datetime.date.today()
    ages = []
    for birthdate in birthdates:
        age = today.year - birthdate.year - \
            ((today.month, today.day) < (birthdate.month, birthdate.day))
        ages.append(age)

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

    list_dicc= [{"marker ": clave, "y": valor} for clave, valor in data.items()]

    for indice, diccionario in enumerate(list_dicc):
        diccionario["x"] = indice

    return list_dicc
