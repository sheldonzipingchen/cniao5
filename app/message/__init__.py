# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

message = Blueprint('message', __name__)

from . import views
