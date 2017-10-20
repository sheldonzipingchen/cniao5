# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

lesson = Blueprint('lesson', __name__)

from . import views
