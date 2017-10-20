# -*- coding: UTF-8 -*-
from datetime import datetime
from flask import render_template, jsonify, request
from flask.ext.login import login_required, current_user, login_user

from . import member
from app.dao.phone_message_dao import PhoneMessageDao
from app.dao.user_dao import UserDao
from app.util.data_validate_util import DataValidate
from app.util.email_message import send_code_for_find_email
from app.util.mobile_message import send_code_for_bind_mobile


__author__ = 'Ivan'




@member.route('/setting/profile')
@login_required
def setting_info():

    user = UserDao().get(current_user.id)
    return render_template('member/setting/profile.html',user=user)


@member.route("/setting/profile/update",methods=['POST'])
@login_required
def update_profile():

    try:
        profile =request.get_json()

        real_name = profile.get('real_name')
        addr = profile.get('addr')
        qq = profile.get('qq')
        company = profile.get('company')
        job = profile.get('job')
        work_year = profile.get('work_year')
        about_me = profile.get('about_me')


        dao =UserDao()
        user = dao.get(current_user.id)
        user.real_name=real_name
        user.addr=addr
        user.qq=qq
        user.company=company
        user.job=job
        user.work_years=work_year
        user.desc=about_me

        dao.save(user)


        return jsonify(success=True)
    except:
        return jsonify(success=False)





@member.route("/setting/profile/modify",methods=['POST'])
@login_required
def profile_modify():

    params = request.get_json();
    action = params.get("action")
    val = params.get("val");

    user_dao = UserDao();
    user = user_dao.get(current_user.id);

    if action == 'username':

        temp_user = user_dao.find_by_username(val)
        if temp_user is not None:
            return jsonify(success=0,message=u'该用户名已经被使用')

        user.username=val


    user_dao.save(user);

    return jsonify(success=1,message=u'修改成功')




@member.route('/setting/avatar')
@login_required
def setting_avatar():
    user = UserDao().get(current_user.id)
    return  render_template('member/setting/avatar.html',user=user)





@member.route('/setting/avatar/save',methods=['POST'])
@login_required
def setting_avatar_save():

    logo_url = request.get_json().get('logo_url')
    user = UserDao().get(current_user.id)

    user.logo_url = logo_url
    UserDao().save(user)

    login_user(user, user)
    return jsonify(success=True,message='success')



@member.route('/setting/avatar/crop')
@login_required
def setting_avatar_crop():
     user = UserDao().get(current_user.id)
     return render_template('member/setting/avatar-crop.html',user=user)








@member.route('/setting/pwd')
@login_required
def setting_pwd():
    return render_template('member/setting/pwd.html')




@member.route('/setting/pwd/update',methods=['POST'])
@login_required
def update_pwd():

    pwds =request.get_json()

    old_pwd = pwds.get('old_pwd')
    new_pwd = pwds.get('new_pwd')


    dao =UserDao()
    user = dao.get(current_user.id)

    if user.verify_password(old_pwd)==False:
        return jsonify(success=False,message=u'原密码输入错误')


    user.password = new_pwd
    user.pwd=new_pwd
    dao.save(user)

    return jsonify(success=True,message=u'success')



@member.route('/setting/profile/mobile/bind',methods=['POST'])
@login_required
def profile_bind_mobile():
    mobile = request.form.get('mobi')
    if mobile is None:
        return jsonify(success=False, message="请填写手机号")

    user_dao = UserDao()
    user = user_dao.get(current_user.id)

    user.mobi=mobile
    user.mobile_confirmed=True

    user_dao.save(user)

    return jsonify(success=True, message=u"success")






@member.route('/setting/profile/mobile/bind/send/smscode')
@login_required
def profile_send_bind_mobile_sms_code():

    phone=request.args.get('phone')
    if phone is None:
        return jsonify(success=False, message="请填写手机号")


    user = UserDao().find_by_mobi_confirmed(phone)
    if user is None:
        send_code_for_bind_mobile(phone)
        return jsonify(success=True, message="success")

    return jsonify(success=False, message="手机号已被使用")




@member.route('/setting/profile/mobile/bind/smscode/check',methods=['POST'])
@login_required
def profile_bind_mobile_code_check():

    phone = request.form.get('phone')
    code = request.form.get('code')
    use_for = 'bind_mobile'

    phone_message = PhoneMessageDao().getPhoneMessage(phone,use_for,code)

    if phone_message is not None:
        min = ((datetime.now() - phone_message.send_time).seconds) / 60
        if min > 10:  #10分钟过期
            return jsonify(success=False, message= u"验证码过期！")
        return jsonify(success=True, message= u"success")
    else:
        return jsonify(success=False, message= u"验证码错误！")








@member.route('/setting/profile/email/bind',methods=['POST'])
@login_required
def profile_bind_email():
    email = request.form.get('email')
    if email is None:
        return jsonify(success=False, message="请填写email")


    if  DataValidate().isEmail(email) ==False:

        return jsonify(success=False, message="email格式不正确")


    user_dao = UserDao()
    user = user_dao.get(current_user.id)

    user.email=email
    user_dao.save(user)

    return jsonify(success=True, message=u"success")



@member.route('/setting/profile/email/bind/send/code')
@login_required
def profile_send_bind_email_code():
    data=request.args.get('email')

    if(data is None or data==''):
        return jsonify(success=0,message='邮箱地址为空')


    if DataValidate().isEmail(data):
        send_code_for_find_email(data)
        return jsonify(success=1,message='验证码已发送到邮箱')



@member.route('/setting/profile/email/bind/code/check',methods=['POST'])
@login_required
def profile_bind_email_code_check():
    code = request.form.get('code')
    email = request.form.get('email')


    phone_message = PhoneMessageDao().getEmailMessage_from_bind_email(email,code)

    if phone_message is not None:
        min = ((datetime.now() - phone_message.send_time).seconds) / 60
        if min > 10:  #10分钟过期
            return jsonify({"success":False, "message": "验证码过期！"})
        return jsonify({"success":True, "message":"验证通过"})
    else:
        return jsonify({"success":False, "message": "验证码错误！"})






@member.route('/setting/profile/alipay/bind',methods=['POST'])
@login_required
def profile_alipay_bind():

    alipay = request.get_json().get("alipay")
    if alipay is None or alipay=='':
        return jsonify(success=False,message='账户为空')

    user_dao =UserDao();
    user = user_dao.get(current_user.id)

    user.alipay = alipay

    user_dao.save(user)
    return jsonify(success=True,message='success')
