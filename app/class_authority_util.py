# -*- coding: UTF-8 -*-

from flask.ext.login import current_user

from app.dao.class_dao import CourseProductRelationDao, CourseDao, LessonDao
from app.dao.product_dao import ProductOrderDao
from app.dao.training_dao import UserTrainStudyRecordDao

__author__ = 'Ivan'



""" 课程播放权限 校验 （2016-03-18） """
def user_course_authority(course_id):

    can_play =False

    #未登录
    if not current_user.is_authenticated():
        return can_play

    if current_user.is_super_admin(): #超级管理员
        return True;

    courseDao = CourseDao();
    course = courseDao.get(course_id)

    if course is None:
        return False


    # course_ids=[]

    if course.user_id == current_user.id: #如果课程的讲师和当然登录用户的ID一样，则有权限
        return True

    if course.is_free == 1: #免费课程
       return  True

    # elif course.types==3: #就业课程
    #     course_ids = get_user_task_courses(user_id=current_user.id)

    else:
        course_ids = get_user_order_courses(current_user.id)

    return (course_id in course_ids)


def user_course_authority_course_api(course_id,user_id):



    can_play =False

    if user_id==None:
        return  can_play

    try:
        user_id = int(user_id)
    except:
        return can_play


    courseDao = CourseDao();
    course = courseDao.get(course_id)

    if course is None:
        return False


    else:
        course_ids = get_user_order_courses(user_id)

    return (course_id in course_ids)



# 校验课时的播放权限
def lesson_authority(lesson_id):




    course_dao = CourseDao();
    course = course_dao.get_by_lesson_id(lesson_id)

    if course == None:
        return False





    course_can_play = user_course_authority(course.id)

    if course_can_play: # 如果课程都有权限，那这个课程下面所有的课时都有权限

        lesson_can_play=True
        return lesson_can_play,course_can_play
    else:
        lesson_dao = LessonDao()
        lesson = lesson_dao.get_or_404(lesson_id)

        if lesson.is_free ==True: # 课时可以免费试看
            lesson_can_play=True
            return lesson_can_play,course_can_play
        else:
            lesson_can_play=False
            return lesson_can_play,course_can_play












#------- 查询出所有有权限的课程 ---------
def get_user_order_courses(user_id):

    course_ids=[];
    course_products= CourseProductRelationDao().find_user_order_course(user_id);
    if len(course_products)>0:
        for c in course_products:
            course_ids.append(c.class_id)


    course_product_orders =ProductOrderDao().find_user_course_product_order(user_id)

    if len(course_product_orders)>0:
        for c in course_product_orders:
            course_ids.append(c.product_id)

    return  course_ids



#------- 查询出用户有权限任务下的所有课程 ---------
def get_user_task_courses(user_id):

    course_ids=[];
    dao =UserTrainStudyRecordDao()

    task_records = dao.find_user_all_activie_tasks(user_id)

    if len(task_records)>0:

        for t in task_records:

            for c in t.task.courses:
                course_ids.append(c.id)



    return  course_ids;