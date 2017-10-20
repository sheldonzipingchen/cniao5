# -*- coding: UTF-8 -*-


from flask.ext.restful import Resource

from ..dao.user_dao import UserDao


__author__ = 'Ivan'



class User(Resource):



    def get(self,id):
        dao =UserDao()
        user = dao.get(id)
        if user is None:
            return {'status':0, 'message':'user not found'} ,404
        else:
            data = {'id':user.id,  'username':user.username, 'email':user.email, 'mobi':user.mobi,
                                   'logo_url': user.logo_url}
            return {'status':1, 'data':data}

    def post(self,id):
        dao =UserDao()
        user = dao.get(id)
        if user is None:
            return {'status':0, 'message':'user not found'} ,404
        else:
            data = {'id':user.id,  'username':user.username, 'email':user.email, 'mobi':user.mobi,
                                   'logo_url': user.logo_url}
            return {'status':1, 'data':data}





class UserData():
    def __init__(self,id, username, email, logo_url):
        self.id=id
        self.username=username
        self.email=email
        self.logo_url=logo_url
