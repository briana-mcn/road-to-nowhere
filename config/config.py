import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('ROAD_TO_NOWHERE_SECRET_KEY')
    ROAD_TO_NOWHERE_PORT = 6000


class ConfigDev(Config):
    pass


class ConfigTest(Config):
    pass


class ConfigProd(Config):
    pass
