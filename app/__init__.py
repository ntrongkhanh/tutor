from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    from app import model

    @app.route('/')
    def index():
        return render_template('hello.html')

    @app.route('/b')
    def a():
        return 'a'

    return app
