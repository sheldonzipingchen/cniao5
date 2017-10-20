# -*- coding: UTF-8 -*-
from datetime import  timedelta, datetime

from flask import current_app, url_for, Response

from .. alipay.alipay import send_goods_confirm_by_platform
from app.dao.class_dao import CourseDao
from app.dao.coupon_dao import CouponDao
from app.dao.product_dao import OrderDao, ProductOrderDao
from app.dao.user_dao import UserDao, UserIncomeDao, UserMessageDao
from app.models import ProductOrder, UserIncome, UserMsg
from app.util.email_message import send_email_use_template
from app.util.mobile_message import send_message_for_buy_vip_success, send_message_for_buy_course_success, \
    send_message_for_have_income


__author__ = 'Ivan'




def is_forum_admin(user_id,admins):
     is_admin=False

     for admin in admins:

        if user_id == admin.user.id:
            is_admin =True
            break


     if is_admin==False:
         user = UserDao().get(user_id)
         is_admin=user.is_super_admin()

     return is_admin