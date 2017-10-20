# -*- coding: UTF-8 -*-
import hashlib
from datetime import datetime

from sqlalchemy import or_, func

from app import db
from app.pagination import Pagination
from ..models import  User, ProductOrder, UserIncome, UserWithdrawal, UserMsg, InviteRecord, SocialUser, UserFollow, \
    Teacher, Thread

__author__ = 'Ivan'



class UserDao():

    def get(self,id):
       return User.query.get(id)

    def get_by_code(self,code):
        return User.query.filter(User.unique_code==code).first();

    def get_by_invite_code(self,code):
        return User.query.filter(User.invite_code==code).first();

    #保存用户信息
    def save(self,user):
        db.session.add(user)
        db.session.commit()

    # 根据邮箱或者手机号查找用户
    def find_by_email_phone(self, email_or_mobi):
        user = User.query.filter_by(email=email_or_mobi).first()
        if user is None:
            user = User.query.filter_by(mobi=email_or_mobi).first()

        return user

    # 根据手机号查找用户
    def find_by_mobi(self,mobi):
        user = User.query.filter_by(mobi=mobi).first();
        return user;

    def find_by_mobi_confirmed(self,mobi):

        user = User.query.filter(User.mobi == mobi)\
             .filter(User.mobile_confirmed == True).\
             first()

        return user

    # 根据用户名查找用户
    def find_by_username(self,username):
        user = User.query.filter_by(username=username).first()
        return user

    def find_vips(self,top):
        query=User.query
        query =query.join(ProductOrder,ProductOrder.user_id ==User.id)\
            .filter(ProductOrder.state==1,ProductOrder.cancel_time>datetime.now())\
            .order_by(ProductOrder.created_time.desc())\
            .limit(top)

        vip_members = query.all()

        return vip_members

    def find_user_followers(self,user_id):

        return User.query.join(UserFollow,UserFollow.follower_id==User.id).filter(UserFollow.followed_id==user_id).order_by(UserFollow.timestamp.desc()).all()


    def find_user_following(self,user_id):

        query = User.query.join(UserFollow,UserFollow.followed_id==User.id).filter(UserFollow.follower_id==user_id).order_by(UserFollow.timestamp.desc())
        return query.all()


    def find_teacher_users(self):
        return User.query.filter(User.user_type==2).all()


    def find_top10_thread_writer(self):

       return db.session.query(User.id,User.username,User.logo_url, func.count(Thread.user_id).label('total')).join(Thread).group_by(User).order_by('total DESC').limit(10).all()

class TeacherDao():

      def save(self,t):
          db.session.add(t)
          db.session.commit()


      def find_all(self):

          return Teacher.query.filter(Teacher.is_show==1).order_by(Teacher.sort_num).all()

      def get_by_user_id(self,user_id):
          return Teacher.query.filter(Teacher.user_id==user_id).first()


      def find_recommend(self,limit):
          return Teacher.query.filter(Teacher.is_show==1,Teacher.is_recommend==1).order_by(Teacher.sort_num).limit(limit).all()


class SocialUserDao():

    def save(self,user):
        db.session.add(user)
        db.session.commit()

    def get_by_open_id(self,open_id):
        return SocialUser.query.filter(SocialUser.open_id == open_id).first()


class UserIncomeDao():
    def save(self,income):
        db.session.add(income)
        db.session.commit()

    def find_user_incomes(self,user_id):
        return UserIncome.query.filter(UserIncome.user_id==user_id).order_by(UserIncome.created_time.desc()).all()


    def find_user_total_income_in_time_bucket(self,user_id,begin_time,end_time):

        begin_time = begin_time.strftime("%Y-%m-%d") +' 00:00:00'
        end_time = end_time.strftime("%Y-%m-%d") +' 59:59:59'
        query= db.session.query(func.sum(UserIncome.money).label('total_money')).filter(UserIncome.user_id==user_id,

                                                                                        UserIncome.created_time>begin_time,
                                                                                        UserIncome.created_time<end_time)
        return  query.first()






    def find_teachers_income(self,page_index,page_size,teacher_id=None):
        query = UserIncome.query.filter(UserIncome.from_type==3)

        if teacher_id !=None:
            query=query.filter(UserIncome.user_id==teacher_id)

        query=query.order_by(UserIncome.created_time.desc())

        count = query.count()


        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size


        items =query.offset(offset).limit(page_size).all()

        return  Pagination(count,page_index,page_size,items);



class UserWithdrawalDao():
    def save(self,withdrawal):
        db.session.add(withdrawal)
        db.session.commit()

    def get(self,id):
       return UserWithdrawal.query.get(id)

    def find_user_withdrawals(self,user_id):
        return UserWithdrawal.query.filter(UserWithdrawal.user_id==user_id).order_by(UserWithdrawal.created_time.desc()).all()


    def pagination(self,page_index,page_size,state,user_id=None):

        query = UserWithdrawal.query


        if int(state) >=0:
            query=query.filter(UserWithdrawal.state==state)

        if user_id !=None:
            query=query.filter(UserWithdrawal.user_id==user_id)

        query=query.order_by(UserWithdrawal.created_time.desc())

        count = query.count()


        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size


        items =query.offset(offset).limit(page_size).all()

        return  Pagination(count,page_index,page_size,items);

class UserMessageDao():
    def save(self,msg):

        msg.conversation_id=self.generate_conversation_code(msg.from_user_id,msg.to_user_id)
        msg.orientation=1
        msg.msg_type=1
        msg.is_read=0
        msg.send_time=datetime.now()

        db.session.add(msg)
        db.session.commit()

    def generate_conversation_code(self,from_user_id,to_user_id):
         id ='%s|%s'%(str(from_user_id),str(to_user_id))
         if to_user_id>from_user_id:
             id ='%s|%s'%(str(to_user_id),str(from_user_id))

         return hashlib.sha1(id).hexdigest()

    def delete(self,msg):
        db.session.delete(msg)
        db.session.commit()


    def get_or_404(self,id):
        return UserMsg.query.get_or_404(id)


    def find_all(self):
        return UserMsg.query.all()


    def find_user_unread_msg_count(self,user_id):
        return UserMsg.query.filter(UserMsg.to_user_id==user_id,UserMsg.is_read==False).count()

    def find_user_conversation_unread_messages(self,user_id,conversation_id):
        return UserMsg.query.filter(UserMsg.to_user_id==user_id,UserMsg.conversation_id==conversation_id, UserMsg.is_read==False).all()

    def user_conversation_messages_read(self,user_id,conversation_id):
        messages = self.find_user_conversation_unread_messages(user_id,conversation_id)
        if len(messages) >0:
            for message in messages:
                if message.is_read==False:
                    message.is_read=True
                    message.read_time = datetime.now()
                    self.save(message)

    def find_conversation_messages(self,conversation_id):

        query =  UserMsg.query.filter(UserMsg.conversation_id==conversation_id)
        return query.all();


    def find_user_messages(self,user_id):
        query =UserMsg.query.filter(or_(UserMsg.to_user_id==user_id,UserMsg.from_user_id==user_id)).group_by(UserMsg.conversation_id).order_by(UserMsg.id.desc())

        return query.all();


class InviteRecordDao():

    def save(self,record):
        db.session.add(record)
        db.session.commit()


    def find_user_invite_list(self,invite_user_id):
        return InviteRecord.query.filter(InviteRecord.inviter_id==invite_user_id).all()