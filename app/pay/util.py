# -*- coding: UTF-8 -*-
import decimal
from datetime import  timedelta, datetime

from flask import current_app, url_for, Response

from app.storage import INVITE_DISCOUNT
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







# 处理支付结果
def pay_result_handle(tn,trade_status):


    current_app.logger.info('enter to handle order progress, the num: %s' % tn)
    order_dao = OrderDao()
    order =order_dao.get_by_num(tn)

    if order is None:
        current_app.logger.info('this order is not exist, num: %s' % (tn))
        success=0
        msg=u'此条订单不存在'
        return success,msg

    if order.trade_status == 'INIT':  # 订单号不为并且订单状态为INIT

        #step1 update order
        update_order(order,trade_status)


        #step2 update order-product
        update_order_product(order)


        #step3 share profit
        share_profit(order)

        #step4 notify user pay result
        notify_user_pay_result(order)


        success=1
        msg=u'支付成功'

        current_app.logger.info('handle order progress finish,  num: %s,status : %s' % (tn,order.trade_status))

    else:
        current_app.logger.info('this order is finish ,it do not need to change, num: %s,status %s:' % (tn,trade_status))
        success=1
        msg=u'此订单已完成'


    return  success,msg





def update_order(order,trade_status):
    order.trade_status = trade_status
    OrderDao().create(order)


def update_order_product(order):

    current_app.logger.info('enter to handle order_product progress, the num: %s' % order.order_num)


    if order.product_type ==0: #会员
        current_app.logger.info('the  order_product product_type is VIP, the num: %s' % order.order_num)
        update_order_product_for_vip(order)

    elif order.product_type==3: #课程
        current_app.logger.info('the  order_product product_type is Course, the num: %s' % order.order_num)
        update_order_product_for_course(order)


    user_msg = UserMsg(title=u'订单完成',
                       msg=u'恭喜你订单已完成，订单号为：%s。祝您学习愉快'%(order.order_num),
                       from_user_id=9999,
                       to_user_id=order.user_id,
                       is_read=0
                       )


    UserMessageDao().save(user_msg)



##############更新用户会员权限###############
def update_order_product_for_vip(order):

    current_app.logger.info('enter to handle update_order_product_for_vip progress, the num: %s' % order.order_num)
    from datetime import datetime

    dao = ProductOrderDao();
    product_order = dao.get_last_vip_product_order(order.user_id)

    if product_order is not  None:
        current_app.logger.info('product_order  not None , the id: %s' % product_order.id)
        if product_order.cancel_time > datetime.now(): # 结束时间大于当前说明还在有效期

            current_app.logger.info('product_order  not expired, update this  , the id: %s' % product_order.id)
            product_order.cancel_time = product_order.cancel_time + timedelta(order.day)
            product_order.state = 1

            dao.save(product_order)
        else:
            current_app.logger.info('product_order  expired , new a product_order')
            save_new_order_product(order)

    else: #new a product-order
        current_app.logger.info('product_order  is None , new a product_order')
        save_new_order_product(order)




##############更新用户课程权限###############
def update_order_product_for_course(order):
    save_new_order_product(order)






def save_new_order_product(order):

    from datetime import datetime
    cancel_time=datetime.now()+timedelta(order.day)
    product_order = ProductOrder(user_id=order.user_id,
                                     product_id=order.product_id,
                                     product_type=order.product_type,
                                     state=1,
                                     created_time=datetime.now(),
                                     order_time=order.created_date,
                                     cancel_time=cancel_time,
                                     is_experience=0,
                                     )


    ProductOrderDao().save(product_order)

    current_app.logger.info('save product_order success')









def share_profit(order):
    current_app.logger.info('enter to handle share_profit progress, the coupon_id: %s' % order.coupon_id)


    if order.product_type==3: #课程

        payback=0

        # 优惠码分享者的收入 = 优惠码返现
        if order.coupon_id > 0:

            coupon_dao = CouponDao()
            coupon = coupon_dao.get(order.coupon_id)

            if coupon is not None:

                payback = coupon.payback
                if coupon.giver > 0:
                    save_income(coupon.giver,coupon.payback,u'分享优惠码返现', 0,order.coupon_id)


        if order.invite_user_id>0: # 邀请人收入
            user = UserDao().get(order.invite_user_id)
            if user is not None and user.id != order.user_id:
                payback = float(order.total_price) * INVITE_DISCOUNT #邀请人收入= 订单金额 * 分成
                save_income(user_id=user.id,money=payback,title=u'分享邀请码返现',from_type=1,from_id=user.id)



        course = CourseDao().get(order.product_id) # 老师收入 = 订单金额 * 分成比例 - 分润（优惠码推荐收入）
        if course.rate > 0.0 :
            current_app.logger.info('save income for teacher,order_num:%s' % order.order_num)
            money = (float(order.total_price) * float(course.rate)) - float(payback)
            save_income(course.user_id,money,u'%s销售收入'% course.name,3,order.product_id)






def save_income(user_id,money,title,from_type,from_id):

    try:

        from datetime import datetime
        user_income = UserIncome(user_id=user_id,money=money,
                                 title=title,
                                 from_type=from_type,from_id=from_id,
                                 created_time=datetime.now())

        UserIncomeDao().save(user_income)


        #更新总收入
        user_dao = UserDao()
        user = user_dao.get(user_id)
        if user is not None:
            try:
                user.balance = user.balance + decimal.Decimal(money)
                user_dao.save(user)
            except:
                pass



        user_msg = UserMsg(title=u'进米通知',
                       msg=u'恭喜你进米了，本次%s共%s元,请再接再厉'%(title,str(money)),
                       from_user_id=9999,
                       to_user_id=user_id,
                       is_read=0
                       )


        UserMessageDao().save(user_msg)

        send_message_for_have_income(title,money)


    except:
        pass



def notify_user_pay_result(order):

    user_dao = UserDao()
    user = user_dao.get(order.user_id)


    if user is not None and user.mobi is not  None:

        if order.product_type==0: #购买会员

            if user.mobi is not None and user.mobi !='':
                dao = ProductOrderDao()
                product_order = dao.get_last_vip_product_order(order.user_id)
                ex_date=datetime.strftime(product_order.cancel_time,'%Y-%m-%d')
                send_message_for_buy_vip_success(user.mobi,ex_date,'105488654')
            else:
                current_app.logger.info('user mobi is null ,can not send sms,  user is is : %s' % str(user.id))

        elif order.product_type==3: #课程
            course = CourseDao().get_or_404(order.product_id);
            qq_num='无';
            if course.qqgroup is not None:
                    qq_num=course.qqgroup.group_num

            if user.mobi is not None and user.mobi !='':

                send_message_for_buy_course_success(user.mobi,qq_num,course.name)

            if user.email is not None and user.email !='':

                sub_vars = {
                'to': [user.email],
                'sub': {
                    '%user.username %': [user.username],
                    '%product_name %': [course.name],
                    '%qqgroup%': [qq_num],
                    '%class_url%': [url_for('course.course_detail',id=course.id,_external=True)]
                    }
                }
                send_email_use_template('user_payfor2016',sub_vars)


def send_confirm_to_alipay(trade_no):

    url = send_goods_confirm_by_platform(trade_no)
    import urllib

    req = urllib.urlopen(url)
    current_app.logger.info('send goods confirmation. %s' % url)



