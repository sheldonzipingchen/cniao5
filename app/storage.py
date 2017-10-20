# -*- coding: UTF-8 -*-
import os
__author__ = 'Sheldon Chen'

from qiniu import Auth, BucketManager

q = Auth(os.environ.get('QINIU_ACCESS_KEY'), os.environ.get('QINIU_SECRET_KEY'))
bucket = BucketManager(q)



INVITE_DISCOUNT=0.1;