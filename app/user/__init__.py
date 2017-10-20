# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

user = Blueprint('user', __name__)

from . import views