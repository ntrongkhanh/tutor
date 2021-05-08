import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEFAULT_PAGE_SIZE = 10
    DEFAULT_PAGE = 1
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'khoaluan.tutor@gmail.com'
    MAIL_PASSWORD = 'khoaluan2021'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    TOKEN_EXPIRED_TIME = timedelta(seconds=10)


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    # FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:ntrongkhanh@localhost:5432/tutor"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SERVER_ADDRESS = ' http://127.0.0.1:5000'

class MySqlConfig(Config):
    """
    Development configurations
    """
    # FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://ntrongkhanh:ntrongkhanh@127.0.0.1:3306/tutor"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SERVER_ADDRESS = ' http://127.0.0.1:5000'


class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@40.71.25.150:54320/tutor"
    SERVER_ADDRESS = 'http://40.71.25.150:5000'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'mysql': MySqlConfig,
    'testing': TestingConfig
}
