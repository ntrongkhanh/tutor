from flask import Flask, redirect
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.util.api_error import CustomError
from app.util.api_response import response_object
from config import app_config

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager(app)


def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config.py')

    app.url_map.strict_slashes = False
    db.init_app(app)
    jwt = JWTManager(app)
    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)

    from . import model
    from app.blueprint import blueprint
    app.register_blueprint(blueprint)
    # CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    @jwt.token_in_blocklist_loader
    def check_token_in_blacklist(jwt_header, jwt_payload):
        from app.model.user_model import User
        from app.model.black_list_token import BlacklistToken
        jti = jwt_payload["jti"]
        black_list_token = BlacklistToken.query.all()

        list_token = []
        for token in black_list_token:
            list_token.append(token.token)

        if jti in list_token:
            raise NoAuthorizationError("Unauthorized")
        return False

    @app.route('/')
    def update():
        from app.model.image_model import Image
        return redirect('/api')

    return app
