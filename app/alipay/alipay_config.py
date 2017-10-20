# -*- coding:utf-8 -*-

__author__ = 'SheldonChen'


class Settings(object):
    # 安全检验码，以数字和字母组成的32位字符
    ALIPAY_KEY = 'dxlo5n8z7q2ui6o9zutja6tp5iqio22p'

    ALIPAY_INPUT_CHARSET = 'utf-8'

    # 合作身份者ID，以2088开头的16位纯数字
    ALIPAY_PARTNER = '2088311784493747'

    # 签约支付宝账号或卖家支付宝帐户
    ALIPAY_SELLER_EMAIL = 'yctadmin@163.com'

    ALIPAY_SIGN_TYPE = 'MD5'

    # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    #ALIPAY_RETURN_URL = 'http://www.cniao5.com/pay/return'

    ALIPAY_RETURN_URL = 'http://www.cniao5.com/pay/return/alipay'

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    #ALIPAY_NOTIFY_URL = 'http://www.cniao5.com/pay/notify'


    ALIPAY_NOTIFY_URL = 'http://www.cniao5.com/pay/notify/alipay'


        # 付完款后跳转的页面（同步通知） 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    #ALIPAY_CLAZZ_RETURN_URL = 'http://www.cniao5.com/pay/clazz/return'
    #ALIPAY_CLAZZ_RETURN_URL = 'http://www.cniao5.com/pay/clazz/return'

    # 交易过程中服务器异步通知的页面 要用 http://格式的完整路径，不允许加?id=123这类自定义参数
    #ALIPAY_CLAZZ_NOTIFY_URL = 'http://www.cniao5.com/pay/clazz/notify'
    #ALIPAY_CLAZZ_NOTIFY_URL = 'http://www.cniao5.com/pay/clazz/notify'


    ALIPAY_SHOW_URL = ''

    # 访问模式,根据自己的服务器是否支持ssl访问，若支持请选择https；若不支持请选择http
    ALIPAY_TRANSPORT = 'http'
