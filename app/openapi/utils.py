# -*- coding: UTF-8 -*-


from flask.ext.restful import fields



__author__ = 'Ivan'




class DateFormat(fields.Raw):
    def format(self,value):

        if value is not None:
            value=value.strftime('%Y-%m-%d %H:%M:%S');
        else:
            value=''

        return value




class FirstImage(fields.Raw):

    def format(self, value):

        defualt_url ="http://cniao5.com/static/images/rcode_for_weixin.jpg"
        if value is not None:
             links = value.split(",")
             if len(links)>0:
                 defualt_url= links[0]

        return defualt_url