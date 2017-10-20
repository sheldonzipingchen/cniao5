# -*- coding: UTF-8 -*-
import datetime

from app import db
from ..models import TrainingClass, TrainUser, ClassModule, \
    UserTrainStudyRecord, ClassTask, TrainApply

__author__ = 'Ivan'



class TrainingClassDao():


    def save(self,cla):
        db.session.add(cla)
        db.session.commit()

    def get(self,id):
        return TrainingClass.query.get(id)

    def find_all(self):
        return TrainingClass.query.filter(TrainingClass.status==1).all()


    def get_by_type(self,type):
        return TrainingClass.query.filter(TrainingClass.status==1,TrainingClass.type==type).first()

    def get_android_training_class(self):
        return self.get_by_type('android')


class TrainApplyDao():

    def save(self,apply):
        db.session.add(apply)
        db.session.commit()


    def get_user_apply_class(self,class_id,user_id):
        return TrainApply.query.filter(TrainApply.class_id==class_id,TrainApply.user_id==user_id).first()


class TrainUserDao():

    def get_by_class_id(self,class_id,user_id):

        return TrainUser.query.filter(TrainUser.user_id==user_id,TrainUser.class_id==class_id).first()

    def find_top10(self,class_id):
        return TrainUser.query.filter(TrainUser.class_id==class_id).order_by(TrainUser.course_credit.desc()).limit(10).all()


    def save(self,train_user):
        db.session.add(train_user)
        db.session.commit()


class ClassModuleDao():

    def find_by_class_id(self,class_id):
        return ClassModule.query.filter(ClassModule.class_id==class_id).all()


class ClassTaskDao():
    def get(self,id):
        return ClassTask.query.get(id)



class UserTrainStudyRecordDao():

    def save(self,record):
        db.session.add(record)
        db.session.commit()

    def save_record_with_tranining_class(self,tranin_class,user_id):

        if tranin_class is None:
            return


        date_now = datetime.datetime.now()
        record = UserTrainStudyRecord(class_id=tranin_class.id,
                                      module_id=0,
                                      task_id=0,
                                      user_id=user_id,
                                      should_start_time=date_now,
                                      should_finish_time=date_now+datetime.timedelta(days=tranin_class.learn_days),
                                      reality_start_time=date_now,
                                      type=1,
                                      status=1
                                      )

        self.save(record) #保存课程


        should_start_time=None
        should_finish_time=None
        task_should_start_time=None
        task_should_finish_time=None

        for i in range(len(tranin_class.modules)) :

            m = tranin_class.modules[i]

            if i ==0:
                should_start_time=date_now
                should_finish_time=should_start_time+datetime.timedelta(days=m.learn_days)

            else:
                should_start_time= should_finish_time
                should_finish_time=should_start_time+datetime.timedelta(days=m.learn_days)


            record = UserTrainStudyRecord(
                             class_id=tranin_class.id,
                              module_id=m.id,
                              task_id=0,
                              user_id=user_id,
                              should_start_time=should_start_time,
                              should_finish_time=should_finish_time,
                              type=2,
                              status=0
                              )

            self.save(record)  # 保存模块



            for j in range(len(m.tasks)):

                t = m.tasks[j]

                if i==0 and j==0:

                   task_should_start_time = date_now
                   task_should_finish_time=task_should_start_time+datetime.timedelta(days=t.max_study_days)

                else:

                   task_should_start_time= task_should_finish_time
                   task_should_finish_time=task_should_start_time+datetime.timedelta(days=t.max_study_days)


                record = UserTrainStudyRecord(
                             class_id=tranin_class.id,
                              module_id=m.id,
                              task_id=t.id,
                              user_id=user_id,
                              should_start_time=task_should_start_time,
                              should_finish_time=task_should_finish_time,
                              type=3,
                              status=0
                              )

                self.save(record)  # 保存任务

    def get_user_current_module(self,user_id,class_id):

        return UserTrainStudyRecord.query.filter(UserTrainStudyRecord.class_id==class_id,
                                                 UserTrainStudyRecord.user_id==user_id,
                                                 UserTrainStudyRecord.type==2,
                                                 UserTrainStudyRecord.status==1).order_by(UserTrainStudyRecord.id.desc()).first()

    def get_module_by_user(self,module_id,user_id):

        return UserTrainStudyRecord.query.filter(
                                                 UserTrainStudyRecord.user_id==user_id,
                                                 UserTrainStudyRecord.module_id==module_id,
                                                 UserTrainStudyRecord.type==2
                                                ).first()


    def find_user_task_by_module(self,module_id,user_id):

        return UserTrainStudyRecord.query.filter(
                                         UserTrainStudyRecord.user_id==user_id,
                                         UserTrainStudyRecord.module_id==module_id,
                                         UserTrainStudyRecord.type==3
                                        ).all()


    def get_task_by_user(self,task_id,user_id):

         return UserTrainStudyRecord.query.filter(
                                         UserTrainStudyRecord.user_id==user_id,
                                         UserTrainStudyRecord.task_id==task_id,
                                         UserTrainStudyRecord.type==3
                                        ).first()


    def find_user_study_plan(self,user_id,class_id):

        return UserTrainStudyRecord.query.filter(UserTrainStudyRecord.class_id==class_id,
                                                 UserTrainStudyRecord.user_id==user_id,
                                                 UserTrainStudyRecord.type==3,
                                                 ).all()


    def find_user_activie_tasks(self,user_id,class_id):

        return UserTrainStudyRecord.query.filter(UserTrainStudyRecord.class_id==class_id,
                                                 UserTrainStudyRecord.user_id==user_id,
                                                 UserTrainStudyRecord.status!=0,
                                                 ).all()


    def find_user_all_activie_tasks(self,user_id):

            return UserTrainStudyRecord.query.filter(
                                            UserTrainStudyRecord.type==3,
                                             UserTrainStudyRecord.user_id==user_id,
                                             UserTrainStudyRecord.status!=0,
                                             ).all()


    def find_user_not_finish_prev_task(self,cur_task_id,user_id):

        record = self.get_task_by_user(cur_task_id,user_id)

        query =  UserTrainStudyRecord.query.filter(
                                            UserTrainStudyRecord.type==3,
                                             UserTrainStudyRecord.user_id==user_id,
                                            UserTrainStudyRecord.class_id==record.class_id,
                                            UserTrainStudyRecord.should_finish_time<=record.should_start_time,
                                             UserTrainStudyRecord.status==0,
                                             )

        return  query.all()
