# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from flask.ext.login import login_required, current_user


from app.qa import qa


@qa.route("/")
def index():
    pass





