# -*- coding: UTF-8 -*-

from . import thread
from datetime import datetime

from flask import request, url_for, jsonify, render_template
from flask.ext.login import current_user, login_required
from app.class_authority_util import user_course_authority

from app.dao.thread_dao import ThreadDao, ThreadPostDao
from app.models import Thread, UserMsg, ThreadPost
from .. dao.class_dao import CourseDao
from .. dao.user_dao import UserMessageDao



__author__ = 'Ivan'



@login_required
@thread.route("/course/question/create",methods=['POST'])
def thread_course_question_create():

    form = request.get_json()

    course_id = form.get("courseId")
    title = form.get('title')
    content = form.get('content')



    course_can_play =user_course_authority(int(course_id))

    if course_can_play == False:
        return jsonify(success=0,message=u'您还不是学员，没有权限提交问题')



    thread = Thread(title=title,
                    content=content,
                    class_id=course_id,
                    user_id=current_user.id,
                    ip_address=request.remote_addr,
                    created_time=datetime.now(),
                    read_count=1
                    )


    ThreadDao().save(thread)


    class_item = CourseDao().get_or_404(course_id)
    user_msg = UserMsg(title=u'有一个新提问',
               msg='尊敬的老师，%s课程，有一个新的提问，请及时去处理'%(class_item.name),
               from_user_id=9999,
               to_user_id=class_item.user_id,
               is_read=0
               )
    UserMessageDao().save(user_msg)

    return jsonify(success=1,message='success')


@thread.route("/course/question/<int:id>")
def thread_course_question_detail(id):

    thread =ThreadDao().get_or_404(id)

    course = CourseDao().get_or_404(thread.class_id)

    return  render_template("course/course_thread_detail.html",thread=thread,class_item = course)

