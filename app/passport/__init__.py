# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Ivan'

passport = Blueprint('passport', __name__,subdomain='passport')

from . import views