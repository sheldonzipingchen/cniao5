# -*- coding: UTF-8 -*-
from ..models import  EmailTemplate


__author__ = 'Ivan'



class EmailTemplateDao():



    def get(self,id):
        return EmailTemplate.query.get(id)






