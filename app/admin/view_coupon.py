# -*- coding: UTF-8 -*-
import multiprocessing

from flask import render_template, request,redirect, url_for
from flask.ext.login import login_required

from app import db
from app.dao.class_dao import CourseDao
from app.dao.user_dao import UserDao
from app.models import Coupon
from app.util.str_util import random_code
from . import admin

__author__ = 'Ivan'



###优惠券管理
@admin.route('/coupon/manage')
@login_required
def coupon_manager():

    page = request.args.get('page', 1, type=int)
    par_value = request.form.get('par_value')
    date_start = request.form.get('date_start')
    date_end = request.form.get('date_end')

    pagination = Coupon.query
    if par_value is not None and par_value != '':
        pagination=pagination.filter(Coupon.val.__eq__(par_value))
    else:
        par_value=''
    if date_start is not None and date_start != '':
        pagination=pagination.filter(Coupon.expiry_time > date_start)
    else:
        date_start=''
    if date_end is not None and date_end != '':
        pagination=pagination.filter(Coupon.expiry_time < date_end)
    else:
        date_end=''
    pagination = pagination.order_by(Coupon.created_time.desc()).paginate(page, per_page=10, error_out=False)
    coupon_list = pagination.items

    return render_template('admin/coupon/list.html', coupon_list=coupon_list, pagination=pagination,
                           par_value=par_value, date_start=date_start, date_end=date_end)




@admin.route('/coupon/create')
@login_required
def coupon_create():

    # vips = ProductVIPDao().get_vip_product()

    courses =  CourseDao().get_project_courses()

    return render_template('admin/coupon/create.html',courses = courses)



@admin.route('/coupons/build',methods=['POST'])
@login_required
def coupons_build():

    from datetime import datetime
    users=request.form.get('users')
    par_value=request.form.get('par_value', type=int)
    expiry_time=request.form.get('expiry_time')
    build_num=request.form.get('build_num', type=int)
    payback=request.form.get('payback', type=int)
    user_for=request.form.get('user_for', type=int)

    temp_users = users.splitlines()

    user_dao = UserDao()
    course = CourseDao().get(user_for)

    title=u'全部课程'
    if course is not None:
        title = course.name

    if len(temp_users) > 0:
        for phone in temp_users:
            user = user_dao.find_by_email_phone(phone)
            if user is None:
                continue

            build(par_value,expiry_time,build_num,payback,user_for,title,user.id,datetime.now())

    else:
        build(par_value,expiry_time,build_num,payback,user_for,title,0,None)


    return  redirect(url_for('admin.coupon_manager'))

def build(par_value,expiry_time,build_num,payback,user_for_id,use_for_title,owner,get_time):

    from datetime import datetime
    coupons = []
    for i in range(int(build_num)):
        code = random_code(i,10)
        coupon = Coupon(val=par_value,
                        code=code,
                        created_time=datetime.now(),
                        expiry_time=expiry_time,
                        state=1,
                        payback=payback,
                        user_for_type=3,
                        user_for_id=user_for_id,
                        use_for_title=use_for_title,
                        owner=owner,
                        giver=0,
                        allow_give=True,
                        get_time=get_time)
        coupons.append(coupon)

    pool = multiprocessing.Pool(10)
    pool.close()
    pool.join()
    cucount=0

    for coupon in coupons:
        db.session.add(coupon)
        cucount +=1
        if cucount%300 == 0:
            db.session.commit()

    db.session.commit()