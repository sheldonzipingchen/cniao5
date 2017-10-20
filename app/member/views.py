# -*- coding: UTF-8 -*-

# from PIL import Image
from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user

from app.dao.product_dao import ProductOrderDao
from . import member

__author__ = 'Sheldon Chen'






@member.route('/index')
@login_required
def index():
    return redirect(url_for('member.course_learning'))




@member.route('/my/vips')
@login_required
def vips():

    orders =ProductOrderDao().find_user_vip_order(current_user.id)
    return render_template('member/vips.html',orders=orders)






@member.route('/social_account.html')
@login_required
def social_account():
    return render_template('member/social_account.html')


