# -*- coding: UTF-8 -*-
import hashlib
from datetime import datetime

from sqlalchemy import or_

from app import db
from app.pagination import Pagination
from ..models import  User, ProductOrder, UserIncome, UserWithdrawal, UserMsg, InviteRecord, SocialUser, UserFollow, \
    CourseCouponGoods, GoodsOrder

__author__ = 'Ivan'


class CourseCouponGoodsDao():


    def save(self, goods):
        db.session.add(goods)
        db.session.commit()

    def find_all(self):
        return  CourseCouponGoods.query.filter(CourseCouponGoods.status==1).order_by(CourseCouponGoods.id.desc()).all()

    def get_all(self):
        return CourseCouponGoods.query.order_by(CourseCouponGoods.id.desc(),CourseCouponGoods.status.desc()).all()



    def get(self,id):

        return  CourseCouponGoods.query.filter(CourseCouponGoods.id==id).first()






class GoodsOrderDao():
    def save(self,order):
        db.session.add(order)
        db.session.commit()



    def find_top10(self):
        return GoodsOrder.query.order_by(GoodsOrder.created_time.desc()).limit(10).all()

    def pagination(self, page_index, page_size):

        query = GoodsOrder.query

        query = query.order_by(GoodsOrder.created_time.desc())

        count = query.count()

        offset = 0
        page_index=int(page_index)
        page_size=int(page_size)
        if (page_index > 1):
            offset = (page_index - 1) * page_size

        items = query.offset(offset).limit(page_size).all()

        return Pagination(count, page_index, page_size, items);