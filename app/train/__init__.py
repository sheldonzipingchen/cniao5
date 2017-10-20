# -*- coding: UTF-8 -*-
from flask import Blueprint

__author__ = 'longo'

train = Blueprint('train', __name__)

from . import views