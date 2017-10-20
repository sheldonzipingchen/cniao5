# -*- coding: UTF-8 -*-
from datetime import datetime
from flask import jsonify, request, flash
from app import User
from . import api
from app.models import UserCoupon
from .authentication import auth

__author__ = 'Ivan'



@api.route('/users/<int:id>')
@auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    result={'name':user.username,'email':user.email}
    return jsonify(result)



@api.route('/user/coupons/<int:user_id>')
def get_user_coupons(user_id):

    coupons =  UserCoupon.query.filter(UserCoupon.user_id==user_id,
                            UserCoupon.state==1,
                            UserCoupon.expiry_time>datetime.now()
                            ).all()




    return  jsonify({'coupons':[coupon.to_json() for coupon in coupons]})

