# -*- coding: utf-8 -*-
import json
import random
from datetime import datetime

from flask import render_template, jsonify
from flask.ext.login import login_required, current_user
from flask.ext.restful import marshal
from flask.ext.restful import fields

from app.activity import activity
from app.dao.activity_dao import ActivityPostDao
from app.dao.thread_dao import ThreadPostDao
from app.dao.user_dao import UserDao
from app.models import ActivityPost
from app.openapi.common_fields import user_fields
from app.openapi.utils import DateFormat

#
# @activity.route("/find/lucky/girl.html")
# def find_the_lucky_girl():
#
#     return render_template("ativity/index.html")
#
#
# @activity.route("/qyz",methods=['POST'])
# @login_required
# def xinshu_choujiang():
#
#     ap_dao = ActivityPostDao()
#
#     list = ThreadPostDao().find_thread_today_posts(3572)
#
#
#     post =None
#
#     while (post==None):
#
#         temp = random.sample(list,1)[0]
#         p = ap_dao.get_by_user(temp.user_id)
#
#         if p is  None:
#             post=temp
#
#
#
#
#     user = UserDao().get(post.user_id)
#
#     if current_user.is_super_admin():
#         effective=True
#
#         ap = ActivityPost(user_id = user.id,post_id = post.id,created_time=datetime.now())
#         ap_dao.save(ap)
#
#     else:
#         effective=False
#
#     return jsonify(success=1,message="success",user_id=user.id,
#                    user_name=user.username,
#                    user_logo = user.logo_url,
#                    post_id=post.id,
#                    post_time=post.created_time,post_context=post.content,effective=effective)
#
#
#
#
#
#
# @activity.route("/qyz/lucky/users")
# def qyz_luckyers():
#
#    list = ActivityPostDao().find_all()
#    result = json.dumps(marshal(list,activity_post_fields))
#
#    return result
#
#
# activity_post_fields={
#
#     'id':fields.Integer,
#     'post_id':fields.Integer,
#     'created_time':DateFormat(attribute='created_time')
#
# }
#
# activity_post_fields['user']=fields.Nested(user_fields)