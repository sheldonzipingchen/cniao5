# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

invite = Blueprint('invite', __name__)

from . import views