# -*- coding: UTF-8 -*-
from datetime import datetime
from flask import render_template, jsonify, request
from flask.ext.login import login_required, current_user

from . import member
from app.dao.user_dao import UserDao
from .. dao.coupon_dao import CouponDao

__author__ = 'Ivan'





@member.route('/my/coupons')
@login_required
def coupons():

    coupon_dao = CouponDao()
    coupons = coupon_dao.find_user_coupons(current_user.id)
    return  render_template('member/coupon/list.html',coupons=coupons)



@member.route('/my/coupon/give',methods=['POST'])
@login_required
def coupon_give():

    json =request.get_json()

    mobile = json.get('mobile')
    coupon_id = json.get('coupon_id')

    user = UserDao().find_by_email_phone(mobile)
    if user is None:
        return jsonify(success=False,message=u'该用户不存在')

    if user.id == current_user.id:
        return jsonify(success=False,message=u'别闹了，好吗')

    dao = CouponDao()

    coupon = dao.get_user_coupon_by_id(current_user.id,coupon_id)

    if coupon is None:
        return jsonify(success=False,message=u'您没有这张优惠券')

    if coupon.state == 3:
        return jsonify(success=False,message=u'该优惠券已经被使用')

    if datetime.now() > coupon.expiry_time:
        return jsonify(success=False,message=u'该优惠券已经过期')


    coupon.giver=current_user.id
    coupon.owner = user.id
    coupon.get_time = datetime.now()
    coupon.allow_give=False

    dao.save(coupon)


    return jsonify(success=True,message=u'success')


@member.route("/coupon/user/<int:use_for_type>/<int:use_for_id>/check/<string:code>",methods=['POST'])
@login_required
def user_coupon_check(use_for_type,use_for_id,code):

    if code is None or code=='':
        return jsonify(success=False,message=u'优惠券码为空')

    dao = CouponDao()

    coupon = dao.get_user_coupon_by_code_and_use_for(current_user.id,use_for_type,use_for_id,code)

    if coupon is None:
        return jsonify(success=False,message=u'您没有这张优惠券')

    if coupon.state == 3:
        return jsonify(success=False,message=u'该优惠券已经被使用')

    if datetime.now() > coupon.expiry_time:
        return jsonify(success=False,message=u'该优惠券已经过期')


    return jsonify(success=True,message=u'success',coupon_id=coupon.id,decreaseAmount=coupon.val)