# -*- coding: UTF-8 -*-
from datetime import datetime

from sqlalchemy import or_, and_, func

from app import db, cache, cache_view_time
from .. pagination import Pagination
from ..models import Course, LessonPlay, CourseNote, Chapter, Lesson, CourseComment, CourseWare,  Video, \
    CourseProductRelationship, ProductOrder, CourseStudy, CourseFavorites, LessonStudy, CourseTopic, ClassDraws

__author__ = 'Ivan'



class CourseDao():

    def get(self,id):
       return Course.query.get(id)

    def save(self,course):
        db.session.add(course)
        db.session.commit()


    def get_all(self,page_index,page_size):

        query = Course.query

        query = query.order_by(Course.created_time.desc(),Course.is_hot.desc())

        count = query.count()

        offset = 0
        if (page_index > 1):
            offset = (page_index - 1) * page_size

        items = query.offset(offset).limit(page_size).all()

        return Pagination(count, page_index, page_size, items);



    def get_project_courses(self):
        return Course.query.filter(Course.types==2).order_by(Course.created_time.desc()).all()

    def get_or_404(self,id):
        return Course.query.get_or_404(id)

    def get_by_lesson_id(self,lesson_id):

        chapter = Chapter.query.join(Lesson,Lesson.chapter_id==Chapter.id).filter(Lesson.id==lesson_id).first()
        if chapter==None:
            return None

        return  self.get(chapter.class_id)

    def get_by_chapter_id(self,chapter_id):

        return Course.query.join(Chapter,Chapter.class_id==Course.id).filter(Chapter.id==chapter_id).first()

    def get_play_list_top(self,id,limit):

        query=LessonPlay.query.filter(LessonPlay.class_id ==id).order_by(LessonPlay.play_time.desc())

        last_play = query.group_by(LessonPlay.user_id).limit(limit).all()

        return last_play

    def get_total_play_count(self,id):

        query=LessonPlay.query.filter(LessonPlay.class_id ==id).order_by(LessonPlay.play_time.desc())
        play_count=query.count()

        return  play_count

    def find_vip_courses(self):
        query = Course.query.join(CourseProductRelationship,CourseProductRelationship.class_id==Course.id)

        query=query.filter(Course.is_online==1,CourseProductRelationship.product_id==8,CourseProductRelationship.product_type==0)
        query=query.order_by(Course.created_time.desc())

        return  query.all()


    def find_user_teach_courses(self,user_id,limit):

        return  Course.query.filter(Course.user_id==user_id).order_by(Course.id.desc()).limit(limit).all()


    def find_user_learn_courses(self,user_id,limit):

        return Course.query.join(CourseStudy,CourseStudy.class_id==Course.id).filter(CourseStudy.user_id==user_id).order_by(Course.id.desc()).limit(limit).all()


    def find_topic_courses(self,topic_id):

        query = Course.query.join(CourseProductRelationship,CourseProductRelationship.class_id==Course.id)
        query=query.filter(Course.is_online==1,CourseProductRelationship.product_id==topic_id,CourseProductRelationship.product_type==2)
        query=query.order_by(CourseProductRelationship.created_time)

        return  query.all()

    @cache.memoize(timeout=cache_view_time)
    def pagination(self,is_free,order_by,page_index,page_size):


        query = Course.query
        query=query.filter(Course.is_online==1)


        if order_by ==0: #按发布时间排序
            query=query.order_by(Course.created_time.desc())
        elif order_by==1:
            query = query.order_by(Course.lessons_played_time.desc())

        elif order_by==2:
            query = query.order_by(Course.is_hot.desc(),Course.lessons_played_time.desc())

        if is_free  ==0 or  is_free==1:
            query=query.filter(Course.is_free==is_free)

        count = query.count()

        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size

        items =query.offset(offset).limit(page_size).all()


        return  Pagination(count,page_index,page_size,items);



#---------笔记-----------
class CourseNoteDao():

    def get_or_404(self,id):

       return CourseNote.query.get_or_404(id)

    def delete(self,course_note):
        db.session.delete(course_note)
        db.session.commit()

    def save(self,course_note):
        db.session.add(course_note)
        db.session.commit()

    def find_user_notebooks_group_by_class(self,user_id):
        query  = db.session.query(CourseNote.id,CourseNote.class_id,Course.name,Course.img_url,CourseNote.created_time,func.count(CourseNote.class_id))\
            .join(Course,Course.id==CourseNote.class_id)\
            .group_by(CourseNote.class_id).filter(CourseNote.user_id == user_id)
        return query.all()

    def find_class_notes_by_user(self,class_id,user_id):
        return CourseNote.query.filter(CourseNote.user_id==user_id).filter(CourseNote.class_id == class_id).order_by(CourseNote.created_time.desc()).all()

    def findByClassId(self,class_id):

        return CourseNote.query.filter(CourseNote.class_id == class_id).order_by(CourseNote.created_time.desc()).all()



#---------评论-----------
class CourseCommentDao():

    def save(self,comment):
        db.session.add(comment)
        db.session.commit()

    def get_user_last(self,user_id):

        return CourseComment.query.filter(CourseComment.user_id==user_id)\
            .order_by(CourseComment.created_time.desc()).first()

    def find_class_id(self,class_id):
        return  CourseComment.query.filter(CourseComment.class_id==class_id).order_by(CourseComment.created_time.desc()).all()

    def pagetion(self,class_id,page_index,page_size):

        query = CourseComment.query.filter(CourseComment.class_id==class_id).order_by(CourseComment.created_time.desc())
        count =query.count()

        offset =0
        if(page_index > 1):
            offset = (page_index-1) * page_size


        items =query.offset(offset).limit(page_size).all()

        return (items,count)

#---------课件-----------
class ClassWareDao():

    def find_by_class_id(self,class_id):

        return CourseWare.query.filter(CourseWare.class_id==class_id).all()

#---------章节-----------
class ChapterDao():


    #根据ID获取章节
    def get(self,id):
       return Chapter.query.get(id)


    #获取课程所有章节
    def get_course_chapter(self,class_id):

        return Chapter.query.filter(Chapter.class_id==class_id).all()

#---------课时-----------
class LessonDao():

    def get(self,id):
       return Lesson.query.get(id)

    def get_or_404(self,id):
        return Lesson.query.get_or_404(id)

    def get_by_id_and_sort(self,id,sort):

        return Lesson.query.filter(Lesson.id==id).filter(Lesson.bsort==sort).first()



    def find_by_class_id(self,class_id):
        query = Lesson.query;
        query = query.join(Chapter,Chapter.id==Lesson.chapter_id)
        query = query.filter(Chapter.class_id==class_id)

        return  query.all()

#---------视频-----------
class VideoDao():

    def get(self,id):
        return Video.query.get(id)

#---------课程学习记录-----------
class CourseStudyDao():

    def save(self,study):
        db.session.add(study)
        db.session.commit()

    def get_class_study_progress_by_user(self,class_id,user_id):
        return CourseStudy.query.filter(CourseStudy.class_id==class_id,CourseStudy.user_id==user_id).first()


    def find_user_study_course(self,user_id,is_finish):
        return CourseStudy.query.filter(CourseStudy.is_finish==is_finish,
                                        CourseStudy.user_id==user_id)\
                                        .order_by(CourseStudy.start_time.desc())\
                                        .all()



    def get_user_study_course_count(self,user_id):
        return CourseStudy.query.filter(CourseStudy.user_id==user_id).count()

    def find_user_courses(self,courseids,user_id):
        return CourseStudy.query.filter(CourseStudy.class_id.in_(courseids),
                                        CourseStudy.user_id==user_id,
                                        ).all()


#---------课时播放记录-----------
class LessonPlayDao():
    def getLastPlay_by_Class(self,class_id):

        return LessonPlay.query.filter(LessonPlay.class_id==class_id)\
            .order_by(LessonPlay.play_time.desc()).first()

    def get_by_user_id(self,lesson_id,user_id):
        return LessonPlay.query.filter(LessonPlay.lesson_id==lesson_id,LessonPlay.user_id==user_id).order_by(LessonPlay.id.desc()).first()

    def save(self,play):
        db.session.add(play)
        db.session.commit()




class LessonStudyDao():

    def save(self,study):
        db.session.add(study)
        db.session.commit()



    def get_by_user_id(self,user_id,lesson_id):

       return LessonStudy.query.filter(LessonStudy.lesson_id==lesson_id,LessonStudy.user_id==user_id).first()


class CourseProductRelationDao():

    def find_user_order_course(self,user_id):

        query = CourseProductRelationship.query
        query = query.join(ProductOrder,and_(ProductOrder.product_id==CourseProductRelationship.product_id,
                                             ProductOrder.product_type==CourseProductRelationship.product_type))\
            .filter(ProductOrder.user_id==user_id)\
            .filter(ProductOrder.state==1)\
            .filter(ProductOrder.cancel_time>datetime.now())

        return query.all()




class CourseFavoritesDao():
    def find_user_favorites(self,user_id):
        return CourseFavorites.query.filter(CourseFavorites.user_id==user_id).order_by(CourseFavorites.created_time.desc()).all()


class CourseWareDownloadDao():
    def save(self,coursewear_down):
         db.session.add(coursewear_down)
         db.session.commit()

class ClassDrawsDao():

    def save(self,draws):
         db.session.add(draws)
         db.session.commit()

    def find_by_course(self,id):

        return ClassDraws.query.filter(ClassDraws.class_id==id).all()



class CourseTopicDao():
    def get(self,id):
        return CourseTopic.query.get(id);