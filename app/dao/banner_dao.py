# -*- coding: UTF-8 -*-
from app import db
from app.pagination import Pagination
from ..models import Thread, ThreadPost, Forum, ForumThreadRelation, ThreadLike, ActivityPost, Banner

__author__ = 'Ivan'


class BannerDao():

    def save(self,banner):
        db.session.add(banner)
        db.session.commit()

    def delete(self,banner):
        db.session.delete(banner)
        db.session.commit()


    def find_all(self):
        return Banner.query.order_by(Banner.state,Banner.order_num);

    def find_active(self):
        return Banner.query.filter(Banner.state==0).order_by(Banner.order_num).all()

    def get(self,id):
        return Banner.query.get(id)


