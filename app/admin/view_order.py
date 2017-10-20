# -*- coding: UTF-8 -*-
from flask import render_template, request, jsonify
from flask.ext.login import login_required
from flask.ext.paginate import Pagination

from app.dao.product_dao import OrderDao
from . import admin

__author__ = 'Ivan'


PAGE_SIZE=10

@admin.route('/orders.html')
@login_required
def orders():

    args = request.args;

    page = args.get("page",type=int, default=1)
    pay_channel= args.get("pay",default='ALIPAY')
    trade_status= args.get("status",default='TRADE_SUCCESS')
    order_num= args.get("order_num")

    dao = OrderDao();

    result = dao.pagination(page,PAGE_SIZE,None,pay_channel,trade_status,order_num)

    pagination = Pagination(page=page, total=result.totalCount)

    return  render_template("admin/order/index.html",orders=result.datas,pagination=pagination,pay=pay_channel,status = trade_status)





@admin.route("/order/update",methods=["POST"])
@login_required
def order_update():

    params = request.get_json();

    id = params.get("id")
    val = params.get("val")
    action = params.get("action")

    dao = OrderDao()

    order = dao.get(id)

    if order ==None:
        return  jsonify(success=0,message="找不到该订单")


    if action == 'status':
        order.trade_status = val

    if action == 'price':
        order.price = val
        order.total_price=val

    dao.create(order)

    return jsonify(success=1,message="更新成功")

