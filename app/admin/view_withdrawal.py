# -*- coding: UTF-8 -*-
import json

from flask import render_template, request, jsonify
from flask.ext.login import login_required
from flask.ext.restful import marshal

from app.dao.user_dao import UserWithdrawalDao, UserDao
from app.openapi.common_fields import withdrawal_pagination_simple_fields
from . import admin

__author__ = 'Ivan'




@admin.route("/withdrawals.html")
@login_required
def withdrawals():
    return  render_template("admin/withdrawal/index.html")



@admin.route("/withdrawal/state/<int:id>_<int:state>",methods=["POST"])
@login_required
def withdrawal_state_update(id,state):

    dao = UserWithdrawalDao()
    withdrawal = dao.get(id)
    if withdrawal ==None:
        return jsonify(success=0,message=u'该提现记录不存在')

    withdrawal.state=state
    dao.save(withdrawal)
    return jsonify(success=1,message=u'success')






@admin.route("/withdrawals")
@login_required
def withdrawal_pagination():

    params = request.args

    page_index=params.get("page_index",type=int)
    page_size=params.get("page_size",type=int)
    email_or_mobi=params.get("email_or_mobi")
    state=params.get("state")

    user_id=None
    if email_or_mobi !=None and email_or_mobi !='':
        user = UserDao().find_by_email_phone(email_or_mobi)
        if user !=None:
            user_id=user.id


    page = UserWithdrawalDao().pagination(page_index,page_size,state,user_id)

    result = json.dumps(marshal(page,withdrawal_pagination_simple_fields))

    return  result





