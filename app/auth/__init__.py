# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

auth = Blueprint('auth', __name__,static_folder='static')

from . import views,view_qq ,view_weibo,view_github,view_wechat