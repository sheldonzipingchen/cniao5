# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

member = Blueprint('member', __name__)

from . import views,views_course,views_account,views_notebooks,views_setting,views_coupon,views_invite



