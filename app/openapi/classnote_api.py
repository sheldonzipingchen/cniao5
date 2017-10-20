# -*- coding: UTF-8 -*-


from flask.ext.restful import Resource,reqparse,fields, marshal_with
from .. dao.class_dao import CourseNoteDao
from . common_fields import user_fields
from . utils import DateFormat





__author__ = 'Ivan'





resource_fields={
    'id':fields.Integer,
    'note':fields.String,
    'created_time':DateFormat(attribute='created_time'),
    'class_id':fields.Integer,
    'lesson_id':fields.Integer,
    'position':fields.Float,
    'img_url':fields.String,
    'is_open':fields.Integer

}

resource_fields['user']=fields.Nested(user_fields)





class ClassNote(Resource):

    def get(self,id):

        pass





#笔记列表
class ClassNoteList(Resource):

    @marshal_with(resource_fields)
    def get(self):

        args = parser.parse_args()
        class_id= args['class_id']

        dao = CourseNoteDao()
        notes =dao.findByClassId(class_id)

        return notes







parser = reqparse.RequestParser()
parser.add_argument('class_id', type=int,required=True , help='class_id cannot be blank')



####

