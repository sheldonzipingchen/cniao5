# -*- coding: UTF-8 -*-
from app import db
from ..models import PhoneMessage


__author__ = 'Ivan'




class PhoneMessageDao():

    def save(self,phone):
        db.session.add(phone)
        db.session.commit()



    def getPhoneMessage(self,phone,use_for,code):

         query =PhoneMessage.query;

         phone_message = query.filter(PhoneMessage.phone == phone) \
        .filter(PhoneMessage.code == code) \
        .filter(PhoneMessage.use_for == use_for) \
        .order_by(PhoneMessage.send_time.desc()).first()

         return phone_message

    def getPhoneMessage_use_for_find_pwd(self,phone,code):

        return self.getPhoneMessage(phone,'find_pwd',code)

    def findPhoneMessages_by_phone_usefor(self,phone,use_for):

         phone_messages = PhoneMessage.query.filter(PhoneMessage.phone == phone) \
        .filter(PhoneMessage.use_for == use_for) \
        .order_by(PhoneMessage.send_time.desc()).all()

         return phone_messages


    def findPhoneMessages_by_phone_use_for_find_pwd(self,phone):
        return  self.findPhoneMessages_by_phone_usefor(phone,'find_pwd')

    def getEmailMessage(self,email,use_for,code):

        phone_message = PhoneMessage.query.filter(PhoneMessage.email == email) \
        .filter(PhoneMessage.code == code) \
        .filter(PhoneMessage.use_for == use_for) \
        .order_by(PhoneMessage.send_time.desc()).first()

        return phone_message


    def getEmailMessage_from_findPassword(self,email,code):
        return self.getEmailMessage(email,'find_pwd',code)


    def getEmailMessage_from_bind_email(self,email,code):
        return self.getEmailMessage(email,'bind_email',code)


