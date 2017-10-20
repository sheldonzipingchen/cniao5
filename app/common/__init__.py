# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

common = Blueprint('common', __name__)

from . import views