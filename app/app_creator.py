# -*- coding: UTF-8 -*-
from flask import request, url_for

from app.models import User
from app.openapi.restful import config_restful_api
from . import redis, login_manager, db, cache





def init_app(app):

    configure_session(app)
    configure_jinja_env(app)
    configure_db(app)
    configure_blueprints(app)
    configure_login_manager(app)
    configure_restful_api(app)
    configure_logging(app)
    configure_cache(app)




def configure_session(app):

     from flask.ext.session import Session
     app.config['SESSION_TYPE'] = 'redis'
     app.config['SESSION_REDIS'] = redis
     Session(app)


def configure_blueprints(app):

    configure_sub_blueprints(app)


    from .admin import admin
    from .auth import auth
    from .clazz import clazz
    from .common import common
    from .course import course
    from .forum import forum
    from .help import help
    from .invite import invite
    from .lesson import lesson
    from .member import member
    from .message import message
    from .order import order

    from .pay import pay
    from .thread import thread
    from .train import train
    from .user import user
    from .vip import vip
    from .mall import mall
    from .qa import qa
    from .activity import activity

    SUBMODULE_BLUEPRINTS = (
    admin,  # 后台管理模块
    auth,  # 登录注册、权限相关
    course,  # 课程
    # chapter,  # 章节
    lesson,  # 课时
    member,  # 会员中心
    pay,  # 支付系统
    help,  # 帮助中心
    clazz, #班级主页
    train, #班级主页
    vip, #会员
    order, #会员
    message,#消息模块
    common, #公共模块
    thread, #帖子模块
    invite, #邀请模块
    forum, #社区
    user, #个人
    mall,#鸟币商城
    qa,#问答
    activity,#活动
    )

     # 默认路由定义
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    for blueprint in SUBMODULE_BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix='/%s' % blueprint.name)




def configure_sub_blueprints(app):

    from .passport import passport
    app.config['SERVER_NAME']='cniao5.com'
    app.url_map.default_subdomain = 'www'
    app.static_folder = 'static'
    app.add_url_rule('/static/<path:filename>',
                 endpoint='static',
                 subdomain='www',
                 view_func=app.send_static_file)
    app.register_blueprint(passport,subdomain=passport.name)






def configure_login_manager(app):



    # flask-login
    login_manager.init_app(app)
    #login_manager.session_protection = 'strong'
    login_manager.session_protection = 'basic'
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))




def configure_restful_api(app):
    #flask-restful
    config_restful_api(app)


def configure_logging(app):
    """
    Configure file(info)
    """
    import logging.config

    logging.config.fileConfig('logging.conf')
    logconsole = logging.getLogger('console')
    logconsole.debug('Debug CONSOLE')

def configure_jinja_env(app):
     # jinja 环境配置
    app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def configure_db(app):
    # flask-sqlalchemy
    db.init_app(app)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

# def configure_whooshalchemy(app):
#     import flask_whooshalchemyplus
#     app.config['WHOOSH_BASE'] = WHOOSH_BASE_DIR
#     flask_whooshalchemyplus.init_app(app)


def configure_cache(app):


    cache.init_app(app)