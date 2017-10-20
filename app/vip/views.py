# -*- coding: UTF-8 -*-
from . import vip
from datetime import datetime
from flask import jsonify, render_template
from flask.ext.login import login_required, current_user
from .. dao.product_dao import ProductVIPDao, ProductOrderDao
from .. dao.class_dao import CourseDao
from .. dao.user_dao import UserDao



__author__ = 'Ivan'

@vip.route("/")
def index():

    userDao = UserDao()
    courseDao =CourseDao()

    vip_members = userDao.find_vips(21);
    vip_courses = courseDao.find_vip_courses();

    is_vip=False
    product_order=None
    if current_user.is_authenticated(): #用户登录了

        product_order = ProductOrderDao().get_last_vip_product_order(current_user.id)

        if product_order is not None:
             if product_order.cancel_time > datetime.now(): # 结束时间大于当前时间说明会员在有效期
                 is_vip=True


    return  render_template('vip/index.html',
                            vip_members=vip_members,
                            vip_courses=vip_courses,
                            is_vip=is_vip,
                            product_order=product_order)



@vip.route("/buy")
@login_required
def buy():

    vip =ProductVIPDao().get_vip_product()
    json='{"%d":{"month":%d,"year":%d}}'%(vip.id,vip.month_price,vip.year_price)
    return render_template('vip/buy.html',
                           product=vip,
                           product_json=json)






@vip.route("/check/isvip")
@login_required
def is_vip():

    product_order = ProductOrderDao().get_last_vip_product_order(current_user.id)

    if product_order is None:

        return jsonify(is_vip=False,message=u'您不是高级会员')

    else:

        if product_order.cancel_time > datetime.now(): # 结束时间大于当前时间说明会员在有效期
             return jsonify(is_vip=True,message=u'您是尊贵的高级会员')
        else:

            return  jsonify(is_vip=False,message=u'您的高级会员已过期，请续费')




