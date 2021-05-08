import base64

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.util.ApiError import CustomError
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
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)

    from . import model
    from app.blueprint import blueprint
    app.register_blueprint(blueprint)

    @app.route('/')
    def update():
        from app.model.image_model import Image
        return render_template("hello.html")

    return app
