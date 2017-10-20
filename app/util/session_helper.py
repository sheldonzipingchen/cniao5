# -*- coding: UTF-8 -*-
from datetime import timedelta

from app import redis, session_lifetime

USER_LOGIN_KEY_PREFIX='user-login:'
SESSION_KEY_PREFIX="session:"

#用户登录成功后调用该方法保存sessionId
def set_user_online(user_id,session_id):

    user_key = USER_LOGIN_KEY_PREFIX+ str(user_id)
    redis.setex(name=user_key,value=session_id,time=total_seconds(timedelta(seconds=session_lifetime)))



def get_user_session_id(user_id):

    session_id = redis.get(USER_LOGIN_KEY_PREFIX+ str(user_id))
    return session_id





#在用户登录之前先调用该方法判断此用户有没有登录
def set_user_offline(user_id):

    try:
        session_id = get_user_session_id(user_id)

        if session_id is None:
            return

        user_session =  redis.get(SESSION_KEY_PREFIX+session_id)

        if 'user_id' in user_session:

            redis.delete(SESSION_KEY_PREFIX+session_id)
            redis.delete(USER_LOGIN_KEY_PREFIX+ str(user_id))
    except:
        pass



def total_seconds(td):
    return td.days * 60 * 60 * 24 + td.seconds