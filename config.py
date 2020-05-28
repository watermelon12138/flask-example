# coding:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# print('basedir: \n', basedir)


class Config(object):
    DEBUG = False
    TESTING= False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:yangxuan@localhost:5432/wordcount_dev'

class StaginConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True