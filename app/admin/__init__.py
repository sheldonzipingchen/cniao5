# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

admin = Blueprint('admin', __name__)

from . import views,view_coupon,view_auth,view_course,view_withdrawal,view_user,view_goods,view_page,view_order