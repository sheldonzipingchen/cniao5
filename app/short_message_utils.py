# -*- coding: UTF-8 -*-

__author__ = 'SheldonChen'


def send_short_message(phones, content):
    """ 发送短信的方法 """
    import urllib

    params_dict = {'id': 'cniao5@163.com',
              'pwd': 'cniao5123456',
              'to': phones,
              'content': content.encode('gb2312','ignore'),
              'time': ''}
    params = urllib.urlencode(params_dict)
    response = urllib.urlopen('http://service.winic.org/sys_port/gateway/?%s' % params)
    html = response.read()
    return html


# if __name__ == '__main__':
#     phones = '18664879291'
#     content = u'测试短信'
#     html = send_short_message(phones, content)
#     print html




if __name__ == '__main__':

    # query=User.query
    # query =query.join(ProductOrder,ProductOrder.user_id ==User.id)\
    #     .filter(ProductOrder.state==1,ProductOrder.product_id==8,
    #             ProductOrder.cancel_time>'2015-06-23 00:00:00',ProductOrder.cancel_time<'2015-06-24 00:00:00')
    #
    # users = query.all()
    #
    #
    # if len(users) >0:
    #
    #     for user in users:
    #         print users.email

    phones =[

        #23号到期
        # 18824240204,
        # 13153054020,
        # 13503081782,
        # 13268040417,
        # 18290028275,
        # 15168859012,
        # 18651818496,
        # 13823695205,
        # 15333724135,
        # 13695316326,
        # 18601365787,
        # 13610094483,
        # 13925770763,
        # 13659260614




        #24号到期
        # 13381340726,
        # 13760772207,
        # 15971421473,
        # 18689208135,
        # 18696080439,
        # 15091675365,
        # 18744023642,
        # 18639719980,
        # 15059719267,
        # 18930947558,
        # 15566690695,
        # 18010678190,
        # 13578918907,
        # 15170006264,
        # 18819012482,
        # 18824614591,
        # 13144410811


        18689208135,
        18824240204,
        13153054020,
        13503081782,
        13268040417,
        18290028275,
        15168859012,
        13823695205,
        15333724135,
        13695316326,
        18601365787,
        13610094483,
        13925770763,
        13659260614,
        13381340726,
        13760772207,
        15971421473,
        15091675365,
        18744023642,
        18639719980,
        15059719267,
        18930947558,
        15566690695,
        18010678190,
        15170006264,
        18819012482,
        13144410811,
        18651818496,
        18696080439,
        13578918907,
        18824614591






    ]

    # 尊敬的菜鸟窝高级会员，您的高级会员X天后(2015-06-xx)到期！请及时续费，不然我就要离你而去了噢o(>﹏<)o

    msg =u'尊敬的菜鸟窝会员，恭喜您获得了一张优惠劵,到期时间为2015-06-23，记得使用喔。详情到【会员中心-我的优惠劵】查看'

    for p in phones:
        print  p
        result = send_short_message(p,msg)
        print  result








