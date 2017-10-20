# -*- coding: UTF-8 -*-
from sqlalchemy import or_
from app import db
from .. models import Coupon


__author__ = 'longo'


class CouponDao():

    def get(self,id):
       return Coupon.query.get(id)

    def save(self,coupon):
         db.session.add(coupon)
         db.session.commit()

    def get_by_code(self,code):

        return Coupon.query.filter(Coupon.code==code).first()


    def find_user_coupons(self,user_id):
        return Coupon.query.filter(Coupon.owner==user_id).order_by(Coupon.get_time.desc()).all()

    def get_user_coupon_by_id(self,user_id,id):
         return Coupon.query.filter(Coupon.owner==user_id,Coupon.id==id).first()

    def get_user_coupon_by_code_and_use_for(self,user_id,use_for_type,use_for_id,code):

        query = Coupon.query.filter(Coupon.code==code)\
            .filter(Coupon.owner==user_id)\
            .filter(Coupon.user_for_type==use_for_type)\
            .filter(or_(Coupon.user_for_id==use_for_id,Coupon.user_for_id==0))


        return query.first()





    # def setCouponByUser(self, userid, couponval):
    #
    #     code = '' #random_code(1)  ###用户领用红包
    #     coupon = Coupon(val=couponval, code=code, created_time=datetime.now(),expiry_time=datetime.now(),state=2, type=2)
    #     db.session.add(coupon)
    #     db.session.commit()
    #
    #     user_coupon = UserCoupon(user_id=userid,
    #                               coupon_id=coupon.id,
    #                               coupon_code=coupon.code,
    #                               coupon_val=coupon.val,
    #                               get_time=datetime.now(),
    #                               expiry_time=coupon.expiry_time,
    #                               state=1)
    #
    #     db.session.add(user_coupon)
    #     db.session.commit()





