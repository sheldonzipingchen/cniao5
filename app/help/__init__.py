# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'Sheldon Chen'

help = Blueprint('help', __name__)

from . import views