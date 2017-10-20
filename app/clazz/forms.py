# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError

from ..models import User


__author__ = 'longo'



class TrainEnrollForm(Form):
    """
    培训班级报名表单
    """
    train_type = HiddenField(u'培训类型')
    realname = StringField(u'姓名', validators=[Required(message='您的姓名不能为空')])
    mobil = StringField(u'手机', validators=[Required(message='手机号不能为空')])
    qq = StringField(u'QQ', validators=[Required(message='QQ不能为空')])
    remark = StringField(u'留言')

    submit = SubmitField(u'提交报名')


class ClassNetForm(Form):
    """
    培训班级报名表单
    """
    classfee = StringField(u'学费', validators=[Required(message='您的学费不能为空')])
    submit = SubmitField(u'提交保存')