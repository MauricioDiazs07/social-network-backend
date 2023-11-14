from flask import Blueprint, jsonify, request
from src.models.DataModel import DataModel
from src.models.CatalogueModel import CatalogueModel
import datetime

main = Blueprint('data_blueprint', __name__)

@main.route('/',  methods=['GET'])
def all_data():
    try:
        feelings_all = CatalogueModel.feeling_data()
        interest_all = CatalogueModel.interest_data()
        interests = DataModel.get_interest()
        genders = DataModel.get_gender()
        birthdates, section = DataModel.get_birthdate_and_section()
        comments = DataModel.get_feelings_comments()
        
        acceptance_count = count_feelings(feelings_all, comments)
        interests_count = count_data(interests)
        interest_count_des = add_count(interests_count,interest_all)
        interest_data = rename_interest(interest_count_des)
        gender_count = create_object_data(genders)
        ages_classified = classified_ages(birthdates)
        section_count = create_object_data_sorted(section)

        return jsonify({
            'interests': {
                'array': [dicc['marker'] for dicc in interest_data],
                'data': interest_data
            },
            'gender': gender_count,
            'section': {
                'array': sorted(list(set(section))),
                "data": section_count
            },
            'age': ages_classified,
            'acceptance': acceptance_count
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/section/<section>',  methods=['GET'])
def seccion_data(section):
    try:

        interests = DataModel.get_interests_by_section(section)
        interest_all = CatalogueModel.interest_data()
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
            'section': section_count
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/acceptance/<section>',  methods=['GET'])
def acceptance_data(section):
    try:
        feelings_all = CatalogueModel.feeling_data()
        interest_all = CatalogueModel.interest_data()
        acceptance = DataModel.get_acceptance_by_section(section)
        acceptance_count = count_acceptance(feelings_all,interest_all,acceptance)

        return jsonify({
            'section': section,
            'acceptance': acceptance_count
        })
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


def create_object_data(array):
    data_count = {
        "M": 0,
        "H": 0
    }
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
        "Menor o igual 10": 0,
        "11 - 20": 0,
        "21 - 30": 0,
        "31 - 40": 0,
        "41 - 50": 0,
        "51 - 60": 0,
        "61 - 70": 0,
        "71 - 80": 0,
        "Mayor 80": 0
    }

    for age in ages:
        if age < 10:
            data["Menor o igual 10"] += 1
        elif age >= 11 and age <= 20:
            data["11 - 20"] += 1
        elif age >= 21 and age <= 30:
            data["21 - 30"] += 1
        elif age >= 31 and age <= 40:
            data["31 - 40"] += 1
        elif age >= 41 and age <= 50:
            data["41 - 50"] += 1
        elif age >= 51 and age <= 60:
            data["51 - 60"] += 1
        elif age >= 61 and age <= 70:
            data["61 - 70"] += 1
        elif age >= 71 and age <= 80:
            data["71 - 80"] += 1
        elif age >= 81:
            data["Mayor 80"] += 1

    list_dicc= [{"marker": clave, "y": valor} for clave, valor in data.items()]
    for indice, diccionario in enumerate(list_dicc):
        diccionario["x"] = indice
    return list_dicc


def count_feelings(feelings_all, comments):
    data_count = {feel['description']: 0 for feel in feelings_all}
    for element in comments:
        if element != None:
            if element in data_count:
                data_count[element] += 1
            else:
                data_count[element] = 1

    list_dicc= [{"label": clave, "value": valor} for clave, valor in data_count.items()]
    return list_dicc

def count_acceptance(feelings_all,interest_all,acceptance_all):
    total = []
    for feeling in feelings_all:
        data_count = {interest['description']: 0 for interest in interest_all}
        for acceptance in acceptance_all:
            if feeling['description'] == acceptance['feeling']:
                data_count[acceptance['interest']] += 1
        final = transform(data_count)
        count = {
            'feeling': feeling['description'],
            'data': final
        }
        total.append(count)
    return total


def transform(data_count):
    info = []
    for i, data in enumerate(data_count):
        obj = {
            "marker": data,
            "x": i,
            "y": data_count[data]
        }
        info.append(obj)
    return info