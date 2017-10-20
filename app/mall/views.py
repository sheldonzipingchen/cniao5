# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from flask import render_template, jsonify
from flask import request
from flask.ext.login import login_required, current_user,abort

from app.dao.class_dao import CourseDao
from app.dao.coupon_dao import CouponDao
from app.dao.mall_dao import CourseCouponGoodsDao, GoodsOrderDao
from app.dao.user_dao import UserDao
from app.mall import mall
from app.models import Coupon, GoodsOrder
from app.util.str_util import random_code


@mall.route("/")
def index():

    goods = CourseCouponGoodsDao().find_all()

    orders = GoodsOrderDao().find_top10()

    user=None
    if current_user.is_authenticated():
        user = UserDao().get(current_user.id)

    return  render_template("mall/index.html",goods=goods,orders=orders,user=user)



@mall.route("/<int:id>")
def detail(id):
    goods = CourseCouponGoodsDao().get(id)
    if goods ==None:
        return  abort(404)
    if goods.status==0:
        return abort(404)

    user = None
    if current_user.is_authenticated():
        user = UserDao().get(current_user.id)
    return render_template("mall/detail.html",goods=goods,user=user)



@mall.route("/<int:id>/buy",methods=["POST"])
@login_required
def mall_buy(id):


    goods_dao = CourseCouponGoodsDao()

    goods = goods_dao.get(id)

    if goods is None:

        return jsonify(success=0,message=u'商品不存在')


    if goods.stock<=0:
        return jsonify(success=0, message=u'商品库存不足')



    user = UserDao().get(current_user.id)


    if goods.price > user.coin:
        return jsonify(success=0,message=u'鸟币不足')


    #扣除鸟币
    user.coin = user.coin-goods.price
    UserDao().save(user)


    #减少库存
    goods.stock= goods.stock-1
    goods_dao.save(goods)

    real_name=None
    addr=None
    mobi=None
    pay_type='coin'
    if goods.is_virtual==False: #非虚拟物品

        params = request.get_json();
        real_name = params.get("real_name");
        addr = params.get("addr");
        mobi = params.get("mobi");

    else:

        # 创建优惠码
        course = CourseDao().get(goods.class_id)
        code = random_code(user.id, 10)
        coupon = Coupon(
            val=goods.val,
            code=code,
            created_time=datetime.now(),
            expiry_time=datetime.now() + timedelta(days=goods.expiry_date),
            state=1,
            payback=0,
            user_for_type=3,
            user_for_id=goods.class_id,
            use_for_title=course.name,
            owner=user.id,
            giver=0,
            allow_give=True,
            get_time=datetime.now())

        CouponDao().save(coupon)



    #保存订单
    order =GoodsOrder(order_num=uuid.uuid4(),
                      title='兑换%s'%goods.title,
                      user_id=user.id,
                      goods_id=goods.id,
                      total_price=goods.price,
                      created_time=datetime.now(),
                      pay_type=pay_type,
                      receiver=real_name,
                      addr=addr,
                      mobi=mobi,

                      )

    GoodsOrderDao().save(order)

    return jsonify(success=1,message=u'兑换成功')


@mall.route("/user/orders")
@login_required
def user_orders():
    pass