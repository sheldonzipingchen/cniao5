# -*- coding: UTF-8 -*-
import json

import requests
from flask import jsonify, request, url_for, session,redirect, render_template
from flask.ext.login import login_user

from app.auth.util import is_bind_account, create_social_user
from app.oauth_social_login import  wechat, WECHAT_APP_ID, WECHAT_APP_SECRET
from . import passport

__author__ = 'Ivan'







@passport.route('/wechat/authorized')
def wechat_authorized():

    code = request.args.get("code")


    access_token_url ='https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(WECHAT_APP_ID,WECHAT_APP_SECRET,code)

    response = requests.get(access_token_url)

    if response.status_code!=200:
        return wechat.authorize(callback=url_for('passport.wechat_authorized',_external=True))




    token_info = json.loads(str(response.text))


    if token_info.get('errcode')!=None:
       return wechat.authorize(callback=url_for('passport.wechat_authorized',_external=True))

    access_token = token_info.get('access_token')
    expires_in = token_info['expires_in']
    open_id = token_info['unionid']
    wechat_open_id =token_info['openid']




    session['access_token'] = access_token
    session['expires_in'] = expires_in
    session['openid'] = open_id


        #判断用户是否已经绑定
    user = is_bind_account(open_id,access_token,expires_in)

    if user is not None:
        login_user(user, True)
        return redirect(url_for('main.index'))


    user_info_url="https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s"%(access_token,wechat_open_id)
    response = requests.get(user_info_url)

    wechat_user = json.loads(response.text)



    social_user=create_social_user(wechat_user['nickname'],
                                       wechat_user['headimgurl'],
                                       'wechat',
                                       wechat_user['sex'])

    return render_template('auth/social-login-select.html',social_user = social_user)




