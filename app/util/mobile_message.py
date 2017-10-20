# -*- coding: UTF-8 -*-
import os
import random
import string
from datetime import datetime
import requests
from hashlib import md5
from .. dao.phone_message_dao import PhoneMessageDao
from .. models import PhoneMessage

__author__ = 'longo'


url = "http://sendcloud.sohu.com/smsapi/send"
sendx_url = 'http://sendcloud.sohu.com/smsapi/sendx'
SMS_USER = os.environ.get('SMS_USER')
SMS_KEY = os.environ.get('SMS_KEY')

def generate_md5(fp):
    m = md5()
    m.update(fp)
    return m.hexdigest()

def send__message(phone, tempId, vars):


    if phone ==None or phone=='':
        return


    """ 发送短信的方法 """
    param = {
        'smsUser': SMS_USER,
        'templateId' : tempId,
        'phone': phone,
        'vars' : vars
    }

    param_keys = list(param.keys())
    param_keys.sort()

    param_str = ""
    for key in param_keys:
        param_str += key + '=' + str(param[key]) + '&'
    param_str = param_str[:-1]

    sign_str = SMS_KEY + '&' + param_str + '&' + SMS_KEY
    sign = generate_md5(sign_str)

    param['signature'] = sign

    res = requests.post(url,data=param)
    print res.text



#发送注册短信验证码
def send_code_for_reg_use_mobile(mobile):

    code = string.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)).replace(" ", "")
    message = '您现在正在注册菜鸟窝账号，验证码是%s ，10分钟后过期，祝你学习愉快！【菜鸟窝】 ' % (code)
    vars_param = '{"%code%": "' + code + '"}'

    send__message(str(mobile), 661, vars_param)

    use_for = 'reg'
    save_phone_message(mobile,code,message,use_for)



#发送注册短信验证码
def send_code_for_bind_mobile(mobile):

    code = string.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)).replace(" ", "")
    message = '您正在绑定手机，验证码是%s ，10分钟后过期，祝你学习愉快！【菜鸟窝】 ' % (code)
    vars_param = '{"%code%": "' + code + '"}'

    send__message(str(mobile), 1063, vars_param)

    use_for = 'bind_mobile'
    save_phone_message(mobile,code,message,use_for)






def send_message_for_find_pwd_use_mobile(mobile):

    code = string.join(random.sample(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)).replace(" ", "")
    message = '您真正使用找回密码服务，验证码是%s ，10分钟后过期，祝你学习愉快！【菜鸟窝】 ' % (code)
    vars_param = '{"%code%": "' + code + '"}'

    send__message(str(mobile), 665, vars_param)

    use_for = 'find_pwd'
    save_phone_message(mobile,code,message,use_for)



def send_message_for_buy_vip_success(mobile,ex_date,qq_group):

    message = '您已成功开通高级会员，有效期至：%s,请加入会员学习群：%s，祝学习愉快！【菜鸟窝】】 ' % (ex_date,qq_group)
    vars_param = '{"%ex_date%": "'+ex_date+'","%qq_group%":"'+qq_group+'"}'

    send__message(str(mobile), 949, vars_param)

    use_for = 'buy_vip_success'

    save_phone_message(mobile,0,message,use_for)


def send_message_for_buy_course_success(mobile,qq_group,class_name):

    message = '您已成功报名《%s》,请加入课程学习群：%s，祝你学习愉快！【菜鸟窝】' % (class_name,qq_group)
    vars_param = '{"%class_name%": "'+class_name+'","%qq_group%":"'+qq_group+'"}'

    send__message(str(mobile), 664, vars_param)

    use_for = 'join_class_success'

    save_phone_message(mobile,0,message,use_for)



def send_message_for_have_income(mobile,title,money):

    message = '恭喜你进米了，本次 %s 共 %s 元,请再接再厉【菜鸟窝】'%(title,str(money))
    vars_param = '{"%title%": "'+title+'","%money%":"'+str(money)+'"}'

    send__message(str(mobile), 1130, vars_param)

    use_for = 'have_income'

    save_phone_message(mobile,0,message,use_for)





def send_message_for_reg_by_invite(mobile,user_name):


    message = '恭喜您注册成功。%s 赠送您的30天VIP已到账。祝学习愉快！【菜鸟窝】'%(user_name)
    # vars_param = '{"%username%":'+str(user_name)+'}'
    vars_param = '{}'

    send__message(str(mobile), 1582, vars_param)

    use_for = 'reg_by_invite'

    save_phone_message(mobile,0,message,use_for)


def send_message_for_invite_success_with_vip(mobile,coin_num):

    message = '恭喜你成功邀请一位好友加入菜鸟窝，赠与您的30天VIP和%s个鸟币已到账，继续努力哦！(*^__^*)'%(str(coin_num))
    vars_param = '{"%coin_num%": '+str(coin_num)+'}'


    send__message(str(mobile), 1583, vars_param)

    use_for = 'invite_success_with_vip'

    save_phone_message(mobile,0,message,use_for)



def send_message_for_invite_success_without_vip(mobile,coin_num):

    message = '恭喜你成功邀请一位好友加入菜鸟窝，赠与您的%s个鸟币已到账，继续努力哦！(*^__^*)'%(str(coin_num))
    vars_param = '{"%coin_num%": '+str(coin_num)+'}'

    send__message(str(mobile), 1584, vars_param)

    use_for = 'invite_success_without_vip'

    save_phone_message(mobile,0,message,use_for)

def send_message_for_teacher_settlement(mobile,money):

    vars_param = '{"%money%": '+str(money)+'}'

    send__message(str(mobile), 2491, vars_param)










def save_phone_message(mobile,code,message,use_for):

    phone_message = PhoneMessage(phone=mobile,
                                     code=code,
                                     message=message,
                                     send_time=datetime.now(),
                                     use_for=use_for,
                                     send_type=0)


    PhoneMessageDao().save(phone_message)