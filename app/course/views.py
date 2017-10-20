# -*- coding: UTF-8 -*-
from datetime import datetime

from flask import render_template, redirect, jsonify, request, url_for
from flask.ext.login import login_required, current_user
from flask.ext.restful import abort

from app import cache, cache_view_time
from . import course
from app.dao.user_dao import UserMessageDao
from .. dao.class_dao import LessonDao,  CourseDao, LessonPlayDao, CourseStudyDao, CourseCommentDao, \
    CourseWareDownloadDao, CourseTopicDao
from .. class_authority_util import  user_course_authority
from .. storage import q
from .. models import CourseWare, CourseWareDownload, ClassDraws, CourseComment, UserMsg


__author__ = 'Sheldon Chen'

PAGE_SIZE = 12
DEFAULT_VALUE=10000



@course.route('/')
@course.route('/page/<int:page_index>')

def index(page_index=1):

    order_by = request.values.get("order_by")
    if order_by==None or order_by=='':
        order_by=2
    else:
        try:
            order_by = int(order_by)

        except:
            order_by=2

    pagination = CourseDao().pagination(-1,order_by,page_index,PAGE_SIZE)
    return  render_template('course/index.html',pagination=pagination,order_by=order_by)





@course.route('/<int:id>')
def course_detail(id):

    class_item = CourseDao().get(id)
    if class_item.is_online==None or class_item.is_online==0:
        return abort(404)

    listDraws = ClassDraws.query.filter(ClassDraws.class_id == id).all()####实战课程图片list


    return render_template('course/course-detail.html',
                           class_item=class_item,
                           listDraws = listDraws, )



@course.route('/topic/<int:id>')
def course_topic(id):
    courses = CourseDao().find_topic_courses(id)

    topic = CourseTopicDao().get(id)
    return render_template("course/topic.html",courses=courses,topic=topic)

@course.route('/topic/pros')
def course_topic_projects():
    courses = CourseDao().find_topic_courses(1)
    topic = CourseTopicDao().get(1)
    return render_template("course/topic.html",courses=courses,topic=topic)

@course.route("/lessons/<int:id>")
def course_lessons(id):

    class_item = CourseDao().get_or_404(id)
    return render_template("course/course_lessons.html",
                              class_item=class_item,
                           )




@course.route('/comment/<int:id>', methods=['GET', 'POST'])
def course_comment(id):

    class_item = CourseDao().get_or_404(id)

    return render_template('course/course_comment.html',
                           class_item=class_item,

                           )


@course.route("/comment/create",methods=['POST'])
@login_required
def course_comment_create():

    json = request.get_json()

    course_id = json.get("course_id")
    score = json.get("score")
    content = json.get("content")


    can_play = user_course_authority(course_id)

    if can_play ==False:
        return jsonify(success=0,message=u'抱歉，您不是该课程的学员，暂无权限评价此课程')

    comment_dao = CourseCommentDao()

    comment =  comment_dao.get_user_last(current_user.id)

    if comment is not None :
        m = ((datetime.now() - comment.created_time).seconds) / 60
        if m < 1:
            return jsonify(success=0,message=u'休息一下再评价吧')



    comment = CourseComment(
        comment=content,
        score=score,
        created_time=datetime.now(),
        class_id=course_id,
        user_id=current_user.id
    )

    comment_dao.save(comment)

    course_dao = CourseDao()
    course = course_dao.get(course_id)
    if course is not None:
        course.comment_count = int(course.comment_count)+1

        user_msg = UserMsg(title=u'有一个新提问',
           msg='尊敬的老师，《%s》有一个新的评价，%s'%(course.name,url_for('course.course_comment',id=course_id,_external=True)),
           from_user_id=9999,
           to_user_id=course.user_id,
           )
        UserMessageDao().save(user_msg)


    return jsonify(success=1,message='success')



@course.route('/notes/<int:id>')
def course_notes(id):

    class_item = CourseDao().get_or_404(id)
    return render_template('course/course_notes.html',
                           class_item=class_item,

                           )


@course.route('/courseware/<int:id>')
def course_courseware(id):

    class_item = CourseDao().get_or_404(id)


    return render_template('course/course_courseware.html',
                           class_item=class_item,
                           # can_play = can_play,
                           # can_download=can_download,
                           # is_experience=is_experience
                           )

@course.route('/courseware/download/<int:id>')
@login_required
def courseware_download(id):



    coursewear =  CourseWare.query.get_or_404(id)


    can_play = user_course_authority(coursewear.class_id)

    if can_play ==False:
        return jsonify(success=0,message=u'抱歉，您不是该课程的学员，暂无权限下载课程源码')



    base_url = '%s//%s' % (coursewear.domain,coursewear.filekey)

    private_url = q.private_download_url(base_url, expires=3600)

    coursewear_down = CourseWareDownload(user_id = current_user.id,
                                             courseware_id = coursewear.id,
                                             download_time = datetime.now())
    CourseWareDownloadDao().save(coursewear_down)

    return redirect(private_url)




@course.route("/course/user/auth/<int:id>")
@login_required
def course_authority(id):



    can_play = user_course_authority(id)

    if can_play==False:

        return jsonify(can_play=can_play)


    course = CourseDao().get_or_404(id);
    total_lesson=course.lessons_count;



    class_study_progress=CourseStudyDao().get_class_study_progress_by_user(id,current_user.id);

    lesson_dao = LessonDao()
    course_lessons = lesson_dao.find_by_class_id(id);

    if class_study_progress is None:

        #判断当前课程是否有课时
        if len(course_lessons)<=0:
            return jsonify(can_play=can_play,
                           progress=0,
                           total_lesson=total_lesson,
                           )
        else:
            return jsonify(can_play=can_play,
                           progress=0,
                           total_lesson=total_lesson,
                           current_id=course_lessons[0].id,
                           current_name=course_lessons[0].name,
                           )
    else:

        progress = class_study_progress.progress
        last_play = LessonPlayDao().getLastPlay_by_Class(id)

        current_lesson = lesson_dao.get(last_play.lesson_id)

        return jsonify(can_play=can_play,
                           progress=progress,
                           total_lesson=total_lesson,
                           current_id=current_lesson.id,
                           current_name=current_lesson.name,
                           )




@course.route("/<int:id>/thread")
def course_thread(id):
    class_item = CourseDao().get_or_404(id)

    return render_template('course/course_thread.html',class_item=class_item)



@course.route("/<int:id>/thread/create",methods=['GET', 'POST'])
@login_required
def course_thread_create(id):

    class_item = CourseDao().get_or_404(id)
    return render_template('course/course_thread_create.html',class_item=class_item)





class UserClassProgress():
    def __init__(self,can_play,progress):

        self.can_play=can_play
        self.progress=progress