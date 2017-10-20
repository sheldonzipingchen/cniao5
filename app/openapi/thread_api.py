# -*- coding: UTF-8 -*-


from flask.ext.restful import Resource, marshal_with,reqparse

from app.dao.thread_dao import ThreadDao, ThreadPostDao
from app.openapi.common_fields import thread_pagination_fields, thread_post_pagination_fields

__author__ = 'Ivan'



class ThreadPagination(Resource):

    @marshal_with(thread_pagination_fields)
    def get(self):

        args = parser.parse_args()
        target_id= args['target_id']
        target_type= args['target_type']
        page_index= args['page_index']
        page_size= args['page_size']
        order_by= args.get('order_by')
        is_hot= args.get('is_hot')

        if order_by is None:
            order_by=0

        order_by = int(order_by)


        if is_hot is None:
            is_hot=0

        dao = ThreadDao();
        if target_type=='course' or target_type=='user':
            pagination =dao.pagination(target_id,target_type,order_by,page_index,page_size)
        else:
            pagination=dao.pagination_for_forum(target_id,order_by,is_hot,page_index,page_size)

        return pagination


class ThreadPostPagination(Resource):

    @marshal_with(thread_post_pagination_fields)
    def get(self):

        args = parser.parse_args()
        target_id= args['target_id']
        page_index= args['page_index']
        page_size= args['page_size']


        dao = ThreadPostDao();
        pagination =dao.pagination(target_id,page_index,page_size)



        return pagination



parser = reqparse.RequestParser()
parser.add_argument('target_id',type=int,required=True , help='target_id cannot be blank')
parser.add_argument('page_index',type=int,required=True , help='page_index cannot be blank')
parser.add_argument('page_size',type=int,required=True , help='page_size cannot be blank')
parser.add_argument('order_by',type=int)
parser.add_argument('target_type',required=True,help='target_type cannot be blank')
parser.add_argument('is_hot',type=int)