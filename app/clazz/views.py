# -*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for, Response

from . import clazz

from app.clazz import videomgr
from .. models import  Lesson, Course


__author__ = 'longo'



@clazz.route('/yaya.html')
def clazz_yaya():
    return redirect(url_for('course.course_detail', id=10073L))

@clazz.route('/weibo.html', methods=['GET', 'POST'])
def clazz_weibo():
    return redirect(url_for('course.course_detail', id=10075L))

@clazz.route('/news.html', methods=['GET', 'POST'])
def clazz_news():

    return redirect(url_for('course.course_detail', id=10076L))




#
## 实战课程列表
#
@clazz.route('/projects', methods=['GET'])
def pro_courses():
   return  redirect(url_for("course.course_topic_projects"))



@clazz.route('/view/<int:id>.html')
def class_view(id):

    return  redirect(url_for('course.course_detail',id=id))




@clazz.route('/get_token/<int:lesson_id>')
def get_token(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id) ##课时info
    token = videomgr.create_token(lesson.video.filekey, '9919P8Ql1srb9d649XqXYbZ3bU0RBkyntY1TKJzA', 'sR49P8Ql1I3d9dXEeXqXYbFD3oi1ZGPWCcdQ2UjV')
    return  token




