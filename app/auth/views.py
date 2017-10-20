# -*- coding: UTF-8 -*-
import StringIO
from datetime import datetime

from flask import current_app, flash, redirect, render_template, request, url_for, session, jsonify, make_response
from flask.ext.login import login_user, login_required, logout_user, user_logged_in
from werkzeug.security import generate_password_hash, check_password_hash

from app.util.session_helper import set_user_online, set_user_offline
from app.util.str_util import random_code, create_uuid
from forms import LoginForm
from . import auth
from .. dao.phone_message_dao import PhoneMessageDao
from .. dao.user_dao import UserDao, UserMessageDao, SocialUserDao, InviteRecordDao
from .. models import User, UserMsg, SocialUser, InviteRecord
from .. util.data_validate_util import DataValidate
from .. util.email_message import send_code_for_find_pwd
from .. util.mobile_message import send_code_for_reg_use_mobile, send_message_for_find_pwd_use_mobile, \
    send_message_for_invite_success_without_vip
from ..validations import create_validate_code

__author__ = 'Sheldon Chen'

ONE_DAY = 86400




################### 注册 ###########################################

""" 注册 """
@auth.route('/reg.html', methods=['GET'])
def reg():
    """ 注册页面 """

    import time
    code = random_code(time.time(),20);
    reg_hash_code = generate_password_hash(code)

    reps = make_response(render_template('auth/reg.html'))
    reps.set_cookie(key='reg_hash_code', value=reg_hash_code, expires=time.time()+10*60) # 10分钟有有效期
    session['reg_hash']=code;
    return reps


"""  保存注册信息 """
@auth.route('/reg/save', methods=['POST'])
def reg_save():


    reg_hash_code = request.cookies.get('reg_hash_code')

    if reg_hash_code is None or reg_hash_code == '':
        return jsonify(success=False, message="校验失败，请刷新页面重试")


    reg_hash = session.get('reg_hash')

    if reg_hash is None or reg_hash == '':
        return jsonify(success=False, message="校验失败，请刷新页面重试")

    if check_password_hash(reg_hash_code.encode('utf-8'), reg_hash)==False:
         return jsonify(success=False, message="认证失败")

    form = request.json
    mobi = form.get('mobi')
    password=form.get('password')
    username = form.get('username')
    reg_type = form.get('regtype') # 注册类型, social:通过第三方平台注册,direct:直接注册,invite:邀请注册  ,如为空默认为直接注册

    if mobi is None or mobi == '':
        return jsonify(success=False, message="请填写手机号")

    if username is None or username == '':
        return jsonify(success=False, message="请填写用户名")

    user_dao=UserDao();
    user = user_dao.find_by_mobi_confirmed(mobi)

    if user is not None:
        return jsonify(success=False, message="该用户已经存在")

    user = user_dao.find_by_username(username)
    if user is not None:
        return jsonify(success=False, message="该用户名已经被使用")

    channel = ''
    if 'channel' in session:
        channel = session['channel']
        current_app.logger.debug('arg s: %s' % (channel, ))


    logo_url=None
    if reg_type=='social':
        logo_url= session['socail_user_head_url']


    user_dao = UserDao()

    user = User( unique_code=create_uuid(),
                 mobi=mobi,
                 mobile_confirmed=True,
                 confirmed=True,
                 username=username,
                 password=password,
                 pwd=password,
                 channel=channel,
                 logo_url=logo_url,
                 reg_time=datetime.now())

    user_dao.save(user)


    if reg_type=='social':

        social_user =SocialUser(user_id=user.id,
                                open_id=session['openid'],
                                type=channel,
                                access_token= session['access_token'],
                                expire_in=session['expires_in'],
                                nickname=username,
                                head_url=logo_url,
                                gender=session['socail_user_gender'],
                                status=1)


        SocialUserDao().save(social_user)

    login_user(user, True)

    if channel !='' and channel !=0:

        try:

            invite_user = user_dao.get_by_code(channel)
            if invite_user is not None:
                  #  赠送鸟币
                invite_user.coin = invite_user.coin+1
                user_dao.save(invite_user)
                send_message_for_invite_success_without_vip(invite_user.mobi,1)

                invite_record = InviteRecord(inviter_id=invite_user.id,
                                 register_id = user.id,
                                 reg_time=datetime.now(),
                                 channel=channel,
                                 coin=1,
                                 vip_days=0)

                InviteRecordDao().save(invite_record)
        except:
            pass



    # user_msg = UserMsg(title=u'注册成功',
    #                msg=u'Hello, 我是菜鸟窝CEO，大家都叫我Ivan :) 欢迎你的到来，成为万千菜鸟中的一员。 '
    #                    u'这里是一个有趣的学习平台,希望我们一起进步。 有任何使用问题可以随时来找我',
    #                from_user_id=1,
    #                to_user_id=user.id,
    #                is_read=0
    #                )
    #
    # UserMessageDao().save(user_msg)

    return jsonify(success=True, message="注册成功！")





@auth.route('/reg/smscode')
def send_sms_code_for_reg():

    reg_hash_code = request.cookies.get('reg_hash_code')

    if reg_hash_code is None or reg_hash_code == '':
        return jsonify(success=False, message="校验失败，请刷新页面重试")



    reg_hash = session.get('reg_hash')

    if reg_hash is None or reg_hash == '':
        return jsonify(success=False, message="校验失败，请刷新页面重试")

    if check_password_hash(reg_hash_code.encode('utf-8'), reg_hash)==False:
         return jsonify(success=False, message="认证失败")


    phone=request.args.get('phone')
    if phone is None:
        return jsonify(success=False, message="请填写手机号")


    user = UserDao().find_by_mobi_confirmed(phone)
    if user is  None:
        send_code_for_reg_use_mobile(phone)

        # if session.get('reg_hash') is not None:
        #     session.pop('reg_hash', None)

        return jsonify(success=True, message="success")

    else:
        return jsonify(success=False, message="手机号已被使用")







####################### 登录 ###############################


@auth.route('/login.html', methods=['GET', 'POST'])
def login():
    """ 登录页面 """
    next_url = request.args.get('next')
    form = LoginForm(remember_me=True, next_url=next_url)
    if form.validate_on_submit():

        userDao = UserDao()
        user = userDao.find_by_email_phone(form.email.data)
        if user is not None and user.verify_password(form.password.data):

            set_user_offline(user.id) #判断该用户有没有在其他地方登录,如果有,挤下线
            login_user(user, form.remember_me.data) #保持登录用户到session
            set_user_online(user.id,session.sid) #设置用户为登录状态

            return redirect(form.next_url.data or url_for('main.index'))

        current_app.logger.debug('login fail')
        flash(u'用户名或者密码错误', 'error_message')

    return render_template('auth/login.html', form=form)




@auth.route('/logout')
@login_required
def logout():
    """ 用户退出 """
    logout_user()
    flash(u'你已退出')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    return  render_template("auth/unconfirmed.html")



################## 找回密码 #########################

@auth.route("/password/find.html")
def find_password():
    return render_template("/auth/find_password.html")

@auth.route("/password/find_next.html",methods=['POST'])
def find_password_step2():

    email_or_mobi = request.form.get('email_phone');

    isEmail =DataValidate().isEmail(email_or_mobi);

    return render_template("/auth/find_password_step2.html",
                           email_or_mobi=email_or_mobi,
                           isEmail=isEmail
                        )



@auth.route("/password/find_last.html",methods=['POST'])
def find_password_step_last():
    email_or_mobi = request.form.get('email_phone');
    return  render_template("/auth/find_password_step3.html",email_or_mobi=email_or_mobi,)


@auth.route("/password/find/code/email/send",methods=['POST'])
def send_code_for_find_pwd_use_email():


    data=request.get_json().get('value')

    if(data is None or data==''):
        return jsonify(success=0,message='邮箱地址为空')


    if DataValidate().isEmail(data):
        send_code_for_find_pwd(data)
        return jsonify(success=1,message='验证码已发送到邮箱')





@auth.route('/password/find/code/email/check')
def send_code_for_find_pwd_use_email_check():
    value = request.args.get('value')
    email = request.args.get('email')


    phone_message = PhoneMessageDao().getEmailMessage_from_findPassword(email,value)

    if phone_message is not None:
        min = ((datetime.now() - phone_message.send_time).seconds) / 60
        if min > 10:  #10分钟过期
            return jsonify({"success":False, "message": "验证码过期！"})
        return jsonify({"success":True, "message":"验证通过"})
    else:
        return jsonify({"success":False, "message": "验证码错误！"})




@auth.route("/password/find/code/mobi/send",methods=['POST'])
def send_code_for_find_pwd_use_mobile():

    mobile=request.get_json().get('value')

    mobile=str(mobile)

    if mobile is None or mobile == '':
        return jsonify(success=0,message='手机号为空')


    if DataValidate().isMobile(mobile):

        phone_msgs= PhoneMessageDao().findPhoneMessages_by_phone_use_for_find_pwd(mobile)

        if len(phone_msgs) > 5:
            return jsonify(success=0,message='本号码多次获取验证码，请明天再试')


        send_message_for_find_pwd_use_mobile(mobile)# 发送短信
        return jsonify(success=1,message='验证码已发送到手机')

    else:
        return jsonify(success=0,message='手机号码格式错误')


@auth.route('/password/find/code/mobil/check')
def code_for_find_pwd_use_mobile_check():

    value = request.args.get('value')
    mobile = request.args.get('mobile')


    phone_message = PhoneMessageDao().getPhoneMessage_use_for_find_pwd(mobile,value)

    if phone_message is not None:
        min = ((datetime.now() - phone_message.send_time).seconds) / 60
        if min > 10:  #10分钟过期
            return jsonify({"success":False, "message": "验证码过期！"})
        return jsonify({"success":True, "message":"验证通过"})
    else:
        return jsonify({"success":False, "message": "验证码错误！"})




@auth.route('/password/find/reset',methods=['POST'])
def password_reset_for_find_pwd():

    json_obj = request.get_json();

    pwd = json_obj.get('password')
    email_or_mobile = json_obj.get('email_phone')

    userDao = UserDao()
    user = userDao.find_by_email_phone(email_or_mobile)
    if user is None:
        return jsonify(success=0,message='用户不存在')
    else:

        user.password = pwd
        user.pwd=pwd
        userDao.save(user)

        return jsonify(success=1,message='重设密码成功')








##################################################################################################################





@auth.route('/code')
def get_code():
    """ 生成验证码图片 """
    # 保存 strs 参数
    code_img, strs = create_validate_code()
    buf = StringIO.StringIO()
    code_img.save(buf, 'JPEG', quality=70)

    buf_str = buf.getvalue()
    response = current_app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    response.set_cookie('validate_code', value='', max_age=1800)
    response.set_cookie('validate_code', value=strs, max_age=1800)
    return response



@auth.route('/reg/sms_check', methods=['GET', 'POST'])
def check_sms():
    # data = request.get_json()
    phone = request.form.get('phone')
    code = request.form.get('code')
    use_for = 'reg'

    phone_message = PhoneMessageDao().getPhoneMessage(phone,use_for,code)

    if phone_message is not None:
        min = ((datetime.now() - phone_message.send_time).seconds) / 60
        if min > 10:  #10分钟过期
            return jsonify(success=False, message= u"验证码过期！")
        return jsonify(success=True, message= u"success")
    else:
        return jsonify(success=False, message= u"验证码错误！")


# 判断用户名是否被使用
@auth.route('/reg/nickname/check')
def check_username():
    username = request.args.get('value')
    user = UserDao().find_by_username(username)

    if username is None or username == '':
        return jsonify({'success': False, 'message': '用户名不能为空'})

    if user is None:
        result = {'success': True, 'message': '该用户名可以使用'}

    else:
        result = {'success': False, 'message': '用户名已存在'}

    return jsonify(result);


@auth.route('/reg/mobile/check')
@auth.route("/mobile/exist/check")
def check_mobile_exist():
    value = request.args.get('value')

    if (value is None or value == ''):
        result = {'success': False, 'message': '手机号码不能为空'}
        return jsonify(result)

    isMobi =DataValidate().isMobile(value)
    if (isMobi==False):
        result = {'success': False, 'message': '请输入正确的手机号码'}
        return jsonify(result)

    userDao = UserDao();
    user = userDao.find_by_mobi(value);

    if user is None:
        result = {'success': True, 'message': '该手机号码可以使用'}

    else:
        result = {'success': False, 'message': '该手机号已经被使用'}

    return jsonify(result)



# 判断邮箱或者手机存在
@auth.route("/email_mobile/exist/check")
def check_email_or_mobi_exist():
    value = request.args.get('value')
    result = None;

    if (value is None or value == ''):
        result = {'success': False, 'message': '手机号/邮箱不能为空'}
        return jsonify(result)

    validator = DataValidate()

    isMobi_Email =validator.isEmailOrMobile(value)

    if isMobi_Email==False:
        result = {'success': False, 'message': '手机号/邮箱格式错误'}
        return jsonify(result)


    userDao = UserDao();
    user = userDao.find_by_email_phone(value);

    if user is None:
        result = {'success': True, 'message': '该手机号/邮箱可以使用'}

    else:
        result = {'success': False, 'message': '该手机号/邮箱已经被使用'}

    return jsonify(result)



# 判断邮箱或者手机不存在
@auth.route("/email_mobile/not_exist/check")
def check_email_or_mobi_not_exist():
    value = request.args.get('value')

    if (value is None or value == ''):
        result = {'success': False, 'message': '手机号/邮箱不能为空'}
        return jsonify(result)

    validator = DataValidate()

    isMobi_Email =validator.isEmailOrMobile(value)

    if isMobi_Email==False:
        result = {'success': False, 'message': '手机号/邮箱格式错误'}
        return jsonify(result)


    userDao = UserDao();
    user = userDao.find_by_email_phone(value);

    if user is None:
        result = {'success': False, 'message': '该用户不存在'}

    else:
        result = {'success': True, 'message': '该用户存在'}

    return jsonify(result)



@auth.route('/validate_code/check')
def validate_code_check():

    value = request.args.get('value')
    code = request.cookies.get('validate_code')

    if code==value:
        result = {'success': True, 'message': '验证通过'}

    else:
        result = {'success': False, 'message': '验证码输入错误'}


    return jsonify(result)




# @user_logged_in.connect_via(app)
# def user_logged_in(sender,user):
#     print "login---------"
#     print user