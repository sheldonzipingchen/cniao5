# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

forum = Blueprint('forum', __name__)

from . import views