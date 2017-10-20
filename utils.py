# -*- coding: UTF-8 -*-

import string
import random
import os

from datetime import datetime

__author__ = 'SheldonChen'


def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception, e:
        raise e