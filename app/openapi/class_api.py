# -*- coding: UTF-8 -*-

from flask.ext.restful import Resource, reqparse,marshal_with, abort
from .. pagination import Pagination

from . common_fields import chapter_fields, class_fields, \
        class_play_data_fields, comment_fields, courseware_fields, \
        comment_pagination_fields, course_pagination_simple_fields
from ..dao.class_dao import CourseDao, ChapterDao, CourseCommentDao, ClassWareDao


__author__ = 'Ivan'







class Class(Resource):

    @marshal_with(class_fields)
    def get(self,id):
        course = CourseDao().get(id)
        if course is None:

            abort(404)
        return  course



class CoursePagination(Resource):
    @marshal_with(course_pagination_simple_fields)
    def get(self):

        args = course_parser.parse_args()
        is_free= args['is_free']
        order_by= args['order_by']
        page_index= args['page_index']
        page_size= args['page_size']


        dao =CourseDao()
        pagination =dao.pagination(is_free,order_by,page_index,page_size)

        return  pagination



course_parser = reqparse.RequestParser()
course_parser.add_argument('is_free',type=int,required=True , help='class_id cannot be blank')
course_parser.add_argument('order_by',type=int,required=True , help='class_id cannot be blank')
course_parser.add_argument('page_index',type=int,required=True , help='page_index cannot be blank')
course_parser.add_argument('page_size',type=int,required=True , help='page_size cannot be blank')



#课程章节
class ClassChapter(Resource):


    @marshal_with(chapter_fields)
    def get(self,id):

        dao = ChapterDao()

        chapters = dao.get_course_chapter(id)

        return chapters


#课程播放
class ClassPlay(Resource):


    @marshal_with(class_play_data_fields)
    def get(self,id):
        dao = CourseDao()
        play_list = dao.get_play_list_top(id,15)
        play_count=dao.get_total_play_count(id)

        data = ClassPlayData(play_count,play_list)

        return data




class ClassCommentPagination(Resource):

    @marshal_with(comment_pagination_fields)
    def get(self):

        args = parser.parse_args()
        class_id= args['class_id']
        page_index= args['page_index']
        page_size= args['page_size']

        dao = CourseCommentDao();
        comments,count=dao.pagetion(class_id,page_index,page_size)


        pagination= Pagination(count,page_index,page_size,comments)

        return pagination





parser = reqparse.RequestParser()
parser.add_argument('class_id',type=int,required=True , help='class_id cannot be blank')
parser.add_argument('page_index',type=int,required=True , help='page_index cannot be blank')
parser.add_argument('page_size',type=int,required=True , help='page_size cannot be blank')


class ClassCourseWare(Resource):

    @marshal_with(courseware_fields)
    def get(self,id):
        dao =ClassWareDao()

        items= dao.find_by_class_id(id)

        # for item in items:
        #     print item.lesson.name

        return  items



class ClassPlayData():
    def __init__(self,play_count,play_list):
        self.play_count=play_count
        self.play_list=play_list


