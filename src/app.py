from flask import Flask
from src.config import config
from flask_cors import CORS

# Routes
from src.routes import AuthRoute, UserRoute, TestRoute

app = Flask(__name__)
CORS(app)

def page_not_fount(error):
    return "<h1> 404 <h1>", 404

def create_app():
        app.config.from_object(config['development'])

        # Blueprints
        app.register_blueprint(AuthRoute.main, url_prefix = '/api/auth')
        app.register_blueprint(UserRoute.main, url_prefix = '/api/user')
        app.register_blueprint(TestRoute.main, url_prefix = '/api/access')

        # Error handlers
        app.register_error_handler(404, page_not_fount)
        app.run()

if __name__ == '__main__':
      create_app()