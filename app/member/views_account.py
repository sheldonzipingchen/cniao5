# -*- coding: UTF-8 -*-
from datetime import datetime

from flask import json
from flask import jsonify, render_template, request
from flask.ext.login import login_required, current_user
from flask.ext.restful import marshal

from app.openapi.common_fields import  order_pagination_fields
from . import member
from app.dao.product_dao import OrderDao
from app.dao.user_dao import UserIncomeDao, UserDao, UserWithdrawalDao
from app.models import UserWithdrawal
from app.util.data_validate_util import DataValidate
from app.util.mobile_message import send__message

__author__ = 'Ivan'


@member.route('/my/revenue')
@login_required
def revenue():
    incomes = UserIncomeDao().find_user_incomes(current_user.id)

    user = UserDao().get(current_user.id)

    return render_template('member/account/revenue.html', incomes=incomes, user=user)


@member.route('/my/orders')
@login_required
def orders():
    return render_template('member/account/orders.html',)



@member.route('/my/orders/list')
@login_required
def orders_list():
    page_index = request.args.get("page_index")

    try:
        page_index = int(page_index)
    except:
        return jsonify(message='参数错误')

    pagination = OrderDao().find_user_orders(current_user.id, page_index, 10)
    result = json.dumps(marshal(pagination, order_pagination_fields))
    return  result;



@member.route('/my/order/<int:id>/cancel', methods=['POST'])
@login_required
def order_cancel(id):
    dao = OrderDao();
    order = dao.get_or_404(id)

    if order.trade_status == 'INIT':
        order.trade_status = 'CANCEL'
        dao.create(order)
        return jsonify(result=True)

    return jsonify(result=False)


@member.route('/my/withdrawals')
@login_required
def withdrawals():

    withdrawals = UserWithdrawalDao().find_user_withdrawals(current_user.id)
    return render_template('member/account/withdrawal.html',withdrawals=withdrawals)





@member.route('/withdrawal', methods=['POST'])
@login_required
def withdrawal():
    money = request.get_json().get('money')

    if not DataValidate().isPositiveInteger(money):
        return jsonify(success=False, message=u'请输入合法的金额')

    user_dao = UserDao()
    user = user_dao.get(current_user.id)

    if user.frozen_capital > 0:
        return jsonify(success=False, message=u'您还有未处理的提现，请耐心等待')

    money = float(money)
    if user.balance < money:
        return jsonify(success=False, message=u'您的账户余额不足')

    user.balance = float(user.balance)- money
    user.frozen_capital = money
    user_dao.save(user)

    service_charge = money * 0.02; # 2%的手续费

    withdrawal = UserWithdrawal(user_id=current_user.id,
                                apply_money=money,
                                created_time=datetime.now(),
                                pay_channel='alipay',
                                beneficiary_account=user.alipay,
                                service_charge=service_charge,
                                pay_money= money-service_charge,
                                state=0)

    UserWithdrawalDao().save(withdrawal)

    if user.mobi is not None:
        send__message(str(user.mobi), 1072, '{}')

    send__message(str('18664879291'), 1071, '{}')

    return jsonify(success=True, message=u'success')


@member.route('/my/alipay/check')
@login_required
def alipay_check():
    user_dao = UserDao()
    user = user_dao.get(current_user.id)

    if user.alipay is None or user.alipay == '':
        return jsonify(success=False, message=u'支付宝账户没有绑定')

    return jsonify(success=True, message=u'success')