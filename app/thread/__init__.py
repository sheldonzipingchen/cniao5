# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

thread = Blueprint('thread', __name__)

from . import views