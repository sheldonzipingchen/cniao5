# -*- coding: UTF-8 -*-
import socket
from datetime import datetime

from flask.ext.restful import reqparse, Resource

from app.class_authority_util import user_course_authority_course_api
from app.dao.user_dao import UserDao
from app import db
from app.models import User

__author__ = 'longo'

# class Login_api(Resource):
#
#     def get(self):
#
#         args = parser.parse_args()
#         email= args['email']
#         password= args['password']
#         userDao = UserDao()
#         user = userDao.find_by_email_phone(email)
#         result={'status':'fail' }
#         if user is not None and user.verify_password(password):
#             result={'status':'success', 'id':user.id,  'name':user.username, 'email':user.email, 'logo_url':user.logo_url}
#         return result
#
#     def post(self):
#
#         args = parser.parse_args()
#         email= args['email']
#         password= args['password']
#         userDao = UserDao()
#         user = userDao.find_by_email_phone(email)
#         result={'status':'fail' }
#         if user is not None and user.verify_password(password):
#             result={'status':'success', 'id':user.id,  'name':user.username, 'email':user.email, 'logo_url':user.logo_url}
#         return result


class Login_api2(Resource):


    def post(self):

        result={}
        result["status"] = 0



        args = parser.parse_args()
        email= args['email']
        password= args['password']
        course_id = args.get("course_id")

        userDao = UserDao()
        user = userDao.find_by_email_phone(email)



        if user is not None and user.verify_password(password):
            data = {'id':user.id,
                    'username':user.username,
                    'email':user.email,
                    'mobi':user.mobi,

                    'logo_url': user.logo_url
                    }
            result["status"]=1
            result["message"]=u'登录成功!'
            result["data"]=data

            if course_id:
                play_auth =  user_course_authority_course_api(course_id,user.id)

                result['course_permission']=play_auth
        else:
            result["message"] = u'登录名或者密码错误!'

        return result




class Reg_api(Resource):



    def post(self):

        result={}
        result["status"] = 0
        result["message"]=u'该接口已停止注册,请到菜鸟窝官网注册:http://www.cniao5.com/auth/reg.html'


        # ips = ['127.0.0.1', '192.168.199.148', '121.199.46.160', '121.124.22.238']
        # localIP = socket.gethostbyname(socket.gethostname())
        # #if localIP in ips:
        # if True:
        #     args = parser2.parse_args()
        #     mobi= args['mobi']
        #     password= args['password']
        #     message=''
        #     flag = True
        #     if mobi is None:
        #         flag = False;
        #         result["status"]=0
        #         result["message"]=u'手机或者密码为空!'
        #     if password is None:
        #         flag = False;
        #         result["status"]=0
        #         result["message"]=u'手机或者密码为空!'
        #     result={'status':0, 'message':message }
        #     if flag:
        #         userDao = UserDao()
        #         user = userDao.find_by_email_phone(mobi)
        #         if user is not None:
        #             result["status"]=0
        #             result["message"]=u'手机号码已被注册!'
        #         else:
        #             user = User(mobi=mobi,password=password, pwd=password, mobile_confirmed=True, confirmed=True,  reg_time = datetime.now())
        #             db.session.add(user)
        #             db.session.commit()
        #             data = {'id':user.id,  'username':user.username, 'email':user.email, 'mobi':user.mobi,
        #                            'logo_url': user.logo_url}
        #             result["status"]=1
        #             result["message"]=u'注册成功!'
        #             result["data"]=data
        # else:
        #      result["status"]=0
        #      result["message"]=u'IP地址验证失败!'
        return result






parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True , help=' email not null')
parser.add_argument('password', type=str, required=True , help=' password not null')
parser.add_argument('course_id', type=int, )


parser2 = reqparse.RequestParser()
parser2.add_argument('mobi', type=str, required=False , help=' mobi not null')
parser2.add_argument('password', type=str, required=False , help=' password not null')


