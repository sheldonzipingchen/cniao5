# -*- coding: UTF-8 -*-
from flask import render_template, jsonify
from flask.ext.login import login_required, current_user

from . import member
from app.dao.class_dao import CourseNoteDao, CourseDao


__author__ = 'Ivan'




@member.route('/my/notebooks')
@login_required
def notebooks():

    notes =CourseNoteDao().find_user_notebooks_group_by_class(current_user.id)

    return  render_template('member/notebook/list.html',notes=notes)


@member.route('/my/notebook/<int:class_id>')
@login_required
def notebook_detail(class_id):

    notes =CourseNoteDao().find_class_notes_by_user(class_id,current_user.id)
    course = CourseDao().get_or_404(class_id)
    # lesson = LessonDao().get_or_404(note.lesson_id)

    return  render_template('member/notebook/detail.html',notes=notes,
                            course=course,
                            )




@member.route('/my/notebook/<int:id>/delete',methods=['POST'])
@login_required
def notebook_delete(id):
    dao =CourseNoteDao()
    note = dao.get_or_404(id)
    dao.delete(note)
    return jsonify(result=True)


