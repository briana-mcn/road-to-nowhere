import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = os.getenv('ROAD_TO_NOWHERE_SECRET_KEY')


class ConfigDev(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class ConfigTest(Config):
    TESTING = True


class ConfigProd(Config):
    pass
