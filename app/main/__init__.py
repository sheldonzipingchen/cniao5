# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

main = Blueprint('main', __name__)

from . import views, errors
