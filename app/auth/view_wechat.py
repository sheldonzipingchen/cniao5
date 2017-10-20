# -*- coding: UTF-8 -*-

from flask import url_for, session

from . import auth
from .. oauth_social_login import wechat

__author__ = 'Ivan'




@auth.route('/wechat/login')
def wechat_login():

  return wechat.authorize(callback=url_for('passport.wechat_authorized',_external=True))








