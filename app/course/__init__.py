# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

course = Blueprint('course', __name__)

from . import views
