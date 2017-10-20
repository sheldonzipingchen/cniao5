# -*- coding: UTF-8 -*-
import decimal
import json

from datetime import datetime
from flask.ext.restful import fields
from flask import render_template, request, jsonify
from flask.ext.login import login_required
from flask.ext.restful import marshal

from app.dao.mall_dao import CourseCouponGoodsDao, GoodsOrderDao
from app.dao.user_dao import UserWithdrawalDao, UserDao, TeacherDao, UserIncomeDao
from app.models import Teacher, UserWithdrawal
from app.openapi.common_fields import user_fields, goods_order_pagination_fields
from app.openapi.utils import DateFormat
from app.util.date_util import get_last_month_fristday_lastday
from app.util.mobile_message import send_message_for_teacher_settlement
from . import admin

__author__ = 'Ivan'



@admin.route("/goods.html")
@login_required
def goods():
    goods = CourseCouponGoodsDao().get_all()

    return  render_template("admin/goods/index.html",goods=goods)



@admin.route("/goods/content/<int:id>")
@login_required
def goods_content(id):
    goods = CourseCouponGoodsDao().get(id)
    return render_template("admin/goods/conext.html",goods = goods)

@admin.route("/goods/update",methods=["POST"])
@login_required
def goods_update():

    params = request.get_json();

    id = params.get("id")
    val = params.get("val")
    action = params.get("action")

    dao = CourseCouponGoodsDao()

    goods = dao.get(id)

    if goods ==None:
        return  jsonify(success=0,message="找不到该商品")


    if action == 'status':
        goods.status = val


    if action=='content':
        goods.content = val
    if action=='stock':
        goods.stock = val

    if action=='price':
        goods.price = val

    if action=='title':
        goods.title = val

    if action=='expiry_date':
        goods.expiry_date = val

    if action=='val':
        goods.val = val


    dao.save(goods)

    return jsonify(success=1,message="更新成功")



@admin.route("/goods/orders.html")
@login_required
def goods_orders():
    return  render_template("admin/goods/orders.html")



@admin.route("/goods/orders")
@login_required
def goods_orders_json():
    params = request.args
    page_index = params.get("page_index")
    page_size = params.get("page_size")
    pagination = GoodsOrderDao().pagination(page_index,page_size)

    result = json.dumps(marshal(pagination, goods_order_pagination_fields))

    return result
