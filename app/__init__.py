import os

from flask import Flask
from config import app_config


def create_app(config_name):
    if os.getenv('FLASK_CONFIG') == 'production':
        app = Flask(__name__)
        app.config.update(
        )
    else:
        app = Flask(__name__)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('../config.py')

    @app.route('/')
    def index():

        return 'hello'

    @app.route('/b')
    def a():
        a = app.config['AAA']

        print(type(a))
        print(a)
        if a:
            print('true')
        else:
            print('false')
        return 'a'

    return app
