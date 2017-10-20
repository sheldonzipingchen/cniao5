# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

order = Blueprint('order', __name__)

from . import views