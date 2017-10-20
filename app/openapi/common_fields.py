
# -*- coding: UTF-8 -*-
from flask.ext.restful import fields
from .. openapi.utils import DateFormat, FirstImage

__author__ = 'Ivan'


user_fields={
    'id':fields.Integer,
    'username':fields.String,
    'email':fields.String,
    'logo_url':fields.String,
    'user_type':fields.Integer
}


qq_fields={
    'id':fields.Integer,
    'group_name':fields.String,
    'group_num':fields.String,
    'desc':fields.String,
    'created_time':DateFormat(attribute='createtime'),
}


#课程
class_fields={

    'id':fields.Integer,
    'name':fields.String,
    'desc':fields.String,
    'created_time':DateFormat(attribute='created_time'),
    'lessons_count':fields.Integer,
    'lessons_time':fields.Integer,
    'lessons_played_time':fields.Integer,
    'comment_count':fields.Integer,
    'recommend_count':fields.Integer,
    'class_type':fields.Integer,
    'second_class_type':fields.Integer,
    'class_difficulty':fields.Integer,
    'key_words':fields.String,
    'fit_to':fields.String,
    'img_url':fields.String,
    'is_free':fields.String,
    'is_online':fields.String,
}

class_fields['teacher']=fields.Nested(user_fields)
class_fields['qqgroup']=fields.Nested(qq_fields)




simple_course_fields={
    'id':fields.Integer,
    'name':fields.String,
    'lessons_count':fields.Integer,
    'lessons_time':fields.Integer,
    'lessons_played_time':fields.Integer,
    'img_url':fields.String,
    'is_free':fields.Integer,
}



course_pagination_simple_fields={

    'totalCount':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}
course_pagination_simple_fields['datas']=fields.Nested(simple_course_fields)



#视频
video_fields={

    'id':fields.Integer,

    'created_time':DateFormat(attribute='createtime'),
    'filesize':fields.Integer,
    'duration':fields.Integer,
}


#课时
lesson_fields={

    'id':fields.Integer,
    'name':fields.String,
    'desc':fields.String,
    'created_time':DateFormat(attribute='created_time'),
    'state':fields.Integer,
    'is_free':fields.Integer,
    'chapter_id':fields.Integer,
    'pub_tag':fields.Integer,
    'bsort':fields.Integer

}

lesson_fields['video'] = fields.Nested(video_fields)



#章节
chapter_fields={

    'id':fields.Integer,
    'name':fields.String(attribute='title'),
    'class_id':fields.Integer

}

chapter_fields['lessons']=fields.Nested(lesson_fields)




#评论
comment_fields={

    'id':fields.Integer,
    'class_id':fields.Integer,
    'lesson_id':fields.Integer,
    'score':fields.Integer,
    'comment':fields.String,
    'created_time':DateFormat(attribute='created_time'),

}

comment_fields['user']=fields.Nested(user_fields)




courseware_fields={

    'id':fields.Integer,
    'filename':fields.String,
    'class_id':fields.Integer,
    'filesize':fields.Integer,
    'is_free':fields.Integer,
    'created_time':DateFormat(attribute='created_time'),

}

# courseware_fields['lesson'] = fields.Nested(lesson_fields)



#课程播放
lesson_play_user_fields={
    'id':fields.Integer,
    'lesson_id':fields.Integer,

}

lesson_play_user_fields['user']=fields.Nested(user_fields)
lesson_play_user_fields['lesson']=fields.Nested(lesson_fields)


class_play_data_fields={

    'play_count':fields.Integer,
}

class_play_data_fields['play_list']=fields.Nested(lesson_play_user_fields)




#帖子

thread_files={

    'id':fields.Integer,
    'title':fields.String,
    'brief':fields.String,
    'logo_url':FirstImage(attribute='imgs'),
    #'content':fields.String,
    'class_id':fields.Integer,
    'lesson_id':fields.Integer,
    'user_id':fields.Integer,
    'created_time':DateFormat(attribute='created_time'),
    'last_comment_time':DateFormat(attribute='created_time'),
    'read_count':fields.Integer,
    'reply_count':fields.Integer,
    'is_hot':fields.Integer,
    'is_top':fields.Integer,
}


thread_files['user'] = fields.Nested(user_fields)



#帖子回复

thread_post_files={

    'id':fields.Integer,
    'content':fields.String,
    'class_id':fields.Integer,
    'lesson_id':fields.Integer,
    'user_id':fields.Integer,
    'created_time':DateFormat(attribute='created_time'),
    'status':fields.Integer
}

thread_post_files['user'] = fields.Nested(user_fields)





#课程评论-分页

comment_pagination_fields={

    'totalCount':fields.Integer,
    'totalPage':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}
comment_pagination_fields['datas']=fields.Nested(comment_fields)






thread_pagination_fields={

    'totalCount':fields.Integer,
    'totalPage':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,


}

thread_pagination_fields['datas']=fields.Nested(thread_files)




thread_post_pagination_fields={

    'totalCount':fields.Integer,
    'totalPage':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}

thread_post_pagination_fields['datas']=fields.Nested(thread_post_files)




#####提现
withdrawal_fields={

    "id":fields.Integer,

    "apply_money":fields.Float,
    "pay_money":fields.Float,
    "service_charge":fields.Float,
    "pay_channel":fields.String,
    "beneficiary_account":fields.String,
    "created_time":DateFormat(attribute='created_time'),
    "hande_time":DateFormat(attribute='hande_time'),
    "state":fields.Integer,
}
withdrawal_fields['user']=fields.Nested(user_fields)

withdrawal_pagination_simple_fields={

    'totalCount':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}
withdrawal_pagination_simple_fields['datas']=fields.Nested(withdrawal_fields)



###订单

order_files={

    'id':fields.Integer,
    'title':fields.String,
    'order_num':fields.String,
    'total_price': fields.Integer,
    'trade_status': fields.String,
    'created_date': DateFormat(attribute='created_date'),

}

order_pagination_fields={

    'totalCount':fields.Integer,
    'totalPage':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}
order_pagination_fields['datas']=fields.Nested(order_files)



#######收入#######
income_fields={

    "id":fields.Integer,
    "title":fields.String,
    "money":fields.Float,
    "created_time":DateFormat(attribute='created_time')
}

income_fields['user']=fields.Nested(user_fields)


income_pagination_simple_fields={

    'totalCount':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}
income_pagination_simple_fields['datas']=fields.Nested(income_fields)



######商品订单

goods_order_fields={

    "id": fields.Integer,
    "goods_id": fields.Integer,
    "title": fields.String,
    "order_num": fields.String,
    "total_price": fields.Float,
    "created_time": DateFormat(attribute='created_time'),
    "pay_type":fields.String,
    "receiver":fields.String,
    "addr":fields.String,
    "mobi":fields.String

}

goods_order_fields["user"]=fields.Nested(user_fields)


goods_order_pagination_fields={

    'totalCount':fields.Integer,
    'pageIndex':fields.Integer,
    'pageSize':fields.Integer,

}
goods_order_pagination_fields['datas']=fields.Nested(goods_order_fields)