# -*- coding: UTF-8 -*-
from flask import render_template
from flask.ext.login import login_required, current_user

from . import member
from app.dao.class_dao import CourseStudyDao, CourseFavoritesDao

__author__ = 'Ivan'



@member.route('/my/course/learning')
@login_required
def course_learning():

    course_study_list = CourseStudyDao().find_user_study_course(current_user.id,False)
    return render_template('member/course/course_learning.html',course_study_list=course_study_list)



@member.route('/my/course/done')
@login_required
def course_done():
    course_study_list = CourseStudyDao().find_user_study_course(current_user.id,True)
    return render_template('member/course/course_done.html',course_study_list=course_study_list)



@member.route('/my/course/fav')
@login_required
def course_fav():

    course_favorites = CourseFavoritesDao().find_user_favorites(current_user.id);
    return render_template('member/course/course_fav.html',course_favorites=course_favorites)
