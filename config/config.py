import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''


class ConfigDev(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://dev:test@localhost:3306/road_to_nowhere'


class ConfigTest(Config):
    pass


class ConfigProd(Config):
    pass