# -*- coding: UTF-8 -*-
from app import db, cache
from app.pagination import Pagination
from ..models import Thread, ThreadPost, Forum, ForumThreadRelation, ThreadLike, ActivityPost, Banner, PageMenu

__author__ = 'Ivan'


class PageMenuDao():

    def save(self,menu):
        db.session.add(menu)
        db.session.commit()

    def delete(self,menu):
        db.session.delete(menu)
        db.session.commit()

    def get(self,id):
        return PageMenu.query.get(id)

    #@cache.memoize(key_prefix='find_by_type')
    def find_by_type(self,type):
        return PageMenu.query.filter(PageMenu.type==type).order_by(PageMenu.sort);



