# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

api = Blueprint('api', __name__)

from . import authentication,Users,Member,Compilation,errors