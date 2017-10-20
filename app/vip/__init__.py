# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

vip = Blueprint('vip', __name__)

from . import views