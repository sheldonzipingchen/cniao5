# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime

from flask import redirect
from flask import render_template, jsonify
from flask import url_for
from flask.ext.login import login_required, current_user
from flask.ext.restful import marshal
from flask.ext.restful import fields

from app.activity import activity
from app.dao.activity_dao import ActivityPostDao, DoubleElevenDao
from app.dao.thread_dao import ThreadPostDao
from app.dao.user_dao import UserDao
from app.models import ActivityPost
from app.openapi.common_fields import user_fields
from app.openapi.utils import DateFormat
from app.util.str_util import create_uuid




@activity.route("/12.html")
def acti_12():
    dao = DoubleElevenDao();

    # 项目实战
    course_sz = dao.find_by_type(1);
    course_xxm = dao.find_by_type(2);
    course_qd = dao.find_by_type(3);
    course_rm = dao.find_by_type(4);
    course_ys = dao.find_by_type(5);

    return  render_template("ativity/12/index.html",
                            course_sz=course_sz,
                            course_xxm=course_xxm,
                            course_qd=course_qd,
                            course_rm=course_rm,
                            course_ys=course_ys)




@activity.route("/11.html")
def index():

    return redirect(url_for("main.index"));

    # user = None
    # if current_user.is_authenticated():  # 用户已登录
    #
    #     user_dao = UserDao();
    #     user = user_dao.get(current_user.id)
    #
    #
    # dao = DoubleElevenDao();
    #
    # # 项目实战
    # course_sz = dao.find_by_type(1);
    # course_xxm = dao.find_by_type(2);
    # course_qd = dao.find_by_type(3);
    # course_rm = dao.find_by_type(4);
    # course_ys = dao.find_by_type(5);
    #
    # return  render_template("ativity/11/index.html",user=user,
    #                         course_sz=course_sz,
    #                         course_xxm=course_xxm,
    #                         course_qd=course_qd,
    #                         course_rm=course_rm,
    #                         course_ys=course_ys)