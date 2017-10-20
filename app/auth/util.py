# -*- coding: UTF-8 -*-
from flask import session

from app.dao.user_dao import SocialUserDao, UserDao
from app.models import SociaUserModel


def is_bind_account(open_id,access_token,expire_in):

     social_user_dao = SocialUserDao()
     social_user = social_user_dao.get_by_open_id(open_id)

     if social_user is not None:

        #更新token 和到期时间
        social_user.access_token = access_token
        social_user.expire_in = expire_in

        social_user_dao.save(social_user)

        user = UserDao().get(social_user.user_id)
        if user is not None:

           save_login_record(user)
           return  user

     return  None




def save_login_record(user):
    pass




def create_social_user(nickname,head_url,channel,gender):

    social_user = SociaUserModel(nickname=nickname,
                                     head_url=head_url,
                                     channel=channel,
                                     gender=gender)

    session['socail_user_nickname']=social_user.nickname
    session['socail_user_head_url']=social_user.head_url
    session['channel']=social_user.channel
    session['socail_user_gender']=social_user.gender


    return social_user