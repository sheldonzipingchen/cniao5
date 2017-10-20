# -*- coding: UTF-8 -*-
from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from app import User
from . import api
from .errors import forbidden, unauthorized


__author__ = 'Ivan'


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):

    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user or not user.verify_password(password):
        return False
    g.current_user = user
    g.token_used = False
    return True


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# @api.before_request
# @auth.login_required
# def before_request():
#     if not g.current_user.is_anonymous() and \
#             not g.current_user.confirmed:
#         return forbidden('Unconfirmed account')


@api.route('/token')
def get_token():
    if g.current_user.is_anonymous() or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})





