# -*- coding: UTF-8 -*-

from flask import render_template, redirect, request, session, url_for
from flask.ext.login import current_user

from app import cache, cache_view_time
from app.dao.banner_dao import BannerDao
from app.dao.page_dao import PageMenuDao
from app.dao.user_dao import  TeacherDao
from app.models import Banner, Recommend, Course
from . import main

__author__ = 'Sheldon Chen'

@main.before_app_request
def before_request():

    """ 全局请求拦截器， """
    if 'channel' in request.args:
        channel = request.args['channel']
        # current_app.logger.debug('arg s: %s' % (channel, ))
        session['channel'] = channel



    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint[:5] != 'main.' \
            and request.endpoint != 'course.' \
            and request.endpoint != 'chapter.' \
            and request.endpoint != 'lesson.' \
            and request.endpoint != 'order.' \
            and request.endpoint != 'message.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@main.route('/')
# @cache.cached(timeout=cache_view_time)
def index():
    """ 首页 """

    banners = BannerDao().find_active()

    query=Course.query
    pro_list =query.join(Recommend, Recommend.resid ==Course.id)\
        .filter(Recommend.status==1, Recommend.restype==1).order_by(Recommend.sort.asc()).limit(4)

    class_list =query.join(Recommend, Recommend.resid ==Course.id)\
        .filter(Recommend.status==1, Recommend.restype==2).order_by(Recommend.sort.asc()).limit(8)

    teach_list = TeacherDao().find_recommend(4)

    menus = PageMenuDao().find_by_type(1)

    return render_template('index.html',
                           banners=banners,
                           pro_list=pro_list,
                           class_list=class_list,
                           teach_list=teach_list,
                           menus=menus)






@main.route("/teachers")
def teachers():
    teachers =TeacherDao().find_all()
    return  render_template("teachers.html",teachers=teachers)



@main.route('/search')
def search():
    return 'success'



@main.route('/download/devtools.html')
def devtools():

    return render_template('help/devtool.html')





