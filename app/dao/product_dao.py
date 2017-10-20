# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta

from app.pagination import Pagination
from app.util.str_util import random_code
from ..models import  ProductVIP, ProductOrder, Order
from app import db


__author__ = 'Ivan'


vip_product_id=8

class ProductVIPDao():

    def get(self,id):

        return ProductVIP.query.get(id)

    def get_vip_product(self):
        return  ProductVIP.query.filter(ProductVIP.id==vip_product_id).first()





class ProductOrderDao():


    #product_type=3 是项目课程
     #product_type==0 是会员
    # #

    def save(self,product_order):
        db.session.add(product_order)
        db.session.commit()

    def save_new(self,user_id,days,product_id,product_type):

        cancel_time=datetime.now()+timedelta(days)
        product_order = ProductOrder(user_id=user_id,
                                         product_id=product_id,
                                         product_type=product_type,
                                         state=1,
                                         created_time=datetime.now(),
                                         order_time=datetime.now(),
                                         cancel_time=cancel_time,
                                         is_experience=0,
                                         )

        self.save(product_order)


    def add_vip_for_free(self,user_id,days):


        product_order = self.get_last_vip_product_order(user_id)

        if product_order is not  None:

            if product_order.cancel_time > datetime.now(): # 结束时间大于当前说明还在有效期

                product_order.cancel_time = product_order.cancel_time + timedelta(days)
                product_order.state = 1

                self.save(product_order)
            else:
                self.save_new(user_id,days,product_order.product_id,product_order.product_type)

        else: #new a product-order

            self.save_new(user_id,days,8,0)



        order_dao = OrderDao()

        title = '赠送高级会员%s天'% str(30)

        order_num = random_code(user_id,30)
        order = Order(order_num=order_num,
              title=title,
              user_id=user_id,
              product_id=8,
              product_type=0,
              order_count=1,
              coupon_id = 0,
              day=30,
              price=0,
              total_price=0,
              created_date = datetime.now(),
              pay_channel='FREE',
              trade_status ='TRADE_SUCCESS',
              )

        order_dao.create(order)




    def find_user_course_product_order(self,user_id):

        query =ProductOrder.query
        return query.filter(ProductOrder.user_id==user_id)\
            .filter(ProductOrder.state==1)\
            .filter(ProductOrder.product_type==3)\
            .all()

    def find_user_vip_order(self,user_id):

        query =ProductOrder.query
        return query.filter(ProductOrder.user_id==user_id)\
            .filter(ProductOrder.state==1)\
            .filter(ProductOrder.product_type==0,ProductOrder.product_id==8)\
            .all()


    def get_last_vip_product_order(self,user_id):

        query =ProductOrder.query
        return query.filter(ProductOrder.user_id==user_id)\
            .filter(ProductOrder.product_id==vip_product_id)\
            .filter(ProductOrder.product_type==0)\
            .filter(ProductOrder.state==1)\
            .order_by(ProductOrder.created_time.desc()).first()


    def get_user_un_expiration_vip(self,user_id):

        query =ProductOrder.query
        return query.filter(ProductOrder.user_id==user_id)\
            .filter(ProductOrder.product_id==vip_product_id)\
            .filter(ProductOrder.product_type==0)\
            .filter(ProductOrder.state==1)\
            .filter(ProductOrder.cancel_time>datetime.now())\
            .order_by(ProductOrder.created_time.desc()).first()





#################### 订单 ######################################

class OrderDao():
    def create(self,order):
        db.session.add(order)
        db.session.commit()

    def get(self,id):
        return Order.query.get(id)

    def get_or_404(self,id):
        return Order.query.get_or_404(id)

    def get_by_num(self,order_num):
       return Order.query.filter(Order.order_num==order_num).first()

    def get_user_last_unfinish_order(self,user_id,product_id,product_type):

        return  Order.query.filter(Order.trade_status=='INIT').filter(Order.user_id==user_id)\
            .filter(Order.product_id==product_id).filter(Order.product_type==product_type)\
            .order_by(Order.created_date.desc()).first()


    def find_user_orders(self,user_id,page_index,page_size):

        query = Order.query.filter(Order.user_id==user_id).order_by(Order.created_date.desc())

        count = query.count()

        offset = 0
        page_index=int(page_index)
        if (page_index > 1):
            offset = (page_index - 1) * page_size

        items = query.offset(offset).limit(page_size).all()

        return Pagination(count, page_index, page_size, items);

    def pagination(self,page_index,page_size,user_id=None,pay_channel=None,trade_status=None,order_num=None):
        query = Order.query.order_by(Order.created_date.desc())
        if user_id:
            query = query.filter(Order.user_id==user_id)

        if pay_channel:
            query = query.filter(Order.pay_channel==pay_channel)

        if trade_status:
            query = query.filter(Order.trade_status == trade_status)

        if order_num:
            query= query.filter(Order.order_num.like('%' + order_num + '%'))

        count = query.count()
        offset = 0
        page_index = int(page_index)
        if (page_index > 1):
            offset = (page_index - 1) * page_size


        items = query.offset(offset).limit(page_size).all()

        return Pagination(count, page_index, page_size, items);