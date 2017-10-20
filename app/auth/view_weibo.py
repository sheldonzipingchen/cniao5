# -*- coding: UTF-8 -*-

from flask import redirect, render_template, request, url_for, json, session
from flask.ext.login import login_user

from app.auth.util import is_bind_account, create_social_user
from . import auth
from .. oauth_social_login import weibo

__author__ = 'Ivan'




@auth.route('/weibo/login')
def weibo_login():

    return weibo.authorize(callback=url_for('auth.weibo_authorized',_external=True))



@auth.route('/weibo/login/authorized')
def weibo_authorized():

    resp = weibo.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )


    if str(resp) =='Invalid response from weibo' or resp.has_key('access_token')==False:

        #没有获取到 token ,重新获取
        return weibo.authorize(callback=url_for('auth.weibo_authorized', _external=True))


    #{u'access_token': u'2.00NLI4eFaLffaEb917623f97J6DgQC', u'remind_in': u'157679999', u'expires_in': 157679999, u'uid': u'5177230591'}


    session['oauth_token'] = (resp['access_token'], '')

    access_token = resp['access_token']
    expires_in = resp['expires_in']
    open_id = resp['uid']

    session['access_token'] = access_token
    session['expires_in'] = expires_in
    session['openid'] = open_id





    #判断用户是否已经绑定
    user = is_bind_account(resp['uid'],access_token,expires_in)

    if user is not None:
        login_user(user, True)
        return redirect(url_for('main.index'))


    response = weibo.get('/users/show.json',{'access_token':access_token,'uid': open_id})


    if isinstance(response.data,dict):
        weibo_user = response.data

    else:
        weibo_user =json.loads(response.data)


    social_user=create_social_user(weibo_user['name'],
                                       weibo_user['avatar_large'],
                                       'weibo',
                                       weibo_user['gender'])

    return render_template('auth/social-login-select.html',social_user = social_user)



@weibo.tokengetter
def get_weibo_oauth_token():
    token= session.get('oauth_token')
    return token


