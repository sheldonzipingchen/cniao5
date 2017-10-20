# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'longo'

clazz = Blueprint('clazz', __name__)

from . import views