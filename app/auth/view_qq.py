# -*- coding: UTF-8 -*-
import os

from flask import redirect, render_template, request, url_for, json, session, jsonify, make_response
from flask.ext.login import login_user
from werkzeug.security import generate_password_hash

from app.auth.util import is_bind_account, create_social_user
from app.dao.user_dao import SocialUserDao, UserDao
from app.util.str_util import random_code
from . import auth
from .. models import SocialUser
from .. oauth_social_login import qq

__author__ = 'Ivan'





QQ_APP_ID = os.environ.get('QQ_APP_ID')
QQ_APP_KEY = os.environ.get('QQ_APP_KEY')


def json_to_dict(x):
    '''OAuthResponse class can't not parse the JSON data with content-type
    text/html, so we need reload the JSON data manually'''
    if x.find('callback') > -1:
        pos_lb = x.find('{')
        pos_rb = x.find('}')
        x = x[pos_lb:pos_rb + 1]
    try:
        return json.loads(x, encoding='utf-8')
    except:
        return x




@auth.route('/qq/login')
def qq_login():
    return qq.authorize(callback=url_for('auth.qq_authorized', _external=True))


@auth.route('/qq/login/authorized')
def qq_authorized():

    resp = qq.authorized_response()

    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )

    if resp.has_key('access_token')==False:

        #没有获取到 token ,重新获取
        return qq.authorize(callback=url_for('auth.qq_authorized', _external=True))


    session['oauth_token'] = (resp['access_token'], '')
    access_token = resp['access_token']
    expires_in = resp['expires_in']

    session['access_token'] = access_token
    session['expires_in'] = expires_in

    # Get openid via access_token, openid and access_token are needed for API calls

    resp = qq.get('/oauth2.0/me',{'access_token': access_token})


    resp = json_to_dict(resp.data)
    if isinstance(resp, dict):

        open_id = resp.get('openid')
        session['openid'] = open_id


        response = qq.get('/user/get_user_info',
                          data={
        'openid': open_id,
        'access_token': access_token,
        'oauth_consumer_key': QQ_APP_ID,
    })


        #判断用户是否已经绑定
        user = is_bind_account(open_id,access_token,expires_in)


        if user is not None:
            login_user(user, True)
            return redirect(url_for('main.index'))


        qq_user_info = json.loads(response.data)


        social_user=create_social_user(qq_user_info['nickname'],
                                       qq_user_info['figureurl_qq_2'],
                                       'qq',
                                       qq_user_info['gender'])

        return render_template('auth/social-login-select.html',social_user = social_user)

    return qq.authorize(callback=url_for('auth.qq_authorized', _external=True))




@qq.tokengetter
def get_qq_oauth_token():

    return session.get("oauth_token")





@auth.route('/social/account/create')
def social_account_create():

    try:
        head_url = session['socail_user_head_url']
    except:
        head_url='http://cniao5.com/static/images/default_head.jpeg'
    nickname=session['socail_user_nickname']


    import time
    code = random_code(time.time(),20);
    reg_hash_code = generate_password_hash(code)

    reps = make_response(render_template("auth/social-account-create.html",head_url=head_url,nickname=nickname))
    reps.set_cookie(key='reg_hash_code', value=reg_hash_code, expires=time.time()+10*60) # 10分钟有有效期
    session['reg_hash']=code;

    return reps




@auth.route('/social/account/band')
def social_account_bind():
    try:
        head_url = session['socail_user_head_url']
    except:
        head_url='http://cniao5.com/static/images/default_head.jpeg'
    return render_template("auth/social-account-bind.html",head_url=head_url)


@auth.route('/user/social/account/band',methods=["POST"])
def user_social_account_bind():

    params = request.json
    mobi = params.get('mobi')
    password=params.get('password')


    userDao = UserDao()
    user = userDao.find_by_email_phone(mobi)

    if user is None:
        return jsonify(success=False,message=u'该用户不存在')

    if user.verify_password(password) == False:

        return jsonify(success=False,message=u'密码错误')



    if user.username==None or user.username=='':
        user.username =session['socail_user_nickname'];

    if user.logo_url==None or user.logo_url=='':
        user.logo_url =session['socail_user_head_url'];


    userDao.save(user)

    social_user =SocialUser(user_id=user.id,
                                open_id=session['openid'],
                                type=session['channel'],
                                access_token= session['access_token'],
                                expire_in=session['expires_in'],
                                nickname=session['socail_user_nickname'],
                                head_url=session['socail_user_head_url'],
                                gender=session['socail_user_gender'],
                                status=1)


    SocialUserDao().save(social_user)

    login_user(user,False)

    return jsonify(success=True,message=u'绑定成功')