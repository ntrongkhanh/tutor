import base64

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from app.util.ApiError import CustomError
from app.util.api_response import response_object
from config import app_config

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config.py')
    app.url_map.strict_slashes = False
    db.init_app(app)

    migrate.init_app(app, db)

    from . import model
    from app.blueprint import blueprint
    app.register_blueprint(blueprint)

    @app.route('/')
    def update():
        from app.model.image_model import Image
        obj = Image.query.get(1)
        image = base64.b64encode(obj.data).decode("utf-8")
        print(image)
        return render_template("image.html",  image=image)

    # @app.errorhandler(200)
    # def bad_request(error):
    #     return response_object(status=False, code=200, message=error.message), 200
    #
    # @app.route('/')
    # def mainpage():
    #     raise CustomError(404, 'Not found')

    return app
