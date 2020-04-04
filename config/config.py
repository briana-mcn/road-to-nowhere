import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ''


class ConfigDev(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'


class ConfigTest(Config):
    pass


class ConfigProd(Config):
    pass
