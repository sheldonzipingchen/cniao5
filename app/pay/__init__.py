# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

pay = Blueprint('pay', __name__)

from . import views