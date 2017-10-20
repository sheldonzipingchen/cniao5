# -*- coding: UTF-8 -*-


from flask.ext import restful

from app.openapi.thread_api import ThreadPagination, ThreadPostPagination
from .. openapi.class_api import Class, ClassChapter, ClassPlay, ClassCourseWare, ClassCommentPagination, \
    CoursePagination
from .. openapi.classnote_api import ClassNoteList
from .. openapi.login_api import  Reg_api, Login_api2
from .. openapi.user_api import User

__author__ = 'Ivan'


#url_prefix = '/api/v1/%s'

def config_restful_api(app):


    api = restful.Api(app)

    #课程相关
    api.add_resource(Class,'/api/v1/course/<int:id>')
    api.add_resource(ClassChapter,'/api/v1/course/<int:id>/chapters')
    api.add_resource(ClassPlay,'/api/v1/course/<int:id>/plays')
    # api.add_resource(ClassComment,'/api/v1/course/<int:id>/comments')
    api.add_resource(ClassCourseWare,'/api/v1/course/<int:id>/wares')

    api.add_resource(ClassNoteList,'/api/v1/notes')
    api.add_resource(CoursePagination,'/api/v1/course/pagination')
    api.add_resource(ClassCommentPagination,'/api/v1/course/comments/pagination')
    api.add_resource(ThreadPagination,'/api/v1/thread/pagination')
    api.add_resource(ThreadPostPagination,'/api/v1/thread/post/pagination')

    #用户相关
    # api.add_resource(User,'/api/v1/user/<int:id>')
    # api.add_resource(Login_api,'/api/v1/user/login')
    api.add_resource(Login_api2,'/api/v1/user/login2')
    api.add_resource(Reg_api,'/api/v1/user/reg')


