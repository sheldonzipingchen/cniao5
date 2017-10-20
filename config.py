# -*- coding: UTF-8 -*-
"""
系统配置文件
"""
import os

from utils import make_dir

basedir = os.path.abspath(os.path.dirname(__file__))

__author__ = 'Sheldon Chen'


class Config(object):
    """
    基础配置
    """
    DEBUG = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '\xdf\xcd\xdf}\xe4<\xdf\xe4B\x9b\xb9\x8fN+\xd0\xb6\xd7-\xdd\xefT\xcfc\xdf'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    LOG_FOLDER = os.path.join(basedir, 'logs')
    make_dir(LOG_FOLDER)

    CNIAO5_ADMIN = 'Sheldon Chen'

    QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    SQLALCHEMY_ECHO = False


    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                               'mysql+mysqldb://%s:%s@%s/%s?charset=utf8' % (
                               'root', '123456', '127.0.0.1', 'cniao5_prodocution')

class TestingConfig(Config):
    """
    测试环境配置
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False
    CNIAO5_ADMIN = os.environ.get('CNIAO5_ADMIN')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                            'mysql+mysqldb://%s:%s@%s/%s?charset=utf8' % (
                            'eyoungadmin', 'eyoungmysqlroot', '121.199.46.160', 'cniao5_prodocution')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}