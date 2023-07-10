from flask import Blueprint

main = Blueprint('login_blueprint', __name__)

@main.route('/', methods = ['POST'])
def main():
    print("Todo funcionando")
    return "Hola mundo de Influex"