# -*- coding: UTF-8 -*-
import os
from flask.ext.oauthlib.client import OAuth

__author__ = 'Ivan'


QQ_APP_ID = os.environ.get('QQ_APP_ID')
QQ_APP_KEY = os.environ.get('QQ_APP_KEY')


WEIBO_APP_ID = os.environ.get('WEIBO_APP_ID')
WEIBO_APP_SECRET = os.environ.get('WEIBO_APP_SECRET')


GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITUB_APP_SECRET = os.environ.get('GITUB_APP_SECRET')


WECHAT_APP_ID = os.environ.get('WECHAT_APP_ID')
WECHAT_APP_SECRET = os.environ.get('WECHAT_APP_SECRET')




oauth = OAuth()

qq = oauth.remote_app(
    'qq',
    consumer_key=QQ_APP_ID,
    consumer_secret=QQ_APP_KEY,
    base_url='https://graph.qq.com',
    request_token_url=None,
    request_token_params={'scope': 'get_user_info'},
    access_token_url='/oauth2.0/token',
    authorize_url='/oauth2.0/authorize',
)


weibo = oauth.remote_app(
    'weibo',
    consumer_key=WEIBO_APP_ID,
    consumer_secret=WEIBO_APP_SECRET,
    request_token_params={'scope': 'email,statuses_to_me_read'},
    base_url='https://api.weibo.com/2/',
    authorize_url='https://api.weibo.com/oauth2/authorize',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.weibo.com/oauth2/access_token',
    # since weibo's response is a shit, we need to force parse the content
    content_type='application/json',
)



github = oauth.remote_app(
    'github',
    consumer_key=GITHUB_APP_ID,
    consumer_secret=GITUB_APP_SECRET,
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


wechat = oauth.remote_app(
    'wechat',
    consumer_key=WECHAT_APP_ID,
    consumer_secret=WECHAT_APP_SECRET,
    request_token_params={'scope': 'snsapi_login','appid':WECHAT_APP_ID},
    access_token_params={'appid':WECHAT_APP_ID,'secret':WECHAT_APP_SECRET},
    base_url='',
    request_token_url=None,
    access_token_url="https://api.weixin.qq.com/sns/oauth2/access_token",
    authorize_url="https://open.weixin.qq.com/connect/qrconnect"


)