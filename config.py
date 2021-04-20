import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    DEBUG = False

    DEFAULT_PAGE_SIZE = 10
    DEFAULT_PAGE = 1


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    # FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:ntrongkhanh@localhost:5432/tutor"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@127.0.0.1:5432/tutor"
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
    'testing': TestingConfig
}
