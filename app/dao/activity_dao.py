# -*- coding: UTF-8 -*-
from app import db
from app.pagination import Pagination
from ..models import Thread, ThreadPost, Forum, ForumThreadRelation, ThreadLike, ActivityPost, ActivityDoubleEleven

__author__ = 'Ivan'


class ActivityPostDao():

    def save(self,ap):
        db.session.add(ap)
        db.session.commit()


    def find_all(self):
        return ActivityPost.query.all();


    def get_by_user(self,user_id):
        return ActivityPost.query.filter(ActivityPost.user_id==user_id).first()


class DoubleElevenDao():
    def find_by_type(self,type):
       return ActivityDoubleEleven.query.filter(ActivityDoubleEleven.type==type).order_by(ActivityDoubleEleven.sort_num).all()