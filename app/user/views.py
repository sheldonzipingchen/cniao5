# -*- coding: utf-8 -*-
import json

from flask import render_template,redirect, jsonify, url_for
from flask.ext.login import login_required, current_user
from flask.ext.restful import abort, marshal
from flask.ext.restful import fields

from app.dao.class_dao import CourseStudyDao, CourseDao
from app.dao.thread_dao import ThreadDao
from app.dao.user_dao import UserDao
from app.openapi.common_fields import user_fields
from app.openapi.utils import DateFormat
from . import user


@user.route("/<int:id>")
def detail(id):
    user = get_user(id)
    if user is None:
        return abort(404)


    return render_template("user/index.html",user=user)



@user.route("/<int:id>/followers")
def followers(id):
    user = get_user(id)
    if user is None:
        return abort(404)

    followers = UserDao().find_user_followers(user.id)
    return render_template("user/followers.html",user=user,followers=followers)



@user.route("/<int:id>/following")
def following(id):
    user = get_user(id)
    if user is None:
        return abort(404)

    followings = UserDao().find_user_following(user.id)
    return render_template("user/following.html",user=user,following=followings)



@user.route("/thread/write")
@login_required
def thread_write():
    return  render_template("forum/write.html",forum_id=id,thread={},action='create',thread_type=0)

@user.route("/<int:id>/threads")
def threads(id):
    return  redirect(url_for('user.detail'))

@user.route("/<int:id>/follow",methods=["POST"])
@login_required
def follow(id):

    dao = UserDao()
    target_user = dao.get(id);
    me=dao.get(current_user.id)
    target_user.follow_user(me)

    return jsonify(success=True,message='succes')

@user.route("/<int:id>/unfollow",methods=["POST"])
@login_required
def unfollow(id):
    dao = UserDao()
    target_user = dao.get(id);
    me=dao.get(current_user.id)
    target_user.unfollow_user(me)

    return jsonify(success=True,message='succes')


@user.route("/<int:id>/follow/status")
@login_required
def follow_status(id):
    dao = UserDao()
    target_user = dao.get(id);
    me=dao.get(current_user.id)

    return jsonify(success=target_user.is_my_follower(me))


@user.route("/<int:id>/public/info")
def user_public_info(id):
    user =UserDao().get(id);
    if user is None:
        return  jsonify(success=False,message=u'用户不存在')

    thread_count = ThreadDao().get_user_thread_count(id);
    study_course_count = CourseStudyDao().get_user_study_course_count(id)
    return jsonify(
                user_id = user.id,
                user_name=user.username,
                user_logo = user.logo_url,
                user_desc = user.desc,
                user_type=user.user_type,
                followed=user.following_count,
                followers=user.follower_count,
                thread_count=thread_count,
                study_course_count=study_course_count)





course_fields={

    'id':fields.Integer,
    'name':fields.String,
    'img_url':fields.String,
    'lessons_played_time':fields.Integer,
    'comment_count':fields.Integer,
    "now_price":fields.Float,
    'created_time':DateFormat(attribute='created_time'),

}

course_fields['teacher']=fields.Nested(user_fields)


@user.route("/<int:id>/course/teach/<int:limit>")
def user_teach_course(id,limit):
     user =UserDao().get(id);

     if user is None:
        return  jsonify(success=False,message=u'用户不存在')

     if not user.is_teacher():
          return  jsonify(success=False,message=u'该用户不是老师')


     courses = CourseDao().find_user_teach_courses(user.id,limit)

     result = json.dumps(marshal(courses,course_fields))

     return result





@user.route("/<int:id>/course/learn/<int:limit>")
def user_learn_course(id,limit):
    user =UserDao().get(id);

    if user is None:
        return  jsonify(success=False,message=u'用户不存在')

    courses = CourseDao().find_user_learn_courses(user.id,limit)

    result = json.dumps(marshal(courses,course_fields))

    return result




thread_fields={

    'id':fields.Integer,
    'title':fields.String,
    'read_count':fields.Integer,
    'is_hot':fields.Integer,
    'is_top':fields.Integer,
    "reply_count":fields.Integer,
    'created_time':DateFormat(attribute='created_time'),

}

thread_fields['user']=fields.Nested(user_fields)




@user.route("/<int:id>/thread/<int:limit>")
def user_thread(id,limit):

    threads =ThreadDao().find_user_threads(id,limit)
    result = json.dumps(marshal(threads,thread_fields))

    return result




def get_user(id):

    user = UserDao().get(id)
    if user is None:
        return None

    thread_count = ThreadDao().get_user_thread_count(id);

    user.thread_count = thread_count

    return user