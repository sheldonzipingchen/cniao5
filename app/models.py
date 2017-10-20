# -*- coding: UTF-8 -*-
import json
import uuid
from datetime import datetime

from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.util.str_util import random_code

__author__ = 'Sheldon Chen'




class UserFollow(db.Model):
    """ 关注表 """
    __tablename__ = 'user_follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # 关注者的 id
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # 被关注者的 id
    timestamp = db.Column(db.DateTime, default=datetime.now())





class User(UserMixin, db.Model):
    """ 用户实体：学员，讲师，管理员 """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    unique_code = db.Column(db.String(200),unique=True) #唯一码
    invite_code = db.Column(db.String(20),unique=True) #邀请码
    email = db.Column(db.String(30), unique=True)  # 邮件，登录帐号
    username = db.Column(db.String(64), unique=True)  # 昵称
    desc = db.Column(db.String(500))  # 简介
    password_hash = db.Column(db.String(128))  # hash 后的密码
    pwd = db.Column(db.String(255))  # mingwen
    mobi = db.Column(db.String(15))  # 手机号
    mobile_confirmed = db.Column(db.Boolean, default=False)  # 确认手机号
    qq = db.Column(db.String(128))  # qq
    #money = db.Column(db.Float,default=0) #账户余额
    balance = db.Column(db.Float,default=0) #账户余额,真实人民币
    coin = db.Column(db.Float,default=0) #虚拟币账户
    frozen_capital=db.Column(db.Float,default=0)#用于冻结资金，申请提现时
    alipay = db.Column(db.String(50)) #支付宝账户
    real_name = db.Column(db.String(20))#真实姓名
    confirmed = db.Column(db.Boolean, default=False)  # 是否确认
    reg_time = db.Column(db.DateTime, default=datetime.now())  # 注册时间
    logo_url = db.Column(db.String(255))  # 帐号 logo 地址
    user_type = db.Column(db.Integer, default=1)  # 帐号类型，1： 学员；2：讲师；3：管理员
    channel = db.Column(db.String(10), default='')  # 渠道
    inviter_id = db.Column(db.Integer) #邀请人ID

    province = db.Column(db.String(255))  # 省
    city = db.Column(db.String(255))  # 市
    addr = db.Column(db.String(500)) # 地址
    company = db.Column(db.String(200)) # 公司/学校
    job = db.Column(db.String(100)) # 职位

    work_years = db.Column(db.String(255))  # 工作经验
    focus_it = db.Column(db.String(255))  # 关注技术

    follower_count =db.Column(db.Integer) #粉丝数
    following_count =db.Column(db.Integer) #关注数

    #我关注的人
    followed = db.relationship('UserFollow',
                               foreign_keys=[UserFollow.follower_id],
                               backref=db.backref('followers', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    #我的粉丝
    followers = db.relationship('UserFollow',
                                foreign_keys=[UserFollow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

    def follow_user(self, user):
        if not self.is_my_follower(user):
            f = UserFollow(follower_id=user.id, followed_id=self.id,timestamp=datetime.now())
            db.session.add(f)
            db.session.commit()

            if self.follower_count==None:
                self.follower_count=1
            else:
                self.follower_count+=1; #自己粉丝数 +1

            db.session.add(self)
            db.session.commit()

            if user.following_count==None:
                user.following_count=1
            else:
                user.following_count+=1; #对方关注数加1

            db.session.add(user)
            db.session.commit()


    def unfollow_user(self, user):
        f = self.followers.filter_by(follower_id=user.id).first()
        if f is not None :
            db.session.delete(f)
            db.session.commit()

            self.follower_count-=1; #自己粉丝数 +1
            db.session.add(self)
            db.session.commit()

            user.following_count-=1; #对方关注数加1
            db.session.add(user)
            db.session.commit()

    def is_my_follower(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None


    def is_followed_by(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None


    def __unicode__(self):
        return '%s' % self.username

    @property
    def password(self):
        """ 不可以直接读取用户密码 """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """ 对用户密码加密后保存到用户类里 """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ 校验用户密码是否正确 """
        return check_password_hash(self.password_hash.encode('utf-8'), password)

    def generate_confirmation_token(self, expiration=3600):
        """ 对用户的 id 进行加密，然后返回一个散列值 """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """ 确认用户状态 """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True



    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None

        return User.query.get(data['id'])


    def is_super_admin(self):
        return self.user_type==3

    def is_teacher(self):
        return self.user_type==2


    def get_unique_code(self):
        if self.unique_code==None:
            self.unique_code=str(uuid.uuid1()).replace('-','')

        return self.unique_code

    def get_invite_code(self):
        if self.invite_code==None:
            self.invite_code=random_code(self.id,6)

        return self.invite_code



class Teacher(db.Model):
     """讲师表 """
     __tablename__ = 'teacher'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
     teacher_name = db.Column(db.String(50))
     id_num = db.Column(db.String(50)) #身份证号码
     logo_url = db.Column(db.String(255))  # 头像地址
     rate = db.Column(db.Float,default=0) #课程分成比例 ，值在 0 - 1 之间
     company = db.Column(db.String(100))  # 就职公司
     mobi=db.Column(db.String(12))
     email=db.Column(db.String(50))
     qq=db.Column(db.String(12))
     brief = db.Column(db.String(500))  # 简介
     sort_num = db.Column(db.Integer) #排序
     is_show=db.Column(db.Integer,default=1) #是否在页面显示
     is_recommend=db.Column(db.Integer,default=0)
     teach_course_type = db.Column(db.String(100)) #授课领域
     bank_name=db.Column(db.String(100)) #银行名称,如支付宝写 ALIPAY
     bank_account = db.Column(db.String(100))  #银行账户
     user = db.relationship('User')





class UserIncome(db.Model):
     """用户收入表 """
     __tablename__ = 'user_income'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
     money = db.Column(db.Float,default=0)
     title =db.Column(db.String(100))
     from_type = db.Column(db.Integer) #收入来源类型， 0:分享优惠码收入（普通用户）1: 分享优惠码收入, 3：销售课程收入（讲师）
     from_id = db.Column(db.Integer)
     created_time = db.Column(db.DateTime, default=datetime.now())

     user = db.relationship('User')


class UserWithdrawal(db.Model):
     """用户提现 """
     __tablename__ = 'user_withdrawal'
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
     apply_money = db.Column(db.Float,default=0) #申请金额
     created_time = db.Column(db.DateTime, default=datetime.now()) #申请时间
     pay_money = db.Column(db.Float,default=0) #支付金额
     pay_channel = db.Column(db.String(10)) #支付渠道，支付宝，网银
     beneficiary_account = db.Column(db.String(50)) # 收款账户
     service_charge = db.Column(db.Float(50)) # 手续费
     hande_user_id =db.Column(db.Integer, db.ForeignKey('users.id'))
     hande_time = db.Column(db.DateTime)
     state = db.Column(db.Integer,default=0) # 0 等待处理，1：成功，2：驳回

     user = db.relationship("User",foreign_keys='[UserWithdrawal.user_id]')





class ProductVIP(db.Model):
    """ 会员实体 """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(30), unique=True)  #会员名称
    month_price = db.Column(db.Integer)  # 会员价格（单位：元/月）
    year_price = db.Column(db.Integer)  # 会员价格（单位：元/年）
    created_time = db.Column(db.DateTime, default=datetime.now())
    is_visible = db.Column(db.Boolean,default=True) #是否公开
    comment = db.Column(db.Text)
    state = db.Column(db.Integer, default=0)  # 状态：0：启用

    # orders = db.relationship('Order', backref='product')
    # classes = db.relationship('CourseProductRelationship')
    # product_order_list = db.relationship('ProductOrder', backref="product")


class Order(db.Model):
    """ 订单实体 """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(50),unique=True)  # 流水号
    title = db.Column(db.String(200))  # 订单名称

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer)

    product_type=db.Column(db.Integer,default=0) # 0：高级会员 1：班级，2：专题(任务)  3：课程
    price = db.Column(db.Float,default=0)  # 商品单价
    order_count=db.Column(db.Integer,default=1) #购买数量
    coupon_id = db.Column(db.Integer) #优惠劵ID
    invite_user_id = db.Column(db.Integer) #邀请人ID
    day = db.Column(db.Integer) #购买产品的使用时长
    total_price = db.Column(db.Float)  # 订单总价
    pay_channel = db.Column(db.String(20))  # 支付渠道，赠送 为 FREE, 支付宝为 ALIPAY, 银行为相应的银行代码,COIN 为虚拟币
    trade_status = db.Column(db.String(50), default='INIT', nullable=True)  # 订单状态 INIT 待支付， TRADE_FINISHED TRADE_SUCCESS 成功，CANCEL: 取消，EXPIRE :过期
    created_date = db.Column(db.DateTime, default=datetime.now())  # 下单时间
    operation = db.Column(db.Integer, default=0)  # 订单操作
    remark=db.Column(db.String(255))  # 备注

    user = db.relationship('User')


class ProductOrder(db.Model):
    """ 订购关系实体 """
    __tablename__ = 'products_orders_relationship'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    product_type=db.Column(db.Integer,default=0) # 0：高级会员 1：班级，2：专题 3：课程
    state = db.Column(db.Integer, default=0)
    created_time = db.Column(db.DateTime, default=datetime.now())
    order_time = db.Column(db.DateTime, nullable=True)
    cancel_time = db.Column(db.DateTime, nullable=True)
    is_experience = db.Column(db.Integer,default=0) #是否是体验会员的权限


class Course(db.Model):
    """ 课程实体 """
    __tablename__ = "classes"
    # __searchable__ = ['name', 'desc']
    # __analyzer__=ChineseAnalyzer()
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)  # 课程标题
    desc = db.Column(db.Text)  # 介绍
    brief = db.Column(db.String(500))  # 简介
    created_time = db.Column(db.DateTime, default=datetime.now())  # 发布时间
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 讲师
    lessons_count = db.Column(db.Integer)  # 总课时
    lessons_finished_count = db.Column(db.Integer, default=0)  # 已更新课时
    lessons_time = db.Column(db.Integer)  # 总时长：秒
    lessons_played_time = db.Column(db.Integer)  # 总播放数
    comment_count = db.Column(db.Integer)  # 总评论数
    recommend_count = db.Column(db.Integer)  # 推荐指数
    class_type = db.Column(db.Integer)
    second_class_type = db.Column(db.Integer, db.ForeignKey('class_types.id'))
    class_difficulty = db.Column(db.Integer, default=1)  # 课程难度： 1：初级；2：中等；3：高级
    key_words = db.Column(db.String(255))  # 课程关键字
    fit_to = db.Column(db.String(255))  # 适合人群
    img_url = db.Column(db.String(255))  # 封面地址
    is_free = db.Column(db.Integer, default=False)  # 是否免费
    is_online = db.Column(db.Integer, default=0)  # 状态 0：未上线；1：已上线；
    types = db.Column(db.Integer, default=1) # 0：免费课程 1：会员课程　２：收费项目，3 就业课程
    cost_price = db.Column(db.Float)
    now_price = db.Column(db.Float)
    qqgroup_id = db.Column(db.Integer, db.ForeignKey('qqgroup.id'))  # qq群
    expiry_day = db.Column(db.Integer,default=365) #学习有效期，对 types ==2 的 课程有效
    rate = db.Column(db.Float,default=0) #课程分成比例 ，值在 0 - 1 之间
    is_hot = db.Column(db.Integer,default=0) #是否热门
    can_buy=db.Column(db.Integer,default=1) #是否可以购买
    can_use_coupon=db.Column(db.Integer,default=1) #是否可以使用优惠码

    teacher = db.relationship('User',
        backref=db.backref('classes', lazy='dynamic'))

    qqgroup = db.relationship('QQGroup',
        backref=db.backref('classes', lazy='dynamic'))

    def __unicode__(self):
        return u'%s' % self.name

    def is_vip(self):

        query = CourseProductRelationship.query.filter(CourseProductRelationship.product_id==8,
                                                       CourseProductRelationship.product_type==0,
                                                          CourseProductRelationship.class_id==self.id)
        relation =query.first()
        return  (relation is not None)




class CoursePath(db.Model):
    """ 课程线路 """
    __tablename__ = "course_path"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)  # 标题
    desc = db.Column(db.Text)  # 介绍
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    price = db.Column(db.Float) #价格
    logo_url = db.Column(db.String(200))
    qqgroup_id = db.Column(db.Integer,db.ForeignKey('qqgroup.id'))
    total_course = db.Column(db.Integer) #总课程数量
    total_lesson = db.Column(db.Integer) #总课时数量
    total_students = db.Column(db.Integer) #总学习数量
    status = db.Column(db.Integer) #0:未发布, 1:正常 ,

    qqgroup = db.relationship('QQGroup',
        backref=db.backref('course_path', lazy='dynamic'))


    topics = db.relationship('CourseTopic', backref='path')



class CourseTopic(db.Model):
    """ 课程专题 """
    __tablename__ = "course_topic"
    id = db.Column(db.Integer, primary_key=True)
    path_id = db.Column(db.Integer, db.ForeignKey('course_path.id'))
    title = db.Column(db.String(50), unique=True)  # 专题标题
    desc = db.Column(db.Text)  # 介绍
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    logo_url = db.Column(db.String(200))


class CourseProductRelationship(db.Model):
    """ 课程和产品中间表 """
    __tablename__ = 'class_product_relationship'
    # id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    product_type=db.Column(db.Integer,default=0) # 0：高级会员 1：班级，2：专题
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    # classes = db.relationship('Class')
    # products = db.relationship('Product')

class ClassType(db.Model):
    """ 课程类型实体 """
    __tablename__ = 'class_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent_id = db.Column(db.Integer, default=0)
    sort = db.Column(db.Integer, default=0)
    created_time = db.Column(db.DateTime, default=datetime.now())
    desc = db.Column(db.String(255))
    classes = db.relationship('Course', backref='class_item_type')


    def __unicode__(self):
        return '%s' % (self.name, )

class Recommend(db.Model):
    """ 课程推荐实体 """
    __tablename__ = 'recommend'
    id = db.Column(db.Integer, primary_key=True)
    restype = db.Column(db.Integer, default=0)
    resid = db.Column(db.Integer, default=0)
    settime = db.Column(db.DateTime, default=datetime.now())
    sort = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=0)



class ClassDraws(db.Model):
    """ 课程效果图 """
    __tablename__ = "classes_draws"
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    img_url = db.Column(db.String(255))  # 课程标题
    remark = db.Column(db.String(255))  # 课程标题

class ClassTypeRelationship(db.Model):

    """ 课程与三级分类管理表"""
    __tablename__ = "classe_type_relationship"
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'), primary_key=True)
    classes = db.relationship('Course')

class CourseWare(db.Model):
    """ 课件 """
    __tablename__ = 'coursewares'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))  # 文件名
    filehash = db.Column(db.String(255))
    filekey = db.Column(db.String(100))  # 七牛上的文件名
    filesize = db.Column(db.Integer)  # 文件大小 单位 B
    bucketname = db.Column(db.String(50))
    domain = db.Column(db.String(255))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    lesson_id=db.Column(db.Integer,db.ForeignKey('lessons.id'))
    created_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 上传时间
    is_free = db.Column(db.Integer, default=0)  # 是否免费下载，默认和Lesson 的权限一致

    # lesson = db.relationship('Lesson')


class CourseWareDownload(db.Model):
      """ 课件下载记录 """
      __tablename__ = 'courseware_download'
      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
      courseware_id = db.Column(db.Integer, db.ForeignKey('coursewares.id'))
      download_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 下载时间


class CourseComment(db.Model):
    """ 课程评论 """
    __tablename__ = 'classcomments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)    # 评论内容
    score = db.Column(db.Integer,default=5)    # 打分
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id')) # 在课程详情页面评论时只记录课程ID，不记录课时ID
    lesson_id =db.Column(db.Integer, db.ForeignKey('lessons.id')) #在播放页面评论时记录课时ID和课程ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User',
        backref=db.backref('comments', lazy='dynamic'))


class CourseNote(db.Model):
    """ 课程笔记 """
    __tablename__ = 'classnotes'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text)   # 课程笔记
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    position = db.Column(db.Float) #笔记在视频中的位置
    img_url = db.Column(db.String(200)) #视频截图地址
    is_open = db.Column(db.Integer,default=1) #是否公开笔记,1 公开，0 私有

    user = db.relationship('User',
        backref=db.backref('notes', lazy='dynamic'))

    lesson = db.relationship('Lesson')


class CourseFavorites(db.Model):
    """ 课程收藏表 """
    __tablename__ = 'classfavorites'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    created_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 添加时间
    clazz = db.relationship('Course')


class Chapter(db.Model):
    """ 章节实体类 """
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))  # 章节标题
    lessons = db.relationship("Lesson",order_by="Lesson.bsort")
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

    def __unicode__(self):
        return '%s' % self.title


class Compilation(db.Model):
    """ 视频合辑实体 """
    __tablename__ = 'compilations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    created_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 发布时间
    videoes = db.relationship('Video')

    def to_Json(self):
        return {
            'id':self.id,
            'name':self.name,
            'created_time': self.created_time
        }

    def format_date(self):

        if self.created_time is not None:
           return self.created_time.strftime("%Y-%m-%d %H:%M:%S")

        return ''


class Lesson(db.Model):
    """ 课时实体 """
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # 课时标题
    desc = db.Column(db.Text)  # 课时介绍
    created_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 发布时间
    state = db.Column(db.Integer, default=0)  # 状态
    is_free = db.Column(db.Integer, default=0)  # 是否收费
    pub_tag = db.Column(db.Integer, default=0)  # 更新标识
    img_url = db.Column(db.String(255))  # 封面地址
    video_id = db.Column(db.Integer,db.ForeignKey('videos.id'))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))  # 章节
    bsort = db.Column(db.Integer, default=0)


    video = db.relationship('Video')

    def __unicode__(self):
        return u'%s' % self.name


class LessonPlay(db.Model):
    """ 课时学习记录表 """
    __tablename__ = 'lesson_play'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    lesson_id = db.Column(db.Integer,db.ForeignKey('lessons.id'))
    play_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 播放时间
    start_position=db.Column(db.Integer,default=0) #开始播放的位置
    position = db.Column(db.Integer,default=0) # 当前播放进度
    lesson_duration = db.Column(db.Integer,default=0) #课时总时长
    play_duration = db.Column(db.Integer,default=0) #学习了多少时间
    end_time = db.Column(db.TIMESTAMP) #结束播放时间
    ip_addr=db.Column(db.String(20)) #播放时候的IP地址

    is_finished = db.Column(db.Boolean,default=False) #是否学完该课时，lesson_duration - play_duration < 2 可认为学完该课时
    user = db.relationship('User',
        backref=db.backref('lesson_study_list', lazy='dynamic'))

    lesson = db.relationship('Lesson')


class LessonStudy(db.Model):
    """ 课时学习记录表 """
    __tablename__ = 'lesson_study'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    lesson_id = db.Column(db.Integer,db.ForeignKey('lessons.id'))
    start_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 播放时间
    update_time = db.Column(db.TIMESTAMP)  # 最后一次更新时间
    learn_time = db.Column(db.Integer) # 学习总时间，每次累加，单位秒
    status = db.Column(db.Integer,default=1) #状态，1：学习中，2：学完


class CourseStudy(db.Model):
    """ 学习进度表 """
    __tablename__ = 'classstudy'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 开始学习时间
    progress = db.Column(db.Integer,default=0) # 当前学习进度，例如：课程共10个课时，当前学到了第5个课时，那进度就是 5
    is_finish=db.Column(db.Boolean,default=False) #是否完成学习
    clazz = db.relationship('Course')


class Video(db.Model):
    """ 视频文件 """
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))  # 本地文件名
    filehash = db.Column(db.String(255))
    filekey = db.Column(db.String(100))  # 七牛上的文件名
    filesize = db.Column(db.Integer)  # 文件大小 单位 B
    bucketname = db.Column(db.String(50))
    domain = db.Column(db.String(200))
    duration = db.Column(db.Integer)  # 时长：(秒）
    createtime = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    creator = db.Column(db.Integer)  # 创建者
    compilation = db.Column(db.Integer, db.ForeignKey('compilations.id'))  # 视频合辑

    def __unicode__(self):
        return u'%s' % (self.filename, )


class QQGroup(db.Model):
    """ QQ 群 """
    __tablename__ = 'qqgroup'

    id = db.Column(db.Integer, primary_key=True);
    group_name = db.Column(db.String(255));
    group_num = db.Column(db.String(20));
    group_link = db.Column(db.String(255));
    createtime = db.Column(db.TIMESTAMP, default=datetime.now())  # 创建时间
    desc = db.Column(db.String(255))
    #classes = db.relationship('Class')


class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True);
    name = db.Column(db.String(50), unique=True)  # Banner标题
    file_name = db.Column(db.String(100))  # 7牛上的文件名，用于删除图片文件
    img_url = db.Column(db.String(255))  # Banner图片URL
    redirect_url = db.Column(db.String(255))  # 点击跳转地址
    bg_color = db.Column(db.String(10))
    is_blank = db.Column(db.Boolean, default=True)  # 是否打开新窗口
    order_num = db.Column(db.Integer, default=0)  # 排序
    state = db.Column(db.Integer, default=0)  # 状态：0：启用


class FriendLink(db.Model):
    __tablename__ = 'friendlink'
    id = db.Column(db.Integer, primary_key=True);
    site_name = db.Column(db.String(100))  # 网站名称
    site_url = db.Column(db.String(255))  # 网站地址
    title = db.Column(db.String(100))  # 显示友链的文字
    contact = db.Column(db.String(200))  # 联系方式
    created_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 添加时间
    state = db.Column(db.Integer, default=0)  # 状态：0：启用


class PhoneMessage(db.Model):
    __tablename__ = 'phonemessages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    use_for = db.Column(db.String(50)) #用于做什么，buy: 购买验证
    phone = db.Column(db.String(15)) #手机号码
    code = db.Column(db.String(10)) # 验证码
    message = db.Column(db.String(200))
    send_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 发送时间
    send_type=db.Column(db.Integer,default=0) # 0为短信发送类型，1为邮件发送类型
    email=db.Column(db.String(50)) # 邮箱地址，send_type 为1 时才有值


class SocialUser(db.Model):
    __tablename__ = 'social_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 用户
    open_id=db.Column(db.String(64))
    type=db.Column(db.String(20)) #账号类型 qq，weibo ，wechat
    access_token=db.Column(db.String(64))
    expire_in = db.Column(db.String(20))  # 过期值
    nickname=db.Column(db.String(20))
    head_url = db.Column(db.String(255))  # 头像URL
    gender=db.Column(db.String(10)) #性别
    status = db.Column(db.Integer,default=1) # 1正常，0解绑


class SociaUserModel(json.JSONEncoder):
    nickname=''
    head_url=''
    channel=''
    gender=''

    def __init__(self,nickname,head_url,channel,gender):
        self.nickname=nickname
        self.head_url=head_url
        self.channel=channel
        self.gender=gender




class UserMsg(db.Model):
     """ 用户通知 """
     __tablename__ = 'user_msg'
     id = db.Column(db.Integer, primary_key=True)
     conversation_id = db.Column(db.String(64),unique=True) #会话ID,由 from_user_id + to _user_id 组成
     title = db.Column(db.String(100)) #标题
     msg = db.Column(db.String(500)) #通知内容
     send_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 发送时间
     from_user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #发信人ID
     to_user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 收信人ID
     orientation = db.Column(db.Integer,default=0) #  0是接收消息，1是发送消息
     msg_type = db.Column(db.Integer,default=0) #消息类型，0为系统消息，1为用户消息
     is_read=db.Column(db.Integer,default=0)
     read_time=db.Column(db.TIMESTAMP) # 阅读时间
     to_user = db.relationship("User",foreign_keys='[UserMsg.to_user_id]')
     from_user = db.relationship("User",foreign_keys=from_user_id,primaryjoin=from_user_id==User.id)



class SysNotification(db.Model):
     """ 系统通知 """
     __tablename__ = 'sys_notification'
     id = db.Column(db.Integer, primary_key=True)
     msg = db.Column(db.String(255)) #通知内容
     create_time = db.Column(db.TIMESTAMP, default=datetime.now())  # 添加时间
     end_time = db.Column(db.TIMESTAMP)  # 结束时间



class Coupon(db.Model):
    """ 优惠劵 """
    __tablename__ = 'coupon'
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.Integer) #面额
    code =db.Column(db.String(15)) #编码
    created_time = db.Column(db.DateTime, default=datetime.now)     # 创建时间
    expiry_time = db.Column(db.DateTime)     # 失效时间
    state = db.Column(db.Integer,default=1) # 1：未使用，2：已领取，3：已使用

    payback = db.Column(db.Integer,default=0) # 返现金额
    user_for_type = db.Column(db.Integer) # 0：优惠码， 3：课程
    user_for_id = db.Column(db.Integer) #使用产品的ID
    use_for_title = db.Column(db.String(50)) #使用产品的ID
    giver = db.Column(db.Integer) #赠予者ID，系统发放ID为 0
    owner = db.Column(db.Integer) #拥有该优惠卷用户ID
    allow_give = db.Column(db.Boolean) #是否允许赠送他人
    get_time = db.Column(db.DateTime)     # 获取时间
    use_time = db.Column(db.DateTime) #使用时间

    remark = db.Column(db.String(50)) #备注
    #type = db.Column(db.Integer,default=1) # 1：优惠券，2：红包，3：现金抵扣券


class ClassTypeEncoder(json.JSONEncoder):
    """ 课程类型 json 编码 """

    def default(self, obj):
        if isinstance(obj, ClassType):
            return {"id": obj.id, "name": obj.name}
        return json.JSONEncoder.default(self, obj)



class ForumThreadRelation(db.Model):

     """ 板块和帖子关联 """
     __tablename__ = 'forum_thread_relation'
     id = db.Column(db.Integer, primary_key=True)
     forum_id=db.Column(db.Integer, db.ForeignKey('forum.id'), primary_key=True)
     thread_id=db.Column(db.Integer, db.ForeignKey('thread.id'),primary_key=True)
     created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间



class Forum(db.Model):

     """ 板块 """
     __tablename__ = 'forum'
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(200)) #标题
     intro = db.Column(db.String(500)) #简介
     logo_url = db.Column(db.String(200)) #图标地址
     created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
     # admin_id = db.Column(db.Integer,db.ForeignKey('users.id')) #管理员ID
     type= db.Column(db.Integer,default=1) #板块类型:1 普通板块 2:活动板块 3: 课程板块
     course_type=db.Column(db.Integer) #1：班级 3：课程,当type 为3时该字段才有效
     is_online= db.Column(db.Integer,default=0) #是否上线,0:未上线,1:上线
     order_num=db.Column(db.Integer) #排序
     thread_count=db.Column(db.Integer) #文章总数
     is_thread_check = db.Column(db.Integer) # 是否开启发帖审核
     is_display=db.Column(db.Integer) # 是否显示

     admins = db.relationship('ForumAdmin')

     def is_normal_forum(self):
         return self.type==1

     def is_course_forum(self):
         return self.type==3






class ForumAdmin(db.Model):

     """ 板块管理员表 """
     __tablename__ = 'forum_admin'
     id = db.Column(db.Integer, primary_key=True)
     forum_id = db.Column(db.Integer, db.ForeignKey('forum.id')) #板块ID
     user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 管理员ID
     type =db.Column(db.Integer) # 1正管理员,0 :副管理员
     status = db.Column(db.Integer) #0取消管理员权限 1:正常

     user = db.relationship('User')




class Thread(db.Model):



     """ 帖子表 """
     __tablename__ = 'thread'
     # __searchable__ = ['title', 'content']
     # __analyzer__=ChineseAnalyzer()
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100)) #标题
     content = db.Column(db.Text)    # 评论内容
     brief = db.Column(db.String(200))    # 简介
     imgs=db.Column(db.String(2000)) #图片链接
     class_id = db.Column(db.Integer, db.ForeignKey('classes.id')) # 针对于某个课程的帖子，不写为0
     lesson_id =db.Column(db.Integer, db.ForeignKey('lessons.id')) #针对于某个课程某个课时的帖子，不写为0
     user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 发帖人ID
     ip_address=db.Column(db.String(20)) #发帖IP地址
     created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
     last_update_time = db.Column(db.DateTime, default=datetime.now())  # 上次更新时间
     last_comment_time = db.Column(db.DateTime)  # 最后评论时间
     read_count = db.Column(db.Integer,default=0) # 中阅读次数
     reply_count = db.Column(db.Integer,default=0) #总回帖次数
     like_count = db.Column(db.Integer,default=0) #喜欢次数
     is_original = db.Column(db.Integer) #是否原创,0:否,1:是
     is_top = db.Column(db.Integer,default=0) #是否置顶
     is_hot = db.Column(db.Integer,default=0) #是否热门
     thread_type = db.Column(db.Integer,default=0) # 0 博客,1 帖子, 2 提问
     status = db.Column(db.Integer,default=0) #状态 0:等待审核,1: 审核通过 ;2 未通过审核, -1 删除

     user = db.relationship('User')

     def first_img(self):

         if self.imgs is not None:
             links = self.imgs.split(",")
             if len(links)>0:
                 return links[0]

         return None;

class ThreadLike(db.Model):

     """ 帖子喜欢表 """
     __tablename__ = 'thread_like'
     id = db.Column(db.Integer, primary_key=True)
     thread_id = db.Column(db.Integer, db.ForeignKey('thread.id')) # 帖子，Id
     user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 发帖人ID
     ip_address=db.Column(db.String(20)) #IP地址
     created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间

class ThreadRequest(db.Model):

     """ 投稿申请表 """
     __tablename__ = 'thread_request'
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100)) #标题
     url = db.Column(db.String(200)) #url 地址
     thread_id = db.Column(db.Integer, db.ForeignKey('thread.id')) # 帖子，Id
     forum_id = db.Column(db.Integer, db.ForeignKey('forum.id')) #板块ID
     request_user_id=db.Column(db.Integer, db.ForeignKey('users.id')) # 申请人ID
     request_time = db.Column(db.DateTime, default=datetime.now())  # 时间
     hand_user_id=db.Column(db.Integer, db.ForeignKey('users.id')) # 申请人ID
     hand_time=db.Column(db.DateTime)
     hand_time=db.Column(db.DateTime)
     msg=db.Column(db.String(500)) #处理反馈消息
     status = db.Column(db.Integer,default=0) # 0 等待处理,1:通过 ,2:不通过

class ThreadPost(db.Model):

     """ 帖子表 """
     __tablename__ = 'thread_post'
     id = db.Column(db.Integer, primary_key=True)
     content = db.Column(db.Text)    # 内容
     thread_id = db.Column(db.Integer, db.ForeignKey('thread.id')) # 帖子，Id
     class_id = db.Column(db.Integer, db.ForeignKey('classes.id')) # 针对于某个课程的帖子，不写为0
     lesson_id =db.Column(db.Integer, db.ForeignKey('lessons.id')) #针对于某个课程某个课时的帖子，不写为0
     user_id = db.Column(db.Integer, db.ForeignKey('users.id')) # 评论人ID
     ip_address=db.Column(db.String(20)) #评论IP地址
     created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
     status = db.Column(db.Integer,default=1) #1正常，0未审核通过
     user = db.relationship('User')

class ThreadAttachment(db.Model):
    """ 附件表 """
    __tablename__ = 'thread_attachment'
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id')) # 帖子，Id
    file_name = db.Column(db.String(200))    # 附件名称
    file_size = db.Column(db.Integer)    # kb
    file_key = db.Column(db.String(100))    #
    dl_url = db.Column(db.String(200)) #下载地址
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间





class TrainingClass(db.Model):

    """ 培训课程 """
    __tablename__ = 'training_class'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #标题
    intro=db.Column(db.String(500)) # 简介
    logo_url = db.Column(db.String(200)) #封面地址
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    price = db.Column(db.Float) #价格
    learn_days = db.Column(db.Integer) #学习周期
    qqgroup_id = db.Column(db.Integer,db.ForeignKey('qqgroup.id'))
    total_course = db.Column(db.Integer) #总课程数量
    total_lesson = db.Column(db.Integer) #总课时数量
    total_students = db.Column(db.Integer) #总学习数量
    status = db.Column(db.Integer) #0:未发布, 1:正常 ,
    type =db.Column(db.String(10)) # 课程类型：android ,ios ,html5 ....
    is_open = db.Column(db.Integer) #是否开放学习

    page_tilte =db.Column(db.String(100)) #页面标题
    page_keywords=db.Column(db.String(500))
    page_description=db.Column(db.String(500))

    qqgroup = db.relationship('QQGroup',
        backref=db.backref('trainingclass', lazy='dynamic'))


    modules = db.relationship('ClassModule', backref='training_class')

class TrainApply(db.Model):
    """ 培训报名申请表 """
    __tablename__ = 'train_apply'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer)
    user_id =db.Column(db.Integer) #用户ID
    username =db.Column(db.String(255)) #用户名
    realname =db.Column(db.String(255)) #姓名
    mobil =db.Column(db.String(12)) #手机
    qq =db.Column(db.String(15)) #QQ
    email =db.Column(db.String(50)) #邮箱
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间

    company =db.Column(db.String(255)) #学校或就职企业
    workyear =db.Column(db.String(255)) #工作年限
    remark = db.Column(db.String(500)) #留言说明
    status = db.Column(db.Integer,default=0) # 申请状态: 0 等待审核,1 :审核通过, 2:审核未通过

class ClassModule(db.Model):
    """ 培训课程 """
    __tablename__ = 'class_module'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #标题
    intro = db.Column(db.String(200)) # 简介
    target = db.Column(db.String(200)) #学习目标
    class_id = db.Column(db.Integer,db.ForeignKey('training_class.id'))
    learn_days = db.Column(db.Integer) #学习周期（天）
    total_course = db.Column(db.Integer) #总课程数量
    total_lesson = db.Column(db.Integer) #总课时数量
    sort_num = db.Column(db.Integer) # 排序
    price = db.Column(db.Float) #价格
    coin = db.Column(db.Integer) #虚拟币
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    status = db.Column(db.Integer) #1正常

    tasks = db.relationship('ClassTask', backref='class_module')


task_course_relation = db.Table('task_course_relation',
    db.Column('task_id', db.Integer, db.ForeignKey('class_task.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('classes.id'))
)



class ClassTask(db.Model):
    """ 学习任务表 """
    __tablename__ = 'class_task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #标题
    intro = db.Column(db.String(200)) # 简介
    class_id = db.Column(db.Integer,db.ForeignKey('training_class.id'))
    module_id = db.Column(db.Integer,db.ForeignKey('class_module.id'))
    price = db.Column(db.Float) #价格
    coin = db.Column(db.Integer) #虚拟币
    pay_cur_type = db.Column(db.Integer) # 使用人民币还是虚拟币支付 0:虚拟币,1:人民币,2:两者都可以
    total_course = db.Column(db.Integer) #总课程数量
    total_lesson = db.Column(db.Integer) #总课时数量
    min_study_days = db.Column(db.Integer) # 最小学习时间
    max_study_days = db.Column(db.Integer) # 最大学习时间
    sort_num = db.Column(db.Integer) # 排序
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    return_course_credit = db.Column(db.Integer,default=0) # 完成任务后返回学分
    status = db.Column(db.Integer) #0:未开放,1:正常
    task_type = db.Column(db.Integer) # 1 普通任务，2 扩展任务 ，3：项目任务

    courses = db.relationship('Course',
                              secondary=task_course_relation,
                              primaryjoin=task_course_relation.c.task_id==id,
                              backref=db.backref('tasks', lazy='dynamic'),
                                    lazy='dynamic')


class TrainUser(db.Model):
    """ 学习任务表 """
    __tablename__ = 'train_user'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer,db.ForeignKey('training_class.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_time = db.Column(db.DateTime, default=datetime.now())  # 加入时间
    ranking = db.Column(db.Integer,default=0) # 排名
    course_credit  = db.Column(db.Integer,default=0) # 学分
    current_task_id = db.Column(db.Integer,db.ForeignKey('user_train_study_record.id')) #当前任务ID
    status = db.Column(db.Integer) #1 :权限正常，0：权限关闭
    current_task = db.relationship('UserTrainStudyRecord')
    user = db.relationship("User")


class UserTrainStudyRecord(db.Model):
    """ 学习任务表 """
    __tablename__ = 'user_train_study_record'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer,db.ForeignKey('training_class.id'))
    module_id = db.Column(db.Integer,db.ForeignKey('class_module.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('class_task.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    should_start_time = db.Column(db.DateTime)  #计划开始时间
    should_finish_time = db.Column(db.DateTime) #计划结束时间

    reality_start_time = db.Column(db.DateTime)  #实际开始时间
    reality_finish_time = db.Column(db.DateTime) #实际结束时间

    type = db.Column(db.Integer) # 学习类型: 1:培训课程,2 :模块 ,3:任务
    status = db.Column(db.Integer) # 状态: 0:未开始学习, 1: 正在学习 ,2:完成学习,3:超时学习

    module = db.relationship('ClassModule')
    task = db.relationship('ClassTask')
    claz = db.relationship('TrainingClass')



class InviteRecord(db.Model):
    """ 邀请记录表 """
    __tablename__ = 'invite_record'
    id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer,db.ForeignKey('users.id')) # 邀请人ID
    register_id = db.Column(db.Integer,db.ForeignKey('users.id')) # 注册人ID
    reg_time =db.Column(db.DateTime,default=datetime.now())
    channel=db.Column(db.String(50)) #渠道
    coin = db.Column(db.Integer) #赠与鸟币数量
    vip_days = db.Column(db.Integer) #赠与VIP天数

    register = db.relationship("User",foreign_keys='[InviteRecord.register_id]')




class CourseCouponGoods(db.Model):
    """ 商品-课程优惠码 """
    __tablename__ = 'course_coupon_goods'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #标题
    intro = db.Column(db.String(200)) # 简介
    logo_url=db.Column(db.String(200))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    val = db.Column(db.Integer,default=0) # 优惠码面额
    price = db.Column(db.Integer,default=0) #价格
    expiry_date = db.Column(db.Integer)#过期时间,单位天
    stock = db.Column(db.Integer,default=0)#库存量
    is_virtual=db.Column(db.Integer,default=1) #是否是虚拟物品(虚拟物品指优惠码等)
    content = db.Column(db.Text)  # 详情内容

    status = db.Column(db.Integer)#状态


class GoodsOrder(db.Model):
    __tablename__ = 'goods_order'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(50),unique=True)  # 流水号
    title = db.Column(db.String(200))  # 订单名称
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    goods_id = db.Column(db.Integer)
    total_price = db.Column(db.Float)  # 订单总价
    created_time = db.Column(db.DateTime, default=datetime.now())  # 下单时间
    pay_type = db.Column(db.String(10)) #支付方式:coin 鸟币,rmb 人民币
    receiver =db.Column(db.String(20)) #收件人
    addr = db.Column(db.String(100)) #手机地址
    mobi = db.Column(db.String(11)) #手机好

    user = db.relationship('User')





class PageMenu(db.Model):
    __tablename__ = 'page_menu'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))  # 名字
    created_time = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    type = db.Column(db.Integer) #菜单类型
    sort =db.Column(db.Integer) #排序
    redirect_url =  db.Column(db.String(200)) #跳转地址







#################活动模块##########################

class ActivityPost(db.Model):
    __tablename__ = 'activity_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('thread_post.id'))
    created_time = db.Column(db.DateTime, default=datetime.now())  # 下单时间

    user = db.relationship('User')


###双11活动
class ActivityDoubleEleven(db.Model):
    __tablename__ = 'activity_11'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('classes.id'))
    sort_num = db.Column(db.Integer)
    type = db.Column(db.Integer)
    original_price = db.Column(db.Integer) #原价
    current_price = db.Column(db.Integer) #现价
    course = db.relationship("Course")