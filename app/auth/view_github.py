# -*- coding: UTF-8 -*-
import json

from flask import request, url_for, session, redirect, render_template
from flask.ext.login import login_user

from app.auth.util import create_social_user, is_bind_account
from . import auth
from .. oauth_social_login import github

__author__ = 'Ivan'






@auth.route('/github/login')
def github_login():
    return github.authorize(callback=url_for('auth.github_authorized', _external=True))





@auth.route('/github/login/authorized')
def github_authorized():

    resp = github.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )


    if resp.has_key('access_token')==False:

        #没有获取到 token ,重新获取
        return github.authorize(callback=url_for('auth.github_authorized', _external=True))



    session['oauth_token'] = (resp['access_token'], '')

    access_token = resp['access_token']
    session['access_token'] = access_token
    session['expires_in'] = 7776000

    response = github.get('user')

    if isinstance(response.data,dict):
        github_user = response.data

    else:
        github_user =json.loads(response.data)


    session['openid'] = github_user['id']


     #判断用户是否已经绑定
    user = is_bind_account(github_user['id'],access_token,7776000)

    if user is not None:
        login_user(user, True)
        return redirect(url_for('main.index'))





    social_user=create_social_user(github_user['login'],
                                       github_user['avatar_url'],
                                       'github',
                                       1)

    return render_template('auth/social-login-select.html',social_user = social_user)




@github.tokengetter
def get_github_oauth_token():
    oauth_token= session.get('oauth_token')
    return oauth_token


