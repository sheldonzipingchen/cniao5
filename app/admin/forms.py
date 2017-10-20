# -*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, FileField, RadioField, TextAreaField, PasswordField, SubmitField, \
    HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import Required


__author__ = 'Sheldon Chen'


class NewProductForm(Form):
    """
    添加产品表单
    """
    name = StringField(u'会员卡名称', validators=[Required(message=u'会员卡名称不能为空')])
    month_price = IntegerField(u'价格（月，单位：分）', validators=[Required(message=u'价格（月）不能为空')])
    year_price = IntegerField(u'价格（年，单位：分）')
    comment = TextAreaField(u'备注')
    submit = SubmitField(u'保存')





class UploadLessonForm(Form):
    """
    上传视频表单
    """
    name = StringField(u'视频标题', validators=[Required(message=u'视频标题不能为空')])
    video_url = FileField(u'选择视频', validators=[Required(message=u'视频文件不能为空')])
    is_free = RadioField(u'是否是免费视频', choices=[('0', u'上传到免费空间'), ('1', u'上传到收费空间')])
    submit = SubmitField(u'开始上传')


class VideoCompilationForm(Form):
    """
    视频合辑表单
    """
    name = StringField(u'视频合辑名称', validators=[Required(message=u'视频合辑不能为空')])
    submit = SubmitField(u'保存')


class AdminLoginForm(Form):
    """
    管理员登录表单
    """
    name = StringField(u'用户名', validators=[Required(message=u'用户名不能为空')])
    password = PasswordField(u'密码', validators=[Required(message=u'密码不能为空')])
    submit = SubmitField(u'登录')


class NewChapterForm(Form):
    """
    创建章节的表单
    """
    title = StringField(u'请输入章节名称', validators=[Required(message=u'章节名称不能为空')])
    submit = SubmitField(u'添加')






class NewQQGroupForm(Form):
    """
     添加QQ群表单
    """
    name = StringField(u'Q群名称', validators=[Required(message=u'Q群名称')])
    num = StringField(u'Q群号码', validators=[Required(message=u'Q群号码')])
    link = StringField(u'Q群链接', validators=[Required(message=u'Q群链接')])
    desc = TextAreaField(u'备注')
    submit = SubmitField(u'添加')


class NewClassTypeForm(Form):
    """
     添加课程分类表单
    """
    name = StringField(u'名称', validators=[Required(message=u'名称')])
    desc = TextAreaField(u'简介')
    submit = SubmitField(u'添加')



class NewSecondClassTypeForm(NewClassTypeForm):
    parent_id =HiddenField();


class NewFriendLinkForm(Form):
    site_name = StringField(u'网站名称', validators=[Required(message=u'网站名称')])
    site_url = StringField(u'网站地址', validators=[Required(message=u'网站地址')])
    title = StringField(u'标题', validators=[Required(message=u'标题')])
    contact=TextAreaField(u'联系方式')
    submit = SubmitField(u'添加')


class NewChapterForm(Form):

    title=StringField(u'章节名称', validators=[Required(message=u'章节名称')])
    class_id = HiddenField();
    submit = SubmitField(u'添加')
