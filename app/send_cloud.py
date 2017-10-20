# -*- coding: UTF-8 -*-
import os
import requests

__author__ = 'Ivan'



BASE_URL_EMAIL='http://sendcloud.sohu.com/webapi/{0}.json'

class SendCloudAPI():

    def __init__(self,api_user,api_key):

        self.api_user = api_user
        self.api_key = api_key


    def group_list(self):
        api_name ='list.get'
        url = BASE_URL_EMAIL.format(api_name)
        params = {
        "api_user": self.api_user,
        "api_key": self.api_key,
        }
        result =requests.post(url,data=params)
        return result.text


    def template_get(self):

        api_name ='template.get'
        url = BASE_URL_EMAIL.format(api_name)

        params = {
        "api_user": self.api_user,
        "api_key": self.api_key,

        }

        result =requests.post(url,data=params)

        return result.text


    def template_get_by_invoke_name(self,invoke_name):
        api_name ='template.get'
        url = BASE_URL_EMAIL.format(api_name)

        params = {
        "api_user": self.api_user,
        "api_key": self.api_key,
        'invoke_name':invoke_name

        }

        result =requests.post(url,data=params)

        return result.text


API_USER=os.environ.get('API_USER')
API_USER_MULTI=os.environ.get('API_USER_MULTI')
API_KEY=os.environ.get('API_KEY')

send_cloud_trigger = SendCloudAPI(API_USER,API_KEY)
send_cloud_multi = SendCloudAPI(API_USER_MULTI,API_KEY)