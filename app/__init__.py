import os

from flask import Flask,render_template
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
        return render_template('hello.html')

    @app.route('/b')
    def a():
        return 'a'

    return app
