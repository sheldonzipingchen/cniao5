# -*- coding: UTF-8 -*-
import json
from datetime import datetime

from flask import render_template, request, jsonify, url_for
from flask.ext.login import current_user, login_required
from flask_restful import fields, marshal

from app.dao.class_dao import CourseStudyDao
from app.dao.product_dao import OrderDao
from app.dao.training_dao import TrainingClassDao, TrainUserDao, UserTrainStudyRecordDao, ClassTaskDao, TrainApplyDao
from app.dao.user_dao import UserDao
from app.models import  TrainUser, Order, TrainApply
from app.util.str_util import random_code
from . import train

__author__ = 'longo'


@train.route("/<int:id>")
def detail(id):

    training_class = TrainingClassDao().get(id);

    train_user_dao = TrainUserDao();

    ranks = train_user_dao.find_top10(training_class.id)

    is_join_class = False;
    train_user=None
    user_study_plan=None
    apply=None

    if current_user.is_authenticated():

        train_user = train_user_dao.get_by_class_id(training_class.id, current_user.id)

        if training_class.is_open==0:
            apply  = TrainApplyDao().get_user_apply_class(training_class.id,current_user.id)

        if train_user is not None:
            is_join_class = True
            user_study_plan =UserTrainStudyRecordDao().find_user_study_plan(current_user.id,training_class.id)

    return render_template("train/index.html",
                           training_class=training_class,
                           ranks=ranks,
                           train_user=train_user,
                           is_join_class=is_join_class,
                           user_study_plan=user_study_plan,
                           apply=apply)




@train.route("/android")
def android():


    # training_class = TrainingClassDao().get_android_training_class();

    # return url_for('train.detail',id=training_class.id)
    return detail(1)





@train.route("/class/applay/<int:id>")
@login_required
def join_apply(id):
    training_class = TrainingClassDao().get(id)

    return render_template("train/apply.html",training_class=training_class,user=current_user)






@train.route("/class/join", methods=['POST'])
@login_required
def join_train_class():
    json = request.get_json()

    class_id = json.get('class_id');

    training_class_dao = TrainingClassDao()
    training_class = training_class_dao.get(class_id);

    if training_class is None:
        return jsonify(result=False, message=u'???????????????')


    dao = TrainUserDao()
    train_user = dao.get_by_class_id(class_id, current_user.id)
    if train_user is not None:
        return jsonify(result=False, message=u'?????????????????????')

    train_user = TrainUser(class_id=class_id,
                           user_id=current_user.id,
                           created_time=datetime.now(),
                           ranking=0,
                           course_credit=0,
                           status=1)

    dao.save(train_user)


    UserTrainStudyRecordDao().save_record_with_tranining_class(training_class,current_user.id)

    training_class.total_students+=1
    training_class_dao.save(training_class)

    return jsonify(result=True,message=u'????????????')




@train.route("/user/current/module/<int:class_id>")
@login_required
def user_current_module(class_id):

    record =UserTrainStudyRecordDao().get_user_current_module(current_user.id,class_id)

    if record is None :

        return jsonify(result=False,message=u'??????????????????')


    return jsonify(result=True,id=record.module.id,title=record.module.title,target=record.module.target)



record_fields={

    'id':fields.Integer,
    'class_id':fields.Integer,
    'module_id':fields.Integer,
    'task_id':fields.Integer,
    'type':fields.Integer,
    'status':fields.Integer,
}



@train.route("/user/active/plan/<int:class_id>")
@login_required
def user_active_task(class_id):

     plan = UserTrainStudyRecordDao().find_user_activie_tasks(current_user.id,class_id)

     result = json.dumps(marshal(plan,record_fields))
     return result




#
#
# @login_required
# @train.route("/task/start",methods=['POST'])
# def task_start():
#
#     params = request.get_json();
#     id = params.get("id");
#     type = params.get("type");
#
#
#     task = ClassTaskDao().get(id);
#
#     if task is None:
#           return jsonify(result=False,code =-1,message=u'???????????????')
#
#     if task.status ==0:
#           return jsonify(result=False,code =-1,message=u'???????????????????????????,???????????????')
#
#     dao =UserTrainStudyRecordDao();
#
#     if type==3: #??????
#
#         record = dao.get_task_by_user(id,current_user.id)
#
#         if record is  None:
#            return jsonify(result=False,code =-1,message=u'???????????????')
#
#
#         tasks = dao.find_user_not_finish_prev_task(id,current_user.id)
#         if len(tasks)>0:
#             return jsonify(result=False,code =-1,message=u'???????????????????????????,????????????????????????????????????')
#
#
#         user_dao =UserDao();
#
#         user = user_dao.get(current_user.id)
#
#         #step1: ????????????,????????????
#
#         price=0
#         if record.task.pay_cur_type==1: #?????????
#
#             if user.balance<record.task.price:
#                 return jsonify(result=False,code =-1,message=u'????????????????????????,????????????,??????????????????')
#
#             user.balance = user.balance-record.task.price
#             price=record.task.price
#
#
#
#         elif record.task.pay_cur_type==0: #?????????
#             if user.coin<record.task.coin:
#                 return jsonify(result=False,code =-2,message=u'??????????????????,????????????. <a href="%s" target="_blank"> ???????????? </a> '%(url_for('member.invite',_external=True)))
#
#             user.coin = user.coin-record.task.coin
#             price = record.task.coin
#
#
#
#         user_dao.save(user) # ??????????????????
#
#         #step2: ????????????
#
#         title = '???????????? <%s>'%(record.task.title)
#
#         order_dao = OrderDao()
#
#         order_num = random_code(current_user.id,30)
#         order = Order(order_num=order_num,
#               title=title,
#               user_id=current_user.id,
#               product_id=record.task.id,
#               product_type=2, #??????
#               order_count=1,
#               coupon_id = 0,
#               day=record.claz.learn_days,
#               price=price,
#               total_price=price,
#               created_date = datetime.now(),
#               pay_channel='COIN',
#               trade_status ='TRADE_SUCCESS',
#               )
#
#         order_dao.create(order)
#
#
#         #step3: ????????????????????????
#         record.status=1; #??????????????????
#         record.reality_start_time=datetime.now()
#         dao.save(record)
#
#
#         #step4:????????????????????????
#         train_user_dao =TrainUserDao();
#         train_user =train_user_dao.get_by_class_id(record.class_id,current_user.id)
#         if train_user is not None:
#             train_user.current_task_id= record.id;
#             train_user_dao.save(train_user)
#
#
#         return jsonify(result=True,
#                        code =1,
#                        message=u'success',
#                        task_id=record.task.id,
#                        title=record.task.title,
#                        start_time = record.should_start_time,
#                        finish_time = record.should_finish_time)
#
#     elif type==2: #??????
#         pass
#

@train.route("/task/<int:id>/status")
@login_required
def task_status(id):

    record = UserTrainStudyRecordDao().get_task_by_user(id,current_user.id);

    if record is None:
        return jsonify(status=-1)

    return  jsonify(status = record.status)



@train.route("/task/<int:id>/prev/status")
@login_required
def task_prev_status(id):

    dao = UserTrainStudyRecordDao()

    tasks = dao.find_user_not_finish_prev_task(id,current_user.id)
    if len(tasks)>0:
        return jsonify(result=False)

    return jsonify(result=True)



@train.route("/task/<int:id>/finish")
@login_required
def task_finish(id):

    task = ClassTaskDao().get(id);

    if task is None:
        return jsonify(result=False,message=u'???????????????')


    courses= task.courses.all();
    course_ids = [];

    if len(courses)>0:
        for c in courses:
            course_ids.append(c.id)



    course_studys =CourseStudyDao().find_user_courses(course_ids,current_user.id)

    if len(course_studys)<=0: # ?????????????????????????????????
        return jsonify(result=False,message=u'?????????????????????????????????,??????????????????')

    else:

        for c in  course_studys:
            if c.is_finish==0: #???????????????????????????
               return jsonify(result=False,message=u'?????????????????????????????????,??????????????????')


    record_dao = UserTrainStudyRecordDao()
    record =  record_dao.get_task_by_user(id,current_user.id)


    if record is not None:

         #????????????
        record.reality_finish_time=datetime.now()

        if datetime.now() > record.should_finish_time:
            record.status=3 #??????????????????
            is_delay=True
        else:
            record.status=2 #??????????????????
            is_delay=False

            #????????????
            train_user_dao = TrainUserDao()
            train_user = train_user_dao.get_by_class_id(record.class_id,current_user.id)
            train_user.course_credit=train_user.course_credit + task.return_course_credit
            train_user_dao.save(train_user)

        record_dao.save(record)


               #step4:????????????????????????
        train_user_dao =TrainUserDao();
        train_user =train_user_dao.get_by_class_id(record.class_id,current_user.id)
        if train_user is not None:
            train_user.current_task_id= record.id;
            train_user_dao.save(train_user)



        return jsonify(result=True,
                       message=u'?????????,????????????',
                       task_id = task.id,
                       is_delay=is_delay,
                       return_course_credit=task.return_course_credit)




#=====================================================

@train.route('/apply/save', methods=[ 'POST'])
@login_required
def apply_save():


    json = request.get_json();
    class_id = json.get("class_id");


    dao = TrainApplyDao()

    train_apply = dao.get_user_apply_class(class_id,current_user.id)

    if train_apply is not None:

        return jsonify(result=False,message=u'???????????????????????????,???????????????,?????????????????????')




    real_name = json.get('real_name')
    qq = json.get('qq')
    company = json.get('company')
    mobi = json.get('mobi')
    email = json.get('email')
    work_year = json.get('work_year')




    train_apply = TrainApply(
                                class_id=class_id,
                                user_id=current_user.id,
                                username = current_user.username,
                                realname = real_name,
                                mobil=mobi,
                                qq=qq,
                                email=email,
                                created_time=datetime.now(),
                                company=company,
                                workyear=work_year,
                                status =0
                            )

    dao.save(train_apply)



    user_dao = UserDao()

    user = user_dao.get(current_user.id);

    if user.real_name is None or user.real_name=='':
        user.real_name=real_name

    if user.qq is None or user.qq=='':
        user.qq=qq

    if user.email is None or user.email=='':
        user.email=email

    if user.company is None or user.company=='':
        user.company=company

    if user.work_years is None or user.work_years=='':
        user.work_years=work_year


    user_dao.save(user)

    return jsonify(result=True,message=u'success')