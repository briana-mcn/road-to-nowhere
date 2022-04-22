import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('ROAD_TO_NOWHERE_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    ROAD_TO_NOWHERE_PORT = 5000
    ROAD_TO_NOWHERE_PYTHON_VER = '3.8.5'
    ROAD_TO_NOWHERE_PROJECT_DIR = '/usr/local/src/app'
    DEBUG_WEB_SERVER = False
    FLASK_APP = 'road_to_nowhere/app.py'


class ConfigDev(Config):
    pass

class ConfigTest(Config):
    TESTING = True


class ConfigProd(Config):
    pass
