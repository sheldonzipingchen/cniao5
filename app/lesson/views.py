# -*- coding: UTF-8 -*-
from datetime import datetime
import os

from flask import render_template, redirect, url_for, jsonify, request
from flask.ext.login import login_required, current_user
from flask.ext.restful import abort
from . import lesson
from app.class_authority_util import lesson_authority
from app.clazz import videomgr
from ..dao.class_dao import LessonDao, CourseDao, LessonPlayDao, LessonStudyDao, CourseStudyDao, \
    CourseNoteDao
from ..storage import q
from ..models import LessonPlay, CourseNote, CourseStudy, LessonStudy




__author__ = 'Ivan'



@login_required
@lesson.route("/play/<int:lesson_id>.html")
def play(lesson_id):
    lesson_can_play, course_can_play = lesson_authority(lesson_id)

    lesson = LessonDao().get_or_404(lesson_id)
    course_dao = CourseDao()
    course = course_dao.get_by_chapter_id(lesson.chapter_id)

    if lesson_can_play == False:
        return render_template("lesson/buy-tip.html",course=course)



    return render_template("lesson/index.html", lesson=lesson,
                           course=course,
                           lesson_can_play=lesson_can_play,
                           course_can_play=course_can_play)




@lesson.route("/<int:id>/player")
@login_required
def player(id):

    lesson_can_play, course_can_play = lesson_authority(id)


    if lesson_can_play == False:
        return abort(404)

    lesson = LessonDao().get_or_404(id)

    if lesson.video.bucketname == 'cniao5-course-paid' or lesson.video.bucketname == 'cniao5-course-free':  # 视频源在七牛
        media_source = 'normal-video'
        token = ''
        video_url = build_video_url(lesson.video)

    else:
        media_source = 'baofeng-video'
        token, video_url = build_baofeng_play_url(lesson.video)

    return render_template("lesson/player.html", lesson=lesson, media_source=media_source,
                           video_url=video_url, token=token,lesson_can_play=lesson_can_play,course_can_play=course_can_play)


def build_baofeng_play_url(video):
    token = videomgr.create_player_token(video.filekey)
    url = 'servicetype=1&uid=%s&fid=%s&tk=%s&tltime=start_time&auto=1&fmatid=1' % (
        os.environ.get('BAO_FENG_USER_ID'), video.filekey, token)

    return token, url


@lesson.route("/play/begin/<int:course_id>")
@login_required
def play_first_lesson(course_id):
    lessons = LessonDao().find_by_class_id(course_id)

    if len(lessons) > 0:
        lesson_id = lessons[0].id
        return redirect(url_for("lesson.play", lesson_id=lesson_id))

    return abort(404)


@lesson.route("/play/try/<int:course_id>")
def play_try(course_id):
    lessons = LessonDao().find_by_class_id(course_id)

    if len(lessons) > 0:
        for l in lessons:
            if l.is_free == 1:
                return jsonify(success=1, lesson_id=l.id)

    return jsonify(success=0, lesson_id=0)


@lesson.route("/info/<int:id>")
@login_required
def lesson_info(id):
    lesson = LessonDao().get(id)

    lesson_can_play, course_can_play = lesson_authority(id)

    number = 0
    if lesson.bsort is not None:
        number = lesson.bsort

    return jsonify(
        id=lesson.id,
        chapterId=lesson.chapter_id,
        type='video',
        title=lesson.name,
        number=number,
        status=lesson.state,
        canLearn=lesson_can_play,
        mediaSource='self')


@lesson.route("/<int:id>/learn/status")
@login_required
def lesson_learn_status(id):
    lesson_study_dao = LessonStudyDao()
    lesson_study = lesson_study_dao.get_by_user_id(current_user.id, id)

    if lesson_study is None:

        return jsonify(status=0)  # 未开始学习

    else:
        return jsonify(status=lesson_study.status)



@lesson.route("/learn/start", methods=["POST"])
@login_required
def lesson_learn_start():
    json = request.get_json()
    course_id = json.get("course_id")
    lesson_id = json.get("lesson_id")

    ip = request.remote_addr

    lesson_play = LessonPlay(
        user_id=current_user.id,
        class_id=course_id,
        lesson_id=lesson_id,
        play_time=datetime.now(),
        start_position=0,
        position=0,
        lesson_duration=0,
        play_duration=0,
        is_finished=0,
        ip_addr=ip
    )

    LessonPlayDao().save(lesson_play)

    lesson_study_dao = LessonStudyDao()
    lesson_study = lesson_study_dao.get_by_user_id(current_user.id, lesson_id)

    if lesson_study is None:
        lesson_study = LessonStudy(

            user_id=current_user.id,
            class_id=course_id,
            lesson_id=lesson_id,
            start_time=datetime.now(),
            learn_time=0,
            status=1
        )

    lesson_study_dao.save(lesson_study)

    return jsonify(success=1)


@lesson.route("/<int:id>/learn/time", methods=["POST"])
# @login_required
def lesson_learn_time(id):


    if current_user.is_authenticated()==False:
        return  jsonify(success=-1,message="登录失效")

    json = request.get_json()

    currTime = json.get("currTime")
    learningCount = json.get("learningCount")

    lesson_play_dao = LessonPlayDao()

    lesson_play = lesson_play_dao.get_by_user_id(id, current_user.id)

    if lesson_play is None:
        return jsonify(success=0)

    lesson_play.position = currTime
    lesson_play.play_duration = lesson_play.play_duration + int(learningCount)

    lesson_play_dao.save(lesson_play)

    lesson_study_dao = LessonStudyDao()
    lesson_study = lesson_study_dao.get_by_user_id(current_user.id, id)

    if lesson_study is not None:
        lesson_study.learn_time = lesson_study.learn_time + int(learningCount)
        lesson_study_dao.save(lesson_study)

    return jsonify(success=1)



@lesson.route("/<int:id>/learn/finish", methods=["POST"])
@login_required
def lesson_learn_finish(id):
    lesson_play_dao = LessonPlayDao()
    lesson_play = lesson_play_dao.get_by_user_id(id, current_user.id)

    if lesson_play is None:
        return jsonify(success=0)

    lesson_play.end_time = datetime.now()
    lesson_play_dao.save(lesson_play)

    lesson_study_dao = LessonStudyDao()
    lesson_study = lesson_study_dao.get_by_user_id(current_user.id, id)

    if lesson_study is not None and lesson_study.status != 2:
        lesson_study.update_time = datetime.now()
        lesson_study.status = 2  # finished
        lesson_study_dao.save(lesson_study)

        course_study_dao = CourseStudyDao()

        classStudy = course_study_dao.get_class_study_progress_by_user(lesson_play.class_id, current_user.id)

        if classStudy is None:

            classStudy = CourseStudy(class_id=lesson_play.class_id,
                                     user_id=current_user.id,
                                     start_time=datetime.now(),
                                     progress=1,
                                     is_finish=False)

            course_study_dao.save(classStudy)

        else:

            if classStudy.is_finish==False:  #如果课程是为完成状态

                classStudy.progress = classStudy.progress + 1

                if classStudy.progress == classStudy.clazz.lessons_count: #当前进度和课程总课时一样说明学完了
                    classStudy.is_finish=True

                course_study_dao.save(classStudy)



    return jsonify(success=1)


@lesson.route("/<int:id>/learn/cancel", methods=["POST"])
@login_required
def lesson_learn_cancel(id):
    return jsonify(success=0)


def build_video_url(video):
    domain = video.domain
    video_url = "%s/%s" % (domain, video.filekey)
    if domain == 'http://video.cniao5.com':  # 是私有空间，需要生成token
        video_url = q.private_download_url(video_url, expires=video.duration)

    return video_url


@lesson.route('/note/save', methods=['POST'])
@login_required
def note_save():
    json = request.get_json()

    content = json.get('content')
    class_id = json.get('course_id')
    lesson_id = json.get('lesson_id')
    # is_open = json.get('is_share')
    # position = json.get('position')

    class_note = CourseNote(note=content,
                            created_time=datetime.now(),
                            class_id=class_id,
                            lesson_id=lesson_id,
                            user_id=current_user.id,
                            position=0,
                            is_open=1)

    CourseNoteDao().save(class_note)

    return jsonify(success=1)


