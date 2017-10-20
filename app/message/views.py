# -*- coding: UTF-8 -*-
import base64
from datetime import datetime
from flask import jsonify, render_template, request
from flask.ext.login import login_required, current_user
from flask.ext.restful import abort

from . import message
from app.dao.user_dao import UserMessageDao, UserDao
from app.models import UserMsg

__author__ = 'Ivan'



@message.route("/user/unread/count")
@login_required
def user_unread_message():

    count = UserMessageDao().find_user_unread_msg_count(current_user.id)
    return jsonify(count=count)



@message.route("/user/messages")
@login_required
def user_messages():

    messageDao = UserMessageDao()

    msgs = messageDao.find_user_messages(current_user.id)

    return render_template('message/index.html',messages=msgs)





@message.route("/user/conversation/<string:id>")
@login_required
def message_conversation(id):


    messages = UserMessageDao().find_conversation_messages(id);

    if len(messages)<=0:
        return abort(404)

    message = messages[0];

    user = message.from_user
    if user.id == current_user.id:
        user=message.to_user

    return render_template("message/detail.html",messages=messages,
                           conversation=id,
                           user=user)



@message.route("/user/conversation/read/<string:id>",methods=['POST'])
@login_required
def message_read(id):
        UserMessageDao().user_conversation_messages_read(current_user.id,id)
        return jsonify(success=True,message=u'Success')




@message.route("/user/message/delete/<int:id>",methods=['POST'])
@login_required
def message_delete(id):

     msg = UserMessageDao().get_or_404(id)
     if msg.from_user_id == current_user.id:
       UserMessageDao().delete(msg)
       return jsonify(success=True,message=u'Success')

     return jsonify(success=False,message=u'删除失败,暂时不能删除该私信')


@message.route("/user/message/send",methods=["POST"])
@login_required
def message_send():

    json = request.get_json();

    to_user_id = json.get("to_user_id");
    msg = json.get("msg")

    if to_user_id == current_user.id:
         return jsonify(success=False,message=u'别闹,不要给自己发私信行不')

    user_dao = UserDao()
    user = user_dao.get(to_user_id)

    if user is None:
        return jsonify(success=False,message=u'用户不存在')


    user_msg =UserMsg(
                      title=u'与%s的对话'%user.username,
                      msg=msg,
                      from_user_id=current_user.id,
                      to_user_id =to_user_id,
                      )

    UserMessageDao().save(user_msg)

    return jsonify(success=True,message=u'发送私信成功')




