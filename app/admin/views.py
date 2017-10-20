# -*- coding: UTF-8 -*-
import json
import multiprocessing
import sys
import threading
import uuid
from datetime import datetime

from flask import current_app, flash, render_template, redirect, request, url_for, jsonify
from flask.ext.login import login_user, login_required, logout_user, current_user
from flask.ext.restful import marshal
from itsdangerous import base64_encode

from app import models
from app.dao.banner_dao import BannerDao
from app.dao.class_dao import CourseDao
from app import db
from app.dao.user_dao import UserDao, TeacherDao
from app.openapi.common_fields import user_fields
from . import admin
from .forms import NewProductForm, AdminLoginForm, \
    NewChapterForm, UploadLessonForm, NewQQGroupForm, NewClassTypeForm, \
    NewSecondClassTypeForm, NewFriendLinkForm
from ..dao.email_user_dao import EmailUserDao
from ..models import User, ProductVIP, Course, Chapter, Lesson, Compilation, ClassType, ClassTypeEncoder, \
    CourseProductRelationship, QQGroup, Banner, FriendLink, CourseWare, UserMsg, Teacher
from .. send_cloud import send_cloud_trigger
from .. util.email_message import send_email_use_html, send_email_template_group

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'Sheldon Chen'




@admin.route('/index.html')
@login_required
def index():
    """
    管理后台首页
    """
    return render_template('admin/index.html')



@admin.route('/banners.html')
@login_required
def banners():
    banner_list = BannerDao().find_all()
    return  render_template("admin/banner/index.html",banners=banner_list)


@admin.route("/banner/update",methods=["POST"])
@login_required
def banner_update():

    params = request.get_json();

    id = params.get("id")
    action = params.get("action")
    val = params.get("val");


    banner = BannerDao().get(id)
    if banner==None:
        return jsonify(success=0,message=u'banner 不存在')

    if action=='color':
        banner.bg_color=val

    elif action=='state':
        banner.state=val

    elif action=='order_num':
        banner.order_num=val

    BannerDao().save(banner)



    if action=='delete':
        BannerDao().delete(banner)



    return  jsonify(success=1,message=u'修改成功')

@admin.route('/banner/add.html')
@login_required
def banner_add():
    return render_template("admin/banner/add.html")



@admin.route('/banner/save',methods=["POST"])
@login_required
def banner_save():

    params = request.get_json();
    redirect_url=params.get("redirect_url")
    bg_color=params.get("bg_color")
    is_blank=params.get("is_blank")
    order_num=params.get("order_num")
    img_url=params.get("img_url")

    banner = Banner(img_url=img_url,redirect_url=redirect_url,bg_color=bg_color,is_blank=is_blank,order_num=order_num,state=0)

    BannerDao().save(banner)

    return  jsonify(success=1)







@admin.route('/qqgroup_manager.html')
@login_required
def qqgroup_manager():
    """ qq群管理 """

    new_qqgroup_form =  NewQQGroupForm()
    qqGroups = QQGroup.query.all()
    return render_template('admin/qqgroup_manage.html', qqGroups=qqGroups,new_qqgroup_form = new_qqgroup_form)


@admin.route('/add_qqgroup',methods=['POST'])
@login_required
def qqgroup_add():
    """
    添加QQ群
    """
    new_qqgroup_form =  NewQQGroupForm()
    if new_qqgroup_form.validate_on_submit():
        qqGroup = QQGroup(group_name=new_qqgroup_form.name.data,
                          group_num = new_qqgroup_form.num.data,
                          group_link=new_qqgroup_form.link.data,
                          desc=new_qqgroup_form.desc.data,
                          createtime= datetime.now())

        db.session.add(qqGroup);
        db.session.commit();

        return  redirect(url_for('admin.qqgroup_manager'))

@admin.route('/del_qqgroup/<int:group_id>')
@login_required
def qqgroup_del(group_id):

    """
     删除QQ群
    :param group_id:
    :return:
    """

    qqGroup = QQGroup.query.get_or_404(group_id)
    db.session.delete(qqGroup)
    db.session.commit()

    return  redirect(url_for('admin.qqgroup_manager'))


@admin.route('/classtype_manager.html')
@login_required
def classtype_manager():
    """ 课程分类管理 """

    new_clastype_form = NewClassTypeForm()
    classTypes = ClassType.query.filter_by(parent_id=0).all()

    return render_template('admin/classtype_manage.html', classTypes=classTypes,new_clastype_form = new_clastype_form)



@admin.route('/classtype_datail/<int:id>')
@login_required
def classtype_detail(id):

  new_clastype_form = NewSecondClassTypeForm(parent_id=id)
  classType = ClassType.query.get_or_404(id)
  second_classTypes = ClassType.query.filter_by(parent_id=id).all()
  return render_template('admin/classtype_detail.html', classType=classType,
                          second_classTypes=second_classTypes,

                          new_clastype_form = new_clastype_form)

@admin.route('/classtype_add',methods=['POST'])
@login_required
def classtype_add():

    new_clastype_form = NewClassTypeForm()

    if new_clastype_form.validate_on_submit():
        classType = ClassType(name = new_clastype_form.name.data,
                             parent_id = 0,
                             desc=new_clastype_form.desc.data,
                             created_time=datetime.now())
        db.session.add(classType)
        db.session.commit();

        return  redirect(url_for('admin.classtype_manager'))

@admin.route('/classtype_add_second',methods=['POST'])
@login_required
def classtype_add_second():

    new_clastype_form = NewSecondClassTypeForm()


    if new_clastype_form.validate_on_submit():
        parent_id = new_clastype_form.parent_id.data

        classType = ClassType(name = new_clastype_form.name.data,
                             parent_id = parent_id,
                             desc=new_clastype_form.desc.data,
                             created_time=datetime.now())

        db.session.add(classType)
        db.session.commit();
        return  redirect(url_for('admin.classtype_detail',id=new_clastype_form.parent_id.data))


@admin.route('/classtype_del/<int:id>')
@login_required
def classtype_del(id):
   return  redirect(url_for('admin.classtype_manager'))




@admin.route('/friendlink_manage.html')
@login_required
def friendlink_manager():
    links = FriendLink.query.all()
    return  render_template('admin/friendlink_manage.html',links = links)


@admin.route('/friendlink_add.html',methods=['GET','POST'])
@login_required
def friendlink_add():
    new_friendlink_form = NewFriendLinkForm()

    if new_friendlink_form.validate_on_submit():
        friendlink =FriendLink(site_name = new_friendlink_form.site_name.data,
                               site_url = new_friendlink_form.site_url.data,
                               title = new_friendlink_form.title.data,
                               contact = new_friendlink_form.contact.data)
        db.session.add(friendlink)
        db.session.commit()
        return redirect(url_for('admin.friendlink_manager'))

    return  render_template('admin/friendlink_add.html',new_friendlink_form=new_friendlink_form)


@admin.route('/usermsg_manager.html')
@login_required
def usermsg_manager():
    return  render_template('admin/usermsg_manage.html')

#def addTextToTask(newTask):
#    return newTask

###开启线程保存用户消息
def saveMsg(users, title, message):
    userMsgs = []
    for user in users:
        userMsg = models.UserMsg(title=title, msg=message, send_time=datetime.now(), user_id=user.id, msg_type=0, is_read=0)
        userMsgs.append(userMsg)
    pool = multiprocessing.Pool(20)
    #fullTasks = pool.map(addTextToTask, newTasks)
    pool.close()
    pool.join()
    cucount=0
    for fullTask in userMsgs:
        db.session.add(fullTask)
        cucount +=1
        if cucount%500 == 0:
            db.session.commit()
    db.session.commit()
    return True

@admin.route('/usermsg_send',methods=['GET','POST'] )
@login_required
def usermsg_send():
    usermsg = ''
    try:
        rduser=request.form.get('rduser') ##all only
        msgusers=request.form.get('msgusers') ##only email
        title=request.form.get('title') ##title
        message=request.form.get('message') ##message info
        if rduser == 'all':
            users = User.query.all()
            saveMsg(users, title, message) ###多线程保存用户消息
        else:
            emails = msgusers.split(',')
            for email in emails:
                user=User.query.filter(User.email.__eq__(email.strip())).first()
                if user is not None:
                    usermsg = UserMsg(title=title, msg=message, send_time=datetime.now(), user_id=user.id, msg_type=0, is_read=0)
                    db.session.add(usermsg)
                    db.session.commit()
                    db.session

        usermsg = '已成功发布用户消息'
    except:
        usermsg = '发布用户消息失败！！！'
    return  render_template('admin/usermsg_result.html', usermsg=usermsg)





@admin.route('/key')
@login_required
def key():
    key_name = '%s' % (uuid.uuid1())
    return key_name







@admin.route('/email/template.html')
@login_required
def email_template():
    return  render_template('admin/email_template_manage.html')



@admin.route('/email/templates')
@login_required
def email_templates():

    templates =send_cloud_trigger.template_get()

    datas=json.loads(templates)

    return jsonify(templates=datas['templateList'])


@admin.route('/email/groups')
@login_required
def email_groups():

    templates =send_cloud_trigger.group_list()
    datas=json.loads(templates)
    return jsonify(templates=datas['lists'])


@admin.route('/email/send',methods=['POST'])
@login_required
def email_send():

    json_obj = request.get_json()
    invoke_name = json_obj.get('invoke_name')
    group_id = json_obj.get('group_id')

    if invoke_name is not None and group_id is not None:
        result =  send_email_template_group(invoke_name, group_id)
        current_app.logger.info(result)
        return jsonify({'code':1})
    else:
        return jsonify({'code':0})



@admin.route('/email/send_sign',methods=['POST'])
@login_required
def email_send_sign():

    json_obj = request.get_json()
    invoke_name = json_obj.get('invoke_name')
    group_id = json_obj.get('group_id')


    tmpl = send_cloud_trigger.template_get_by_invoke_name(invoke_name)
    template_json=json.loads(tmpl)

    template =template_json['templateList'][0]



    email_user_dao=  EmailUserDao()
    email_users = email_user_dao.findEmailUserByGroupId(group_id)



    if template is not None and len(email_users)>0:

        eusers =[]

        for u in email_users:
            euser = Euser(u.name,u.email)
            eusers.append(euser)

        timer = SendEmailTimer(1,5,template,eusers)
        timer.start()


        return jsonify({'code':1})

    else:
        return jsonify({'code':0})




@admin.route('/video_deltoken.html')
@login_required
def video_deltoken(chapter_id):
    accessKey = '9919P8Ql1srb9d649XqXYbZ3bU0RBkyntY1TKJzA'
    secretKey = 'sR49P8Ql1I3d9dXEeXqXYbFD3oi1ZGPWCcdQ2UjV'
    url='http://access.baofengcloud.com/upload'


    filename =  request.args.get('filename')
    if filename is None:
        print 'error! Missing parameters!'


    filename = request.args.get('filename');
    servicetype = request.args.get('servicetype');
    filekey = request.args.get('filekey');
    deadline = datetime.time+3600;
    callbackurl = request.args.get('callbackurl')

    jsonstr = {}
    jsonstr.filename = filename
    jsonstr.filekey = filekey
    jsonstr.deadline = deadline
    jsonstr.servicetype = servicetype
    jsonstr.callbackurl = callbackurl


    encoded_json = base64_encode(jsonstr)

    sign = hash('sha1', encoded_json, secretKey, True)
    encoded_sign = base64_encode(sign)

     #token = accessKey + ":" + getEncodeSign(encoded) + ":" + encoded;
    token = accessKey + ':' + encoded_sign + ':' + encoded_json;
    data='{token : '+token+'}'
    return  data;


@admin.route('/video_token.html')
@login_required
def video_token():


    print 'yamasun river!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    accessKey = '9919P8Ql1srb9d649XqXYbZ3bU0RBkyntY1TKJzA'
    secretKey = 'sR49P8Ql1I3d9dXEeXqXYbFD3oi1ZGPWCcdQ2UjV'
    url='http://access.baofengcloud.com/upload'

    #token = accessKey + ":" + getEncodeSign(encoded) + ":" + encoded;
    if  request.args.get('filename') is None:
        return 'data not full'

    filename = request.args.get('filename')
    filesize = request.args.get('filesize')
    uptype = request.args.get('uptype')
    servicetype = request.args.get('servicetype')
    filetype = request.args.get('filetype');
    filekey = request.args.get('filekey');
    deadline = datetime.time+3600;
    callbackurl = request.args.get('callbackurl');


    # base_url = '%s/%s?avinfo' %(domain,key)
    # current_app.logger.info(video_url)
    # import  urllib2
    # api = video_url
    # http_request = urllib2.Request(api)
    # http_request.add_header("Accept", "*/*")
    # http_request.add_header('Referer', "http://www.cniao5.com")
    # http_request.add_header("Accept-Language", "zh-cn")
    # opener = urllib2.build_opener()
    # f = opener.open(http_request)
    # result = f.read()

    jsonstr = {}
    jsonstr.uptype = uptype
    jsonstr.filetype = filetype
    jsonstr.filename = filename
    jsonstr.filesize = filesize
    jsonstr.filekey = filekey
    jsonstr.deadline = deadline
    jsonstr.servicetype = servicetype
    jsonstr.callbackurl = callbackurl
    jsonstr = jsonify(jsonstr)

    encoded_json = base64_encode(jsonstr)

    sign = hash('sha1', encoded_json, secretKey, True)
    encoded_sign = base64_encode(sign)

     #token = accessKey + ":" + getEncodeSign(encoded) + ":" + encoded;
    token = accessKey + ':' + encoded_sign + ':' + encoded_json;
    data='{token : '+token+'}'
    return  data;




@admin.route('/video_delcallback.html')
@login_required
def video_delcallback(chapter_id):
     print 'delcallback list'

@admin.route('/video_uploadcallback.html')
@login_required
def video_uploadcallback(chapter_id):
    print 'yaya'





class Euser():
    def __init__(self,name,email):
        self.name = name
        self.email = email


class SendEmailTimer(threading.Thread):

    def __init__(self, num, interval,email_template,email_users):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
        self.email_template = email_template
        self.email_users = email_users



    def run(self): #Overwrite run() method, put what you want the thread do here

        import time


        if len(self.email_users)<=0:
            self.stop()

        html = self.email_template.get('html')
        subject = self.email_template.get('subject')

        e_users =self.email_users
        for user in e_users:
            name=user.name
            if name is None:
                name=user.email
            html = html.replace('%user.name%',name)
            send_email_use_html(user.email,subject,html)

            time.sleep(self.interval)




    def stop(self):
        self.thread_stop = True




