# -*- coding: UTF-8 -*-
import os

from app import create_app, db

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


from app.app_creator import  init_app
from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand, Migrate

# from app.models import CourseProductRelationship, ProductVIP, UserFollow, User, Order, ProductOrder, \
#     Course, Chapter, Lesson, Compilation, ClassType, Video, QQGroup, Banner, FriendLink, CourseComment,  \
#     LessonPlay, CourseFavorites, ClassTypeRelationship, PhoneMessage, UserActivateEmail, \
#      CourseWareDownload, SysNotification, UserMsg,  EmailTemplate, Coupon, \
#     EmailMessage, EmailGroupUser, EmailUser, EmailGroup, CourseStudy, UserIncome,UserWithdrawal

__author__ = 'Sheldon Chen'




app = create_app(os.getenv('CNIAO5_CONFIG') or 'default')
init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)

# @app.context_processor
# def main_processor():
#     second_class_type_list = ClassType.query.filter(ClassType.parent_id == 1).all()
#     login_form = LoginForm(remember_me=True)
#     return dict(second_class_type_list=second_class_type_list,login_form=login_form)


# @app.route('/register')
# def register():
#     return redirect(url_for('auth.reg'))




#
# def make_shell_context():
#     return dict(app=app, db=db, CourseProductRelationship=CourseProductRelationship,
#                 ProductVIP=ProductVIP, Order=Order,
#                 ProductOrder=ProductOrder, Chapter=Chapter,
#                 UserFollow=UserFollow, User=User,
#                 ClassType=ClassType, Video=Video,
#                 ClassComment=CourseComment,
#                 Course=Course, Lesson=Lesson,
#                 Compilation=Compilation, QQGroup=QQGroup,
#                 Banner=Banner,FriendLink=FriendLink,
#                 CourseStudy=CourseStudy, LessonPlay=LessonPlay,
#                 CourseFavorites=CourseFavorites,
#                 ClassTypeRelationship=ClassTypeRelationship, PhoneMessage=PhoneMessage,
#                 UserActivateEmail=UserActivateEmail,CourseWareDownload=CourseWareDownload,
#                 SysNotification=SysNotification,UserMsg=UserMsg,
#                 EmailGroup=EmailGroup,EmailUser=EmailUser,
#                 EmailGroupUser=EmailGroupUser,EmailMessage=EmailMessage,
#                 EmailTemplate=EmailTemplate,
#                 Coupon=Coupon, UserIncome=UserIncome,
#                 UserWithdrawal=UserWithdrawal)
#
#
# manager.add_command('shell', Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)

#
# @manager.command
# def test(coverage=False):
#     """ Run the unit tests. """
#     if coverage and not os.environ.get('FLASK_COVERAGE'):
#         import sys
#
#         os.environ['FLASK_COVERAGE'] = '1'
#         os.execvp(sys.executable, [sys.executable] + sys.argv)
#     import unittest
#
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#     if COV:
#         COV.stop()
#         COV.save()
#         print('Coverage Summary:')
#         COV.report()
#         basedir = os.path.abspath(os.path.dirname(__file__))
#         covdir = os.path.join(basedir, 'tmp/coverage')
#         COV.html_report(directory=covdir)
#         print('HTML version: file://%s/index.html' % covdir)
#         COV.erase()


def deploy():
    """ Run deployment tasks. """
    from flask.ext.migrate import upgrade

    # 把数据库迁移到最新修订版本
    upgrade()



if __name__ == '__main__':
    manager.run()
