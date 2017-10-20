# -*- coding: UTF-8 -*-
import uuid

from flask import redirect, request, render_template, url_for, Response, jsonify
from flask.ext.login import login_required
from flask.ext.restful import abort
from app.common import common
from app.dao.user_dao import UserDao
from app.storage import q


__author__ = 'Ivan'


@common.route('/qn/upload/token/<string:bucket>')
def get_qiniu_upload_token(bucket):
    token = q.upload_token(bucket)
    return jsonify(uptoken=token)



@common.route('/file/key')
def build_file_key():
    key_name = '%s' % (uuid.uuid1())

    return jsonify(result=key_name)



@common.route('/user/<int:id>/profile/complete/check')
def check_user_profile_complete(id):

    user_dao = UserDao()

    user = user_dao.get(id)

    if user is None:
        return jsonify(result=False,message=u'用户不存在')


    is_email_full = True
    if user.email is None or user.email=='':
        is_email_full=False


    is_head_logo_full = True
    if user.logo_url is None or user.logo_url=='':
        is_head_logo_full=False

    is_mobi_full = True
    if user.mobi is None or user.mobi=='':
        is_mobi_full=False

    is_qq_full = True
    if user.qq is None or user.qq=='':
        is_qq_full=False

    is_username_full = True
    if user.username is None or user.username=='':
        is_username_full=False



    return jsonify(result=True,message=u'success',
                   email=is_email_full,
                   mobi = is_mobi_full,
                   head=is_head_logo_full,
                   qq=is_qq_full,
                   username=is_username_full)


@common.route('/tool/image/upload')
def imgage_upload():
    return  render_template('common/image-upload.html')