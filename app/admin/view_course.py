# -*- coding: UTF-8 -*-
from flask import render_template, request,redirect, url_for, flash, jsonify
from flask.ext.login import current_user, logout_user, login_user, login_required

from app.dao.class_dao import CourseDao, ClassDrawsDao
from app.dao.user_dao import UserDao
from app.models import ClassDraws
from . import admin

__author__ = 'Ivan'






@admin.route('/courses.html')
@login_required
def courses():

    page_index = request.args.get("page_index");
    if page_index==None or page_index=='':
        page_index =1;

    try:
         page_index =int(page_index)
    except:
         page_index=1

    pagination  = CourseDao().get_all(page_index,10);
    return  render_template("admin/course/index.html",pagination=pagination)




@admin.route('/course/<int:id>/desc')
@login_required
def courser_desc(id):
    course = CourseDao().get(id)

    return  render_template("admin/course/desc.html",course=course)


@admin.route('/course/<int:id>/pics')
@login_required
def courser_pics(id):

    imgs = ClassDrawsDao().find_by_course(id)
    return render_template("admin/course/pic-list.html",course_id=id,imgs=imgs)


@admin.route('/course/draw/save',methods=['POST'])
@login_required
def course_draw_save():
    json = request.get_json()
    course_id = json.get("course_id");
    img_url = json.get("img_url");

    cd = ClassDraws(class_id=course_id,img_url=img_url)

    ClassDrawsDao().save(cd)

    return jsonify(success=1)



@admin.route("/course/update/field",methods=["POST"])
@login_required
def course_update_field():


    json = request.get_json()
    course_id = json.get("course_id");
    action = json.get("action");
    val = json.get("val");


    course_dao = CourseDao()

    course = course_dao.get(course_id)

    if course ==None:
        return jsonify(success=0,message=u'课程不存在')



    if action=='can_buy':
        course.can_buy = val

    elif action=='can_use_coupon':
        course.can_use_coupon = val

    elif action=='now_price':
        course.now_price = val

    elif action=='cost_price':
        course.cost_price = val

    elif action=='name':
        course.name = val


    elif action=='lessons_count':
        course.lessons_count = val

    elif action=='lessons_finished_count':
        course.lessons_finished_count = val


    elif action=='desc':
        course.desc = val


    course_dao.save(course)

    return jsonify(success=1,message=u'修改成功')


@admin.route("/course/config")
@login_required
def course_config():
    pass


