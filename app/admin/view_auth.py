# -*- coding: UTF-8 -*-
from flask import render_template, request,redirect, url_for, flash, jsonify
from flask.ext.login import current_user, logout_user, login_user

from app.dao.user_dao import UserDao
from . import admin

__author__ = 'Ivan'



@admin.before_request
def before_request():
    if request.endpoint != 'admin.login' and request.endpoint !='admin.admin_login':
        if current_user.is_authenticated()==False :
            return redirect(url_for('admin.login'))

        if current_user.is_super_admin() == False:
             return redirect(url_for('main.index'))



@admin.route('/login.html')
def login():
    if current_user.is_authenticated() and current_user.is_super_admin():
        return  redirect(url_for(".index"))

    return render_template('admin/login.html',)


@admin.route('/login',methods=["POST"])
def admin_login():
    json = request.get_json()
    account = json.get("account")
    pwd = json.get("password")
    user =UserDao().find_by_email_phone(account)

    if user is None:
        return jsonify(success=0,message=u'用户不存在')

    if user.verify_password(pwd) and user.is_super_admin():
        login_user(user, False)
        return jsonify(success=1,message='success')

    return jsonify(success=0,message=u'用户名或者密码错误')



@admin.route('/logout.html')
def logout():
    """
    管理员退出
    """
    logout_user()
    flash(u'你已退出')
    return redirect(url_for('admin.login'))
