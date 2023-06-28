from flask import Flask
from config import config

# Routes
from routes import LoginRoute, UserRoute, SignUpRoute

app = Flask(__name__)

def page_not_fount(error):
    return "<h1> 404 <h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(LoginRoute.main, url_prefix = '/api/login')
    app.register_blueprint(UserRoute.main, url_prefix = '/api/user')
    app.register_blueprint(SignUpRoute.main, url_prefix = '/api/signup')

    # Error handlers
    app.register_error_handler(404, page_not_fount)
    app.run()