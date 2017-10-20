# -*- coding: UTF-8 -*-

import re
import types

__author__ = 'Ivan'


class DataValidate():


    def isMobile(self,value):

        rule='^1[3|4|5|7|8]\d{9}$';

        match = re.match( rule , value )

        if match:
            return True
        return False


    def isEmailOrMobile(self,value):

        isEmail = self.isEmail(value)
        print  isEmail
        if isEmail:
            return  True
        else:
            isMobi =self.isMobile(value)
            print  isMobi
            if isMobi:
                return True

        return False


    #判断是否为整数 15
    def isNumber(self,varObj):

        return type(varObj) is types.IntType

    #判断是否为字符串 string
    def isString(self,varObj):

        return type(varObj) is types.StringType

    #判断是否为浮点数 1.324
    def isFloat(self,varObj):
        return type(varObj) is types.FloatType

    #判断是否为字典 {'a1':'1','a2':'2'}
    def isDict(self,varObj):

        return type(varObj) is types.DictType

    #判断是否为tuple [1,2,3]
    def IsTuple(self,varObj):

        return type(varObj) is types.TupleType

    #判断是否为List [1,3,4]
    def isList(self,varObj):

        return type(varObj) is types.ListType

    #判断是否为布尔值 True
    def IsBoolean(self,varObj):

        return type(varObj) is types.BooleanType

    #判断是否为货币型 1.32
    def isCurrency(self,varObj):

        #数字是否为整数或浮点数
        if self.IsFloat(varObj) and self.isNumber(varObj):
            #数字不能为负数
            if varObj >0:
                return self.isNumber(varObj)
                return False
        return True

    #判断某个变量是否为空 x
    def isEmpty(self,varObj):

        if len(varObj) == 0:
            return True
        return False

    #判断变量是否为None None
    def isNone(self,varObj):

        return type(varObj) is types.NoneType# == "None" or varObj == "none":

    #判断是否为日期格式,并且是否符合日历规则 2010-01-31
    def IsDate(self,varObj):

        if len(varObj) == 10:
            rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
            match = re.match( rule , varObj )
            if match:
                return True
            return False
        return False

    #判断是否为邮件地址
    def isEmail(self,varObj):

        rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
        match = re.match( rule , varObj )

        if match:
            return True
        return False

    #判断是否为中文字符串
    def isChineseCharString(self,varObj):

        for x in varObj:
            if (x >= u"\u4e00" and x<=u"\u9fa5") or (x >= u'\u0041' and x<=u'\u005a') or (x >= u'\u0061' and x<=u'\u007a'):
               continue
            else:
               return False
        return True


    #判断是否为中文字符
    def isChineseChar(self,varObj):

        if varObj[0] > chr(127):
           return True
        return False

    #判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线
    def isLegalAccounts(varObj):

        rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
        match = re.match( rule , varObj )

        if match:
            return True
        return False

    #匹配IP地址
    def isIpAddr(self,varObj):

        rule = '\d+\.\d+\.\d+\.\d+'
        match = re.match( rule , varObj )

        if match:
            return True
        return False


    #判断是否为正整数
    def isPositiveInteger(self,val):

        rule = '^[0-9]*[1-9][0-9]*$'
        return self.rule_match(rule,str(val))

     #判断是否为整数
    def isInteger(self,val):
        rule='^[+-]?\d+$'
        return self.rule_match(rule,str(val))

    def rule_match(self,rule,val):

        match = re.match(rule , str(val))

        if match:
            return True
        return False



