# -*- coding: UTF-8 -*-
from datetime import timedelta
from flask import Flask
from flask.ext.cache import Cache
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from redis import Redis

from config import config
__author__ = 'Sheldon Chen'




session_lifetime = 2 * 60 * 60
cache_view_time=3600 #一个小时

redis = Redis()
login_manager = LoginManager()
db = SQLAlchemy()

cache = Cache(config={'CACHE_TYPE': 'redis',  # Use Redis
                           'CACHE_REDIS_HOST': '127.0.0.1',  # Host, default 'localhost'
                           'CACHE_REDIS_PORT': 6379,  # Port, default 6379
                           'CACHE_REDIS_PASSWORD': '',  # Password
                           'CACHE_REDIS_DB': 2}
              )

def create_app(config_name =None):



    if config_name==None:
        config_name='production'

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    #配置session超时时间
    app.permanent_session_lifetime = timedelta(seconds=session_lifetime) #两个小时


    return app

