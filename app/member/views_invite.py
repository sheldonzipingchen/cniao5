# -*- coding: UTF-8 -*-

# from PIL import Image
from flask import render_template, jsonify
from flask.ext.login import login_required, current_user

from app.dao.class_dao import CourseDao
from app.dao.user_dao import InviteRecordDao, UserDao
from app.storage import INVITE_DISCOUNT
from . import member

__author__ = 'Ivan'



@member.route("/invite/vip")
@login_required
def invite():

    dao = InviteRecordDao()
    datas =dao.find_user_invite_list(current_user.id)

    return render_template("member/invite/index.html",datas=datas)



@member.route("/invite/cash")
@login_required
def invite_cash():
    return render_template("member/invite/cash.html")


@member.route("/invite/user/<int:course_id>/check/<string:code>",methods=['POST'])
@login_required
def invite_coupon_check(course_id,code):


    user = UserDao().get_by_invite_code(code)

    if user is None:
        return jsonify(success=False, message=u'邀请码不存在')


    if user.id==current_user.id:
        return jsonify(success=False, message=u'不能使用自己的邀请码')

    course = CourseDao().get(course_id)

    if course is None:
        return jsonify(success=False,message=u'课程不存在')

    decreaseAmount = course.now_price * INVITE_DISCOUNT;

    return jsonify(success=True, message=u'success',  decreaseAmount=decreaseAmount,user_id = user.id,username=user.username)