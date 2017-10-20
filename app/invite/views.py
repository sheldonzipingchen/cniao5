# -*- coding: utf-8 -*-
import base64
import urlparse
import uuid
from datetime import datetime

from flask import render_template, url_for, make_response, session, request, jsonify
from flask.ext.login import current_user, login_user
from flask.ext.restful import abort
from werkzeug.security import generate_password_hash, check_password_hash

from app.dao.product_dao import ProductOrderDao
from app.dao.user_dao import UserDao, InviteRecordDao, UserMessageDao
from app.models import InviteRecord, UserMsg, User
from app.util.mobile_message import send_message_for_reg_by_invite, send_message_for_invite_success_with_vip, \
    send_message_for_invite_success_without_vip
from app.util.str_util import create_uinque_code, create_uuid, random_code
from . import invite

__author__ = 'Ivan'


@invite.route("/")
def index():


    user=None
    if current_user.is_authenticated(): #用户已登录

        user_dao = UserDao();
        user = user_dao.get(current_user.id)

        if user.unique_code is None or user.unique_code=='':
            user.unique_code = create_uuid()


    return  render_template("invite/index.html",user=user)



@invite.route("/user/<string:code>")
def invite_user(code):

    if code ==None or code=='':
        return abort(404)

    channel=request.args.get('channel');


    lens = len(code)
    lenx = lens - (lens % 4 if lens % 4 else 4)
    try:
        params = base64.decodestring(code[:lenx])
    except:
       pass


    if params is None or params == '':
         return abort(404)

    values = params.split('&')

    from_code=None

    for key_value in values:
        temp = key_value.split('=')
        key=temp[0]
        if key == 'from_code':
            from_code=temp[1]
        if key == 'channel' and channel ==None:
            channel = temp[1]


    user_dao = UserDao()
    user =user_dao.get_by_code(from_code)

    if user is None:
         return abort(404)



    import time
    code = random_code(time.time(),20);
    reg_hash_code = generate_password_hash(code)

    reps = make_response(render_template('invite/invite.html',user=user,channel=channel))
    reps.set_cookie(key='reg_hash_code', value=reg_hash_code, expires=time.time()+10*60) # 10分钟有有效期
    session['reg_hash']=code;

    return reps


@invite.route("/reg",methods=['POST'])
def reg():


    reg_hash_code = request.cookies.get('reg_hash_code')

    if reg_hash_code is None or reg_hash_code == '':
        return jsonify(success=False, message="校验失败，请刷新页面重试")


    reg_hash = session.get('reg_hash')

    if reg_hash is None or reg_hash == '':
        return jsonify(success=False, message="校验失败，请刷新页面重试")

    if check_password_hash(reg_hash_code.encode('utf-8'), reg_hash)==False:
         return jsonify(success=False, message="认证失败")



    json = request.get_json()

    mobi = json.get("mobi")
    password = json.get("password")
    from_code= json.get("from_code")
    channel = json.get("channel")


    user_dao = UserDao()

    user_check = UserDao().find_by_mobi_confirmed(mobi)

    if user_check is not None:
        return jsonify(success=False, message="该用户已经存在")



    invite_dao = InviteRecordDao()
    product_order_dao = ProductOrderDao()

    invite_user = user_dao.get_by_code(from_code)



    ######## 新用户  #########

    #step1 注册用户 和赠送会员
    user = User(
                unique_code=create_uuid(),
                mobi=mobi,
                mobile_confirmed=True,
                confirmed=True,
                password=password,
                pwd=password,
                channel=channel,
                inviter_id=invite_user.id,
                reg_time=datetime.now())
    user_dao.save(user)

    product_order_dao.add_vip_for_free(user.id,30)
    #发送通知

    user_msg = UserMsg(title=u'注册成功',
                   msg=u'Hello, 我是菜鸟窝CEO，大家都叫我Ivan :) 欢迎你的到来，成为万千菜鸟中的一员。 '
                       u'这里是一个有趣的学习平台,希望我们一起进步。 有任何使用问题可以随时来找我',
                   from_user_id=1,
                   to_user_id=user.id,
                   is_read=0
                   )
    UserMessageDao().save(user_msg)

    send_message_for_reg_by_invite(user.mobi,invite_user.username)





    ######## 邀请人  #########

    ##step2  赠送鸟币
    invite_user.coin = invite_user.coin+1
    user_dao.save(invite_user)



    #step3 赠送会员
    invite_list = invite_dao.find_user_invite_list(invite_user.id)

    if len(invite_list)>12 : # 送够12个月就不再赠送
        vip_days =0
        send_message_for_invite_success_without_vip(invite_user.mobi,1)

    else:
        vip_days=30
        product_order_dao.add_vip_for_free(invite_user.id,30)

        send_message_for_invite_success_with_vip(invite_user.mobi,1)



    #step4 新增邀请记录

    invite_record = InviteRecord(inviter_id=invite_user.id,
                                 register_id = user.id,
                                 reg_time=datetime.now(),
                                 channel=channel,
                                 coin=1,
                                 vip_days=vip_days)

    invite_dao.save(invite_record)



    login_user(user, True)


    return jsonify(success=True, message='注册成功')