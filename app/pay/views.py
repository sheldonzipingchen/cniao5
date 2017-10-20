# -*- coding: UTF-8 -*-

from flask import redirect, request, render_template, url_for, Response
from flask.ext.login import login_required
from flask.ext.restful import abort

from . import pay
from ..alipay.alipay import *
from app.dao.class_dao import CourseDao
from app.dao.product_dao import OrderDao
from app.pay.util import pay_result_handle, send_confirm_to_alipay


__author__ = 'Ivan'









@pay.route('/center/<string:order_num>')
@login_required
def center(order_num):


    order = OrderDao().get_by_num(order_num);
    course=None

    if order is None:
        return  abort(404)

    if order.trade_status=='TRADE_SUCCESS':
        return redirect(url_for('pay.result',success=1,msg=u'该订单已经成功，无需再次支付'))


    if order.product_type == 3: # 购买课程
        course = CourseDao().get_or_404(order.product_id)

    return render_template("pay/center.html",
                           order=order,
                           course=course)



@pay.route('/center/pay')
@login_required
def pay_order():
    order_num = request.args.get('order_num')

    order = OrderDao().get_by_num(order_num)

    if order is None:
        return  abort(404)

    if order.trade_status !='INIT':
        return  abort(404)

    order.pay_channel="ALIPAY"
    OrderDao().create(order)

    pay_url = create_direct_pay_by_user(order.order_num,
                                        order.title,
                                        order.title,
                                        str(order.total_price),
                                        Settings.ALIPAY_RETURN_URL,
                                        Settings.ALIPAY_NOTIFY_URL
                                        )

    return redirect(pay_url)






@pay.route("/result")
@login_required
def result():

    success=request.args.get('success')
    msg=request.args.get('message')
    return  render_template("pay/pay_finish.html",
                            success=success,
                            msg=msg)




@pay.route("/return/alipay")
def alipay_return():

    current_app.logger.info('>> pay callback handler start')

    # if notify_verify(request.args)==False:
    #     current_app.logger.info('>> verify error')
    #     return  redirect(url_for('pay.result',success=0,
    #                             message=u'交易签名验证失败，请稍后在会员中心查看支付结果'))


    tn = request.args['out_trade_no'] #order id
    trade_no = request.args['trade_no']
    trade_status = request.args['trade_status']

    current_app.logger.info('change the status of bill %s' % tn)
    current_app.logger.info('the status changed to %s' % trade_status)

    if trade_status == 'TRADE_FINISHED' or trade_status == 'TRADE_SUCCESS':
        success,msg= pay_result_handle(tn,trade_status)
        if success==1:
            send_confirm_to_alipay(trade_no)
        current_app.logger.info('>> 订单处理完成%s'%(tn))



    return   redirect(url_for('pay.result',success=success,
                                message=msg))





@pay.route("/notify/alipay",methods=['POST'])
def alipay_notify():
    current_app.logger.info('>>   handler alipay notify_async')

    if notify_verify(request.form):
        tn = request.form['out_trade_no'] #order id
        trade_no = request.form['trade_no']
        trade_status = request.form['trade_status']

        current_app.logger.info('notify_async:change the status of bill %s' % tn)
        current_app.logger.info('notify_async:the status changed to %s' % trade_status)

        if trade_status == 'TRADE_FINISHED' or trade_status == 'TRADE_SUCCESS':

            success,msg=pay_result_handle(tn,trade_status)
            current_app.logger.info('handle pay result:%d ,msg:%s ,the num  %s' %(success,msg, trade_status))

            send_confirm_to_alipay(trade_no)
            return Response('success')

    else:
        current_app.logger.info('notify_async: notify_verify error')






