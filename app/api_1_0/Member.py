# -*- coding: UTF-8 -*-
from flask import jsonify
from app import User
from . import api
from .authentication import auth

__author__ = 'Ivan'




@api.route('/member/name/exist/<name>')
def is_member_exist_by_name(name):
    count =User.query.filter(User.username==name).count()

    return  jsonify({'exist':count>0})



@api.route('/member/email/exist/<email>')
def is_member_exist_by_email(email):
    count =User.query.filter(User.email==email).count()

    return  jsonify({'exist':count>0})



@api.route('/member/phone/exist/<phone>')
def is_member_exist_by_phone(phone):
    count =User.query.filter(User.mobi==phone).count()

    return  jsonify({'exist':count>0})