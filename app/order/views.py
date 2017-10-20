# -*- coding: UTF-8 -*-
import uuid
from flask import render_template, request, url_for,redirect
from flask.ext.login import login_required, current_user
from flask.ext.restful import abort

from app.storage import INVITE_DISCOUNT
from . import order
from app.dao.class_dao import CourseDao
from app.dao.coupon_dao import CouponDao
from app.dao.product_dao import ProductVIPDao, OrderDao
from app.dao.user_dao import UserMessageDao, UserDao
from app.models import Order, UserMsg
from app.util.data_validate_util import DataValidate
from app.util.order_util import is_legal_product_type
from .. util.str_util import random_code


__author__ = 'Ivan'

validator = DataValidate();

@order.route("/show")
@login_required
def show():

    args= request.args;
    product_id=args.get('product_id')
    product_type=args.get('product_type')


    if validator.isInteger(product_type)==False or is_legal_product_type(product_type)==False:
        return abort(404)


    if product_id is None  or validator.isPositiveInteger(product_id)==False:
        return abort(404)



    product_type = int(product_type)
    product_id = int(product_id)

    if product_type == 0: # 高级会员

        duration = args.get('duration') # 购买时长
        buy_type = args.get('unit') # 按月购买或者按年 ，month是按月，year是按年

        if validator.isPositiveInteger(duration)==False:
            return abort(404)

        if buy_type not in ['month','year']:
            return abort(404)

        duration = int(duration)

        title = '购买高级会员 X %d个月'%(int(duration))
        product = ProductVIPDao().get_vip_product();

        duration_f = float(duration)
        if buy_type== 'month':
            price = product.month_price
            total_price = product.month_price * duration_f
        elif buy_type=='year':
            price = product.year_price
            total_price = product.year_price * duration_f

        order = OrderModel(title,price,total_price,duration,None,True)

    elif product_type == 3: #课程

        course = CourseDao().get_or_404(product_id)
        if course.can_buy==False:
            return render_template("order/buy-tip.html",course_id=product_id);

        title = u'购买《%s》'%course.name
        buy_type='year'

        can_use_coupon=course.can_use_coupon
        order = OrderModel(title,course.now_price,course.now_price,1,course.img_url,can_use_coupon)

    else:
        return abort(404)


    return render_template('order/show.html',
                           order=order,
                           product_id=product_id,
                           product_type=product_type,
                           buy_type=buy_type
                           
                           )



@order.route("/create")
@login_required
def create():

    args= request.args;
    product_id=args.get('product_id')
    product_type=args.get('product_type')
    title=args.get('title')



    if validator.isInteger(product_type) == False or is_legal_product_type(product_type )== False:
        return abort(404)

    if product_id is None or validator.isPositiveInteger(product_id) == False:
        return abort(404)

    discount_type = args.get('discount_type',type=int)

    coupon_id = 0;
    invite_user_id=0

    if discount_type ==1 : #使用优惠码
        coupon_id = args.get('coupon_id')
        if coupon_id is None or validator.isInteger(coupon_id) == False:
            return abort(404)

    elif discount_type ==2: # 使用邀请码
        invite_user_id = args.get('invite_id')
        if invite_user_id is None or validator.isInteger(invite_user_id) == False:
            return abort(404)




    from datetime import datetime
    order_dao = OrderDao()

    order = order_dao.get_user_last_unfinish_order(current_user.id,product_id,product_type)


    if order is not None: #存在相同产品但是未付款的订单（48小时内的）

        if (datetime.now()- order.created_date).days < 2:
            return  redirect(url_for('pay.center',order_num=order.order_num))



    product_type = int(product_type)
    product_id = int(product_id)
    coupon_id = int(coupon_id)
    invite_user_id = int(invite_user_id)



    if discount_type==1: #使用优惠券
        coupon_dao =CouponDao();


        coupon = coupon_dao.get(coupon_id)

        if coupon is None: #判断优惠码是否存在
            coupon_id = 0
        else:
            if datetime.now() >coupon.expiry_time: #判断是否过期
                coupon_id= 0

            if coupon.state == 3: #判断是否被使用
                coupon_id =0

            if coupon.owner != current_user.id: #判断是否是本人的
                coupon_id=0

    elif discount_type==2:
        user = UserDao().get(invite_user_id)
        if user is  None: #如果用户不存在则设置为0
            invite_user_id=0

        if user.id == current_user.id: #不能自己的使用邀请码
            invite_user_id=0;




    if product_type==0: #会员

        order_count=args.get('count') #购买多少个月或者多少年
        buy_type = args.get('unit') # 按月购买或者按年 ，month是按月，year是按年

        product_vip = ProductVIPDao().get_vip_product();

        order_count = int(order_count)


        if buy_type== 'month':

            price =product_vip.month_price
            day = order_count * 31;

        elif buy_type=='year':
            price =product_vip.year_price
            day = order_count * 365;

        total_price = order_count * float(price)

        if discount_type==2:
            total_price = total_price - (total_price * INVITE_DISCOUNT)


    elif product_type ==3: #课程
        course = CourseDao().get_or_404(product_id)


        order_count=1
        day= course.expiry_day
        price =course.now_price
        total_price = price * order_count



    if discount_type == 1:
        if coupon_id > 0 and total_price > coupon.val:
            total_price = total_price -coupon.val # 减去优惠卷的抵扣金额

            try:
                coupon.state = 3
                coupon.use_time = datetime.now()
                coupon_dao.save(coupon)
            except:
                pass



    elif discount_type==2 :

        if invite_user_id>0:
            total_price = total_price - (total_price * INVITE_DISCOUNT)


    order_num = random_code(current_user.id,30)
    order = Order(order_num=order_num,
                  title=title,
                  user_id=current_user.id,
                  product_id=product_id,
                  product_type=product_type,
                  order_count=order_count,
                  coupon_id = coupon_id,
                  invite_user_id=invite_user_id,
                  day=day,
                  price=price,
                  total_price=total_price,
                  created_date = datetime.now(),
                  )

    order_dao.create(order)



    user_msg = UserMsg(title=u'下单成功',
                       msg=u'恭喜你下单成功，订单号为：%s。请在４８小时内完成支付！逾期订单将被取消'%(order_num),
                       from_user_id=9999,
                       to_user_id=order.user_id,
                       is_read=0
                       )


    UserMessageDao().save(user_msg)

    return redirect(url_for('pay.center',order_num=order_num))








class OrderModel():
    def __init__(self,title,price,total_price,count,pic,can_use_coupon):
        self.pic=pic
        self.title=title
        self.price=price
        self.total_price=total_price
        self.count=count
        self.can_use_coupon=can_use_coupon