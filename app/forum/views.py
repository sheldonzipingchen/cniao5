# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import render_template, jsonify, request
from flask.ext.login import login_required, current_user
from flask.ext.restful import abort, marshal

from app.class_authority_util import user_course_authority
from app.dao.thread_dao import ForumDao, ThreadDao, ForumThreadRelationDao, ThreadPostDao, ThreadLikeDao, \
    ThreadRequestDao
from app.dao.user_dao import UserDao
from app.forum.util import is_forum_admin
from app.models import Thread, ForumThreadRelation, ThreadPost, ThreadLike, ThreadRequest
from app.user.views import thread_fields
from app.util.HTMLSpider import ThreadHtmlPareser
from tasks import  task_get_article,task_get_jinshu_articles, task_get_lcode_articles
from . import forum

__author__ = 'Ivan'



#
# @forum.route("/<int:forum_id>/spider/jianshu/one/<string:id>")
# @login_required
# def jianshu_spider(forum_id,id):
#     task = task_get_article.delay(id,current_user.id,forum_id)
#     return jsonify(task=task.id)
#
# @forum.route("/spider/jianshu/list/<int:start>/<int:end>")
# @login_required
# def jianshu_list_spider(start,end):
#     if current_user.is_super_admin():
#         task = task_get_jinshu_articles.delay(start,end)
#         return jsonify(task=task.id)
#
#     return jsonify(message=u"无权限")
#
#
# @forum.route("/<int:forum_id>/spider/lcode/list")
# @login_required
# def lcode_spider(forum_id):
#
#     task=task_get_lcode_articles.delay(current_user.id,forum_id)
#
#     return jsonify(task=task.id)


@forum.route("/spider",methods=["POST"])
@login_required
def spider():

    params = request.get_json();

    forum_id = params.get("forum_id")
    site = params.get("site")
    url = params.get("url")

    task = task_get_article.delay(site,url,current_user.id,forum_id)

    return jsonify(success=1,task=task.id)





@forum.route("/")
def index():

    list =UserDao().find_top10_thread_writer()
    forums = ForumDao().find_all()

    is_admin=False
    if current_user.is_authenticated():
        is_admin=current_user.is_super_admin()

    return render_template("forum/index.html",forums=forums,forum_id=0,top_writer=list,is_admin=is_admin)

@forum.route("/<int:id>")
def detail(id):

    dao =ForumDao()
    forum = dao.get(id);

    if forum is None:
        return  abort(404)

    forums = ForumDao().find_all()
    list =UserDao().find_top10_thread_writer()
    return render_template("forum/index.html",forums=forums,forum_id=forum.id,top_writer=list,is_admin=is_admin(forum))

    # return render_template('forum/detail.html',forum=forum,is_admin=is_admin(forum),forums=dao.find_all())



@forum.route("/<int:id>/hot/thread")
def forum_hot_thread(id):

     threads = ThreadDao().find_forum_hot_threads(id,10)
     result = json.dumps(marshal(threads,thread_fields))

     return result



############################投稿模块####################################################

@forum.route("/<int:id>/thread/submit")
@login_required
def forum_thread_submit(id):
     return render_template('forum/submit.html',forum_id = id)


@forum.route("/<int:id>/thread/submit/result")
@login_required
def forum_thread_submit_result(id):
    return render_template('forum/submit-result.html',forum_id = id)


@forum.route("/thread/submit/request",methods=['POST'])
@login_required
def forum_thread_submit_request():

    json = request.get_json();
    title = json.get("title")
    url = json.get("url")
    thread_id = json.get("threadId")
    forum_id = json.get("forumId")


    thread_dao =ThreadDao();
    thread = thread_dao.get(thread_id)
    if thread is None:
        return jsonify(success=True,message=u'文章不存在')

    forum_dao =ForumDao()

    forum = forum_dao.get(forum_id)

    if forum is None:
        return jsonify(success=True,message=u'栏目不存在')



    auth = is_admin(forum)
    if auth:
        relation = ForumThreadRelation(forum_id=forum_id,thread_id=thread_id,created_time=datetime.now())
        ForumThreadRelationDao().save(relation)

    else:
        thread_request =  ThreadRequest(title=title,url=url,
                                        thread_id=thread_id,
                                        forum_id=forum_id,
                                        request_user_id=current_user.id,
                                        request_time=datetime.now(),
                                        status=0)

        ThreadRequestDao().save(thread_request)

    return jsonify(success=True)



############################文章模块####################################################

@forum.route("/thread/<int:id>")
def thread_detail(id):

    thread_dao = ThreadDao()
    thread = thread_dao.get(id)

    if thread is None:
        return abort(404);



    auth=False
    if current_user.is_authenticated(): #已经登录
        auth = current_user.is_super_admin() or (current_user.id==thread.user_id)
        if auth:
            content = thread.content #管理员或者作者本人直接显示原始内容
        else:
            post_count=ThreadPostDao().get_thread_user_post_count(current_user.id,thread.id)
            if post_count>0:
                content = thread.content
            else:
                content = ThreadHtmlPareser().show(thread.content)
    else:
        content = ThreadHtmlPareser().show(thread.content)

    thread_count = thread_dao.get_user_thread_count(thread.user_id)
    return render_template("forum/thread-detail.html",thread=thread,auth=auth,thread_count=thread_count,content=content)


@forum.route("/<int:id>/thread/write")
@login_required
def thread_write(id):
    thread={}
    return render_template("forum/write.html",forum_id=id,thread=thread,action='create',thread_type=1)


@forum.route("/thread/<int:id>/update")
@login_required
def thread_update(id):
    thread = ThreadDao().get(id)
    return render_template("forum/write.html",thread=thread,action='update')


@forum.route("/thread/create",methods=['POST'])
@login_required
def thread_create():

    form = request.get_json()


    title = form.get('title')
    content = form.get('content');
    brief = form.get("brief")
    is_original = form.get("is_original")
    thread_type = form.get("thread_type")


    if thread_type==1:

        forum_id = form.get("forumId")
        forum_dao = ForumDao()
        forum = forum_dao.get(forum_id)

        if forum.is_normal_forum()==False: #普通板块

            is_admin=is_forum_admin(current_user.id,forum.admins)
            if is_admin==False:
                return jsonify(result=False,message=u'您暂无权限发表文章')


    htmlparser = ThreadHtmlPareser()
    htmlparser.pasert(content)

    img_links=None
    if  len(htmlparser.imgs)>0:
        img_links = ",".join(htmlparser.imgs)


    thread_dao = ThreadDao()

    thread = Thread(
                title=title,
                content=content,
                imgs=img_links,
                user_id=current_user.id,
                ip_address=request.remote_addr,
                created_time=datetime.now(),
                read_count=1,
                is_original=is_original,
                brief=brief,
                status =1,
                thread_type=thread_type
                )

    thread_dao.save(thread)


    if thread_type==1: # 在栏目里面发帖才保存中间表
        #保存中间表
        relation= ForumThreadRelation(forum_id=forum_id,thread_id=thread.id,
                                      created_time=datetime.now())
        ForumThreadRelationDao().save(relation)
        #数量加1
        forum.thread_count+=1
        forum_dao.save(forum)



    return  jsonify(result=True,message='success')


@forum.route("/thread/modify",methods=['POST'])
@login_required
def thread_modify():
    form = request.get_json()

    thread_id = form.get("threadId")
    title = form.get('title')
    content = form.get('content')
    brief = form.get("brief")
    is_original = form.get("is_original")

    thread_dao = ThreadDao()

    thread = thread_dao.get(thread_id)

    if thread is None:
        return jsonify(result=False,message='文章不存在')

    auth = current_user.is_super_admin() or (current_user.id==thread.user_id)

    if auth==False:
        return jsonify(result=False,message='无权限修改')


    thread.title=title
    thread.content=content
    thread.brief=brief
    thread.is_original=is_original
    thread.last_update_time=datetime.now()

    thread_dao.save(thread)

    return jsonify(result=True,message='success')


@forum.route("/thread/read/<int:id>")
def thread_read(id):

     thread = ThreadDao().get(id)

     thread.read_count += 1
     ThreadDao().save(thread)

     return jsonify(success=1,message='success')

@forum.route("/thread/delete/<int:id>",methods=['POST'])
@login_required
def thread_delete(id):

    dao =ThreadDao();
    thread = dao.get(id)

    auth = current_user.is_super_admin() or (current_user.id==thread.user_id)

    if auth==False:
        return jsonify(success=0,message='无权限删除')

    thread.status =-1;
    dao.save(thread)

    return jsonify(success=1,message='success')


############# 评论 ###########

@forum.route("/thread/post/create",methods=['POST'])
@login_required
def thread_post_create():

    json = request.get_json()

    course_id = json.get("courseId")
    thread_id = json.get('threadId')
    content = json.get('content')


    if course_id >0:
        course_id = int(course_id)
        course_can_play =user_course_authority(course_id)


        if course_can_play == False:
            return jsonify(success=0,message=u'您还不是学员，没有权限提交问题')



    thread_post = ThreadPost(content=content,
                             thread_id=thread_id,
                             class_id=course_id,
                             user_id=current_user.id,
                             ip_address=request.remote_addr,
                             created_time=datetime.now(),
                             status=1)

    ThreadPostDao().save(thread_post)

    thread_dao = ThreadDao();

    thread = thread_dao.get_or_404(thread_id)
    thread.last_comment_time = datetime.now()
    thread.reply_count += 1

    thread_dao.save(thread)

    return jsonify(success=1,message='success')


@forum.route("/thread/post/delete/<int:id>",methods=['POST'])
@login_required
def thread_post_del(id):

    dao = ThreadPostDao()

    post = dao.get(id)
    if post.user_id !=current_user.id:
        return jsonify(success=0,message='无权限删除')


    dao.delete(post)

    return jsonify(success=1,message='success')



############################文章喜欢模块####################################################

@forum.route("/thread/<int:id>/like",methods=['POST'])
@login_required
def thread_like(id):


    thread_dao =ThreadDao();

    thread = thread_dao.get(id)

    if thread is None:
        return jsonify(success=False,message=u'文章不存在')




    like_dao = ThreadLikeDao()
    like = like_dao.get_by_user_thread(current_user.id,id)

    if like is not None:
        return jsonify(success=False,message=u'')



    like = ThreadLike(thread_id=id,user_id=current_user.id,ip_address=request.remote_addr,created_time=datetime.now())
    like_dao.save(like)

    thread.like_count+=1;

    if thread.is_hot==False and thread.like_count>20:
        thread.is_hot=True

    thread_dao.save(thread)

    return jsonify(success=True,message=u'success')


@forum.route("/thread/<int:id>/like/status")
@login_required
def thread_like_status(id):
    like_dao = ThreadLikeDao()
    like = like_dao.get_by_user_thread(current_user.id,id)

    if like is not None:
        return jsonify(success=True,message=u'success')

    return jsonify(success=False,message=u'')




@forum.route("/<int:forum_id>/thread/<int:thread_id>/hot/setting",methods=['POST'])
def thread_hot_setting(forum_id,thread_id):
    thread = ThreadDao().get(thread_id)

    if thread is None:
        return jsonify(success=0,message='thread not exist')

    if thread.is_hot==1:
        thread.is_hot=0
    else:
        thread.is_hot=1

    ThreadDao().save(thread)

    return jsonify(success=1,message='')





def is_admin(forum):
    is_admin=False
    if current_user.is_authenticated():
        is_admin=is_forum_admin(current_user.id,forum.admins)

    return is_admin
