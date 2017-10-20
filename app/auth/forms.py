# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError

from ..models import User


__author__ = 'Sheldon Chen'


class LoginForm(Form):
    """
    登录表单
    """
    email = StringField(u'邮箱', validators=[
        Required(message=u'邮箱或手机号不能为空')])
    #mobi = StringField(u'手机', validators=[
    #    Required(message=u'手机号不能为空')])
    password = PasswordField(u'密码', validators=[Required(message=u'密码不能为空')])
    remember_me = BooleanField(u'记住我')
    next_url =HiddenField()
    coupon =HiddenField()
    submit = SubmitField(u'立即登录')


class RegisterForm(Form):
    """
    注册表单
    """
      # Required(message=u'邮箱不能为空'),
      #  Length(1, 64, message=u'邮箱长度必须是在1到64位之间'),
      #  Email(message=u'不符合邮箱格式')])
    mobi = StringField(u'手机', validators=[
        Required(message=u'手机号不能为空')])
    code = StringField(u'验证码', validators=[
        Required(message=u'手机验证码不能为空！')])
    username = StringField(u'昵称', validators=[
        Required(message=u'昵称不能为空'),
        Length(1, 10, message=u'昵称长度必须是在1到10位之间')])
    password = PasswordField(u'密码', validators=[
        Required(message=u'密码不能为空'),
        Length(6, 20, message=u'密码必须是在6到20位之间')])
    coupon =HiddenField()
    submit = SubmitField(u'立即注册')

    # def validate_email(self, field):
    #     """
    #     校验邮箱是否已被注册
    #     :param field:
    #     :return:
    #     """
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError(u'该邮箱已被注册')
    def validate_mobi(self, field):
        """
        校验手机是否已被注册
        :param field:
        :return:
        """
        if User.query.filter_by(mobi=field.data, mobile_confirmed=True).first():
            raise ValidationError(u'该手机已被注册')

    def validate_username(self, field):
        """
        校验用户名是否已被注册
        :param field:
        :return:
        """
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册')


class ForgetPasswordForm(Form):
    """
    忘记密码表单
    """
    email = StringField(u'邮箱', validators=[
        Required(message=u'邮箱不能为空'),
        Length(1, 64, message=u'邮箱长度必须是在1到64位之间'),
        Email(message=u'不符合邮箱格式')])
    code = StringField(u'验证码', validators=[Required(message=u'验证码不能为空')])
    submit = SubmitField(u'找回密码')


class SicialRegForm(Form):
    """
    第三方登录注册表单
    """
    mobi = StringField(u'手机', validators=[
        Required(message=u'手机号不能为空')])
    username = StringField(u'昵称')
    password = PasswordField(u'密码', validators=[
        Required(message=u'密码不能为空'),
        Length(6, 20, message=u'密码必须是在6到20位之间')])

    social_uid = HiddenField()
    suid = HiddenField()
    suname = HiddenField()
    platform = HiddenField()
    token = HiddenField()
    expires_in = HiddenField()
    logo_url = HiddenField()
    sex = HiddenField()
    submit = SubmitField(u'完 成')
