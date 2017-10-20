# -*- coding: utf-8 -*-

# give wsgi the "application"
from app import create_app
application = create_app('production')