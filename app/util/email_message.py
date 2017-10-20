# -*- coding: UTF-8 -*-
import json
import random
import string
from datetime import datetime
from flask import render_template
import requests
import os
from .. dao.phone_message_dao import PhoneMessageDao
from .. models import PhoneMessage

url = "http://sendcloud.sohu.com/webapi/mail.send.json"
temp_url=  "http://sendcloud.sohu.com/webapi/mail.send_template.json"

temp_url_v2='http://api.sendcloud.net/apiv2/mail/sendtemplate'



API_USER=os.environ.get('API_USER')
API_USER_MULTI=os.environ.get('API_USER_MULTI')


API_KEY=os.environ.get('API_KEY')

def send_email(to, subject, template, **kwargs):
    html = render_template(template + '.html', **kwargs)
    params = {
        "api_user": API_USER,
        "api_key": API_KEY,
        "to": to,
        "from": 'no-reply@cniao5.com',
        "fromname": u'菜鸟窝',
        "subject": subject,
        "html": html,
        "resp_email_id": "true",
    }
    r = requests.post(url, files="", data=params)
    print r.text




def send_email_use_html(to, subject,html):

    params = {
        "api_user": API_USER_MULTI,
        "api_key": API_KEY,
        "to": to,
        "from": 'no-reply@cniao5.com',
        "fromname": u'菜鸟窝',
        "subject": subject,
        "html": html,
        "resp_email_id": "true",
    }
    r = requests.post(url, files="", data=params)
    print r.text

def send_email_template_group(template_invoke_name, group):
    params = {
        "api_user": API_USER_MULTI,
        "api_key": API_KEY,
        "from": 'postmaster@cniao5.sendcloud.org',
        "fromname": u'菜鸟窝',
        "template_invoke_name": template_invoke_name,
        "use_maillist":True,
        "to":group,
        "resp_email_id": "true"
    }
    r = requests.post(temp_url, files="", data=params)
    return r.text



def send_email_use_template(template_id,sub_vars):

    params = {
        "apiUser": API_USER, # 使用api_user和api_key进行验证
        "apiKey" : API_KEY,
        "templateInvokeName" : template_id,
        "xsmtpapi" : json.dumps(sub_vars),
        "from": 'postmaster@cniao5.sendcloud.org',
        "fromName": u'菜鸟窝',
        "respEmailId": "true",
    }

    r = requests.post(temp_url_v2, files="", data=params)
    print  r.text




# 发送找回密码的验证码
def send_code_for_find_pwd(email):

     code = string.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)).replace(" ", "")
     sub_vars = {
                'to': [email],
                'sub': {
                    '%code%': [code]
                }
            }

     send_email_use_template('validate_for_find_pwd',sub_vars)

     use_for = 'find_pwd'
     phone_message = PhoneMessage(phone='00000000000',
                                     code=code,
                                     message='validate_for_find_pwd',
                                     send_time=datetime.now(),
                                     use_for=use_for,
                                     send_type=1,
                                     email=email
                                     )


     PhoneMessageDao().save(phone_message)




def send_code_for_find_email(email):

     code = string.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)).replace(" ", "")
     sub_vars = {
                'to': [email],
                'sub': {
                    '%code%': [code]
                }
            }

     send_email_use_template('bind_email_code',sub_vars)

     use_for = 'bind_email'
     phone_message = PhoneMessage(phone='00000000000',
                                     code=code,
                                     message='bind_email_code',
                                     send_time=datetime.now(),
                                     use_for=use_for,
                                     send_type=1,
                                     email=email
                                     )


     PhoneMessageDao().save(phone_message)