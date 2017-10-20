# -*- coding: UTF-8 -*-
from app import db
from app.pagination import Pagination
from ..models import Thread, ThreadPost, Forum, ForumThreadRelation, ThreadLike

__author__ = 'Ivan'



class ThreadDao():

    def save(self,thread):
        db.session.add(thread)
        db.session.commit()

    def delete(self,thread):
        db.session.delete(thread)
        db.session.commit()


    def get_or_404(self,id):
        return  Thread.query.get_or_404(id)

    def get(self,id):
        return Thread.query.filter(Thread.status==1,Thread.id==id).first()

    def get_user_thread_count(self,user_id):
        return Thread.query.filter(Thread.user_id==user_id).count()

    def find_user_threads(self,user_id,limit):
        return Thread.query.filter(Thread.user_id==user_id,Thread.status==1).order_by(Thread.id.desc()).limit(limit).all()

    def find_forum_hot_threads(self,forum_id,limit):

        query =  Thread.query.join(ForumThreadRelation,ForumThreadRelation.thread_id==Thread.id)\
            .filter(ForumThreadRelation.forum_id==forum_id,Thread.is_hot==1).order_by(ForumThreadRelation.created_time.desc()).limit(limit)


        return  query.all()

    def pagination(self,target_id,target_type,order_by,page_index,page_size):


        query = Thread.query
        query=query.filter(Thread.status==1)

        if target_type =='course':
            query = query.filter(Thread.class_id==target_id)

        elif target_type=='user':
            query = query.filter(Thread.user_id==target_id)

        if order_by ==0: #按发布时间排序
            query=query.order_by(Thread.created_time.desc())
        else:
            query = query.order_by(Thread.last_comment_time.desc())


        count = query.count()


        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size


        items =query.offset(offset).limit(page_size).all()


        return  Pagination(count,page_index,page_size,items);


    def pagination_for_forum(self,forum_id,order_by,is_hot,page_index,page_size):



        query = Thread.query

        query= query.join(ForumThreadRelation,ForumThreadRelation.thread_id==Thread.id)

        query = query.filter(Thread.status==1)

        if forum_id>0:
            query = query.filter(ForumThreadRelation.forum_id==forum_id)

        if is_hot>0:
            query = query.filter(Thread.is_hot==is_hot)

        if order_by ==0: #按发布时间排序
            query=query.order_by(Thread.created_time.desc())
        else:
            query = query.order_by(Thread.last_comment_time.desc())



        count = query.count()


        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size


        items =query.offset(offset).limit(page_size).all()


        return  Pagination(count,page_index,page_size,items);

class ThreadLikeDao():
    def save(self,like):
        db.session.add(like)
        db.session.commit()

    def get_by_user_thread(self,user_id,thread_id):
        return ThreadLike.query.filter(ThreadLike.thread_id==thread_id,ThreadLike.user_id==user_id).first()


class ThreadPostDao():
    def save(self,post):
        db.session.add(post)
        db.session.commit()

    def delete(self,post):
        db.session.delete(post)
        db.session.commit()


    def get(self,id):
        return ThreadPost.query.get(id)

    def get_thread_user_post_count(self,user_id,thread_id):
        return ThreadPost.query.filter(ThreadPost.user_id==user_id,ThreadPost.thread_id==thread_id).count()


    def find_thread_today_posts(self,thread_id):

        import datetime
        t= datetime.datetime.today()
        oneday=datetime.timedelta(days=1)
        yesterday = t -oneday

        yesterday =  datetime.datetime.strftime(yesterday, '%Y-%m-%d')
        start = yesterday+ " 00:00:00"
        end = yesterday+" 23:59:59"

        print start
        print end

        query = ThreadPost.query.filter(ThreadPost.thread_id==thread_id,ThreadPost.created_time.between(start,end))
        return  query.all()

    def pagination(self,thread_id,page_index,page_size):

        query = ThreadPost.query
        query=query.filter(ThreadPost.thread_id==thread_id)

        query=query.order_by(ThreadPost.created_time.desc())

        count = query.count()


        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size


        items =query.offset(offset).limit(page_size).all()


        return  Pagination(count,page_index,page_size,items);

class ThreadRequestDao():
      def save(self,rq):
        db.session.add(rq)
        db.session.commit()


class ForumDao():

    def get(self,id):
       return Forum.query.get(id)

    def save(self,forum):
        db.session.add(forum)
        db.session.commit()

    def find_all(self):
        return Forum.query.filter(Forum.is_online==1,Forum.is_display==1).order_by(Forum.order_num).all()


class ForumThreadRelationDao():

    def save(self,relation):
        db.session.add(relation)
        db.session.commit()