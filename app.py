from flask import Flask
from src.config import config
from flask_cors import CORS

# Routes
from src.routes import AuthRoute, UserRoute, AiRoute, InterestRoute

app = Flask(__name__)
CORS(app)

def page_not_fount(error):
    return "<h1> 404 <h1>", 404

app.config.from_object(config['development'])

app.register_blueprint(AuthRoute.main, url_prefix = '/api/auth')
app.register_blueprint(UserRoute.main, url_prefix = '/api/user')
app.register_blueprint(AiRoute.main, url_prefix = '/api/ai')
app.register_blueprint(InterestRoute.main, url_prefix = '/api/interest')

# Error handlers
app.register_error_handler(404, page_not_fount)

if __name__ == '__main__':
    app.run()