# -*- coding: UTF-8 -*-
import decimal
import json

from datetime import datetime
from flask.ext.restful import fields
from flask import render_template, request, jsonify
from flask.ext.login import login_required
from flask.ext.restful import marshal

from app.dao.user_dao import UserWithdrawalDao, UserDao, TeacherDao, UserIncomeDao
from app.models import Teacher, UserWithdrawal
from app.openapi.common_fields import user_fields, income_pagination_simple_fields
from app.openapi.utils import DateFormat
from app.util.date_util import get_last_month_fristday_lastday
from app.util.mobile_message import send_message_for_teacher_settlement
from . import admin

__author__ = 'Ivan'





@admin.route("/teacher/lastmonth/income/<int:user_id>")
@login_required
def  teacher_last_month_income(user_id):

    begin,end =get_last_month_fristday_lastday()
    money = UserIncomeDao().find_user_total_income_in_time_bucket(user_id,begin,end)



    if money[0] ==None:
        return jsonify(money=0)

    income = float(decimal.Decimal(money[0]))

    return jsonify(money=income)



@admin.route("/teacher/settlement",methods=["POST"])
@login_required
def teacher_settlement():

    params = request.get_json();

    user_id = params.get("user_id");
    money = params.get("money");



    begin,end =get_last_month_fristday_lastday()
    last_month_income = UserIncomeDao().find_user_total_income_in_time_bucket(user_id,begin,end)


    if last_month_income[0] ==None:
        return jsonify(success=0,message=u'该老师上月收入为0')


    last_month_income = float(last_month_income[0])

    try:
        money =float(money)
    except:
        return jsonify(success=0,message=u'请输入正常的数字')


    if money>last_month_income:
        return jsonify(success=0,message=u'结算金额大于上月收入')



    user_dao = UserDao()

    user = user_dao.get(user_id)

    if user==None:
        return jsonify(success=0,message=u'讲师不存在')


    if float(user.balance) < money:
        return jsonify(success=0,message=u'账户余额不足')


    #扣除账户余额
    user.balance = user.balance-decimal.Decimal(money)
    user_dao.save(user)


    teacher = TeacherDao().get_by_user_id(user_id)

    #添加结算记录
    withdrawal = UserWithdrawal(user_id=user_id,
                                apply_money=money,
                                pay_money=money,
                                service_charge=0,
                                pay_channel=teacher.bank_name,
                                beneficiary_account=teacher.bank_account,
                                state=1,
                                hande_user_id=1,
                                hande_time=datetime.now(),
                                created_time=datetime.now(),

                                )
    UserWithdrawalDao().save(withdrawal)


    #发送短信通知
    if user.mobi!=None and user.mobi !='':
        print  'send message'
        send_message_for_teacher_settlement(user.mobi,money)


    return jsonify(success=1,message=u'结算成功')







##################----------#########################

@admin.route('/teachers.html')
@login_required
def teachers():
    teachers = TeacherDao().find_all()

    return render_template("admin/user/teachers.html",teachers=teachers)

@admin.route('/teacher/add')
@login_required
def teacher_add():
    return  render_template("admin/user/teacher-add.html")



@admin.route('/teacher/save',methods=["POST"])
@login_required
def teacher_save():

    json = request.get_json();
    teacher_name = json.get("teacher_name")
    idcard = json.get("idcard")
    rate = json.get("rate")
    user_id = json.get("user_id")
    company = json.get("company")
    brief = json.get("brief")
    logo_url = json.get("logo_url")


    t = Teacher(user_id=user_id,teacher_name=teacher_name,
                id_num=idcard,logo_url=logo_url,rate=rate,
                company=company,brief=brief)

    TeacherDao().save(t)

    return  jsonify(success=1)


@admin.route("/teacher/users")
@login_required
def teacher_users():

      users =   UserDao().find_teacher_users()

      result = json.dumps(marshal(users,user_fields))

      return result



@admin.route("/teacher/incomes.html")
@login_required
def teacher_incomes():

    return  render_template("admin/user/teacher-income.html")




@admin.route("/teacher/incomes")
@login_required
def teacher_incomes_list():

    params = request.args

    page_index=params.get("page_index",type=int)
    page_size=params.get("page_size",type=int)
    email_or_mobi=params.get("email_or_mobi")

    user_id=None
    if email_or_mobi !=None and email_or_mobi !='':
        user = UserDao().find_by_email_phone(email_or_mobi)
        if user !=None:
            user_id=user.id

    page = UserIncomeDao().find_teachers_income(page_index,page_size,user_id)

    result = json.dumps(marshal(page,income_pagination_simple_fields))
    return  result



