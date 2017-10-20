# -*- coding: utf-8 -*-
from celery import Celery

from app import create_app, db
from app.util.HTMLSpider import JianshuSpider, LcodeSpider, SegmentfaultSpider, CSDNSpider


def make_celery(app=None):

    if app ==None:
        app=create_app('default')

    db.init_app(app)

    app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery()


@celery.task()
def task_get_article(site,url,user_id,forum_id):

    if site =='jianshu':
         JianshuSpider().get_article_detail(url,user_id,forum_id)

    elif site =='lcode':
        LcodeSpider().get_article_detail(url,user_id,forum_id)

    elif site =="segmentfault":

        SegmentfaultSpider().get_article_detail(url,user_id,forum_id)
    elif site=='csdn':

        CSDNSpider().get_article_detail(url,user_id,forum_id)






@celery.task()
def task_get_jinshu_articles(startpage,endpage):

    JianshuSpider().get_jianshu_articles(startpage,endpage)




@celery.task()
def task_get_lcode_articles(user_id,forum_id):
    LcodeSpider().getlist(user_id,forum_id)

