# -*- coding: utf-8 -*-
from flask import render_template

from . import help

__author__ = 'SheldonChen'







@help.route('/about_us.html')
def about_us():
    return render_template('help/about_us.html')





@help.route('/contact_us.html')
def contact_us():
    return render_template('help/contact_us.html')


@help.route('/teacher/recruit.html')
def teacher_recruit():
    return render_template('help/teacher-recruit.html')



@help.route('/service.html')
def service():
    return render_template('help/service.html')