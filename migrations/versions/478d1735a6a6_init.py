"""init

Revision ID: 478d1735a6a6
Revises: None
Create Date: 2015-05-27 11:55:11.599358

"""

# revision identifiers, used by Alembic.
revision = '478d1735a6a6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('sort', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qqgroup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=255), nullable=True),
    sa.Column('group_num', sa.String(length=20), nullable=True),
    sa.Column('createtime', sa.TIMESTAMP(), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=30), nullable=True),
    sa.Column('month_price', sa.Integer(), nullable=True),
    sa.Column('year_price', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('product_name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('mobi', sa.String(length=15), nullable=True),
    sa.Column('mobile_confirmed', sa.Boolean(), nullable=True),
    sa.Column('qq', sa.String(length=128), nullable=True),
    sa.Column('money', sa.Float(), nullable=True),
    sa.Column('real_name', sa.String(length=20), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('reg_time', sa.DateTime(), nullable=True),
    sa.Column('logo_url', sa.String(length=255), nullable=True),
    sa.Column('user_type', sa.Integer(), nullable=True),
    sa.Column('channel', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('friendlink',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_name', sa.String(length=100), nullable=True),
    sa.Column('site_url', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('contact', sa.String(length=200), nullable=True),
    sa.Column('created_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('banner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('file_name', sa.String(length=100), nullable=True),
    sa.Column('img_url', sa.String(length=255), nullable=True),
    sa.Column('redirect_url', sa.String(length=255), nullable=True),
    sa.Column('bg_color', sa.String(length=10), nullable=True),
    sa.Column('is_blank', sa.Boolean(), nullable=True),
    sa.Column('order_num', sa.Integer(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_activate_email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('token', sa.String(length=200), nullable=True),
    sa.Column('send_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('activate_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('compilations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('lessons_count', sa.Integer(), nullable=True),
    sa.Column('lessons_finished_count', sa.Integer(), nullable=True),
    sa.Column('lessons_time', sa.Integer(), nullable=True),
    sa.Column('lessons_played_time', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.Column('recommend_count', sa.Integer(), nullable=True),
    sa.Column('class_type', sa.Integer(), nullable=True),
    sa.Column('second_class_type', sa.Integer(), nullable=True),
    sa.Column('class_difficulty', sa.Integer(), nullable=True),
    sa.Column('key_words', sa.String(length=255), nullable=True),
    sa.Column('fit_to', sa.String(length=255), nullable=True),
    sa.Column('img_url', sa.String(length=255), nullable=True),
    sa.Column('is_have_copyright', sa.Boolean(), nullable=True),
    sa.Column('is_free', sa.Boolean(), nullable=True),
    sa.Column('is_online', sa.Integer(), nullable=True),
    sa.Column('qqgroup_id', sa.Integer(), nullable=True),
    sa.Column('play_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['qqgroup_id'], ['qqgroup.id'], ),
    sa.ForeignKeyConstraint(['second_class_type'], ['class_types.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_num', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('product_order_id', sa.Integer(), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=True),
    sa.Column('pay_channel', sa.String(length=20), nullable=True),
    sa.Column('trade_status', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('operation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_num')
    )
    op.create_table('teacher_student_follows',
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('teacher_id', 'student_id')
    )
    op.create_table('products_orders_relationship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('order_time', sa.DateTime(), nullable=True),
    sa.Column('cancel_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('filehash', sa.String(length=255), nullable=True),
    sa.Column('filekey', sa.String(length=100), nullable=True),
    sa.Column('filesize', sa.Integer(), nullable=True),
    sa.Column('bucketname', sa.String(length=50), nullable=True),
    sa.Column('domain', sa.String(length=200), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('creator', sa.Integer(), nullable=True),
    sa.Column('compilation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['compilation'], ['compilations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phonemessages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('use_for', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('message', sa.String(length=200), nullable=True),
    sa.Column('send_time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_discount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('discount_price', sa.Float(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('social',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('suid', sa.String(length=255), nullable=True),
    sa.Column('suname', sa.String(length=255), nullable=True),
    sa.Column('sex', sa.String(length=255), nullable=True),
    sa.Column('logo_url', sa.String(length=255), nullable=True),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('expirein', sa.String(length=255), nullable=True),
    sa.Column('sessionkey', sa.String(length=255), nullable=True),
    sa.Column('sessionsecret', sa.String(length=255), nullable=True),
    sa.Column('social_uid', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_product_relationship',
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('class_id', 'product_id')
    )
    op.create_table('classfavorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classnotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classstudy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.Column('is_finish', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classe_type_relationship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('class_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['class_type_id'], ['class_types.id'], ),
    sa.PrimaryKeyConstraint('id', 'class_id', 'class_type_id')
    )
    op.create_table('user_product_discount',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('discount_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['discount_id'], ['product_discount.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chapters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('created_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('is_free', sa.Integer(), nullable=True),
    sa.Column('img_url', sa.String(length=255), nullable=True),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('chapter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classcomments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_time', sa.DateTime(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lesson_play',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('play_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('start_position', sa.Integer(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('lesson_duration', sa.Integer(), nullable=True),
    sa.Column('play_duration', sa.Integer(), nullable=True),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('is_finished', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coursewares',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.Column('filehash', sa.String(length=255), nullable=True),
    sa.Column('filekey', sa.String(length=100), nullable=True),
    sa.Column('filesize', sa.Integer(), nullable=True),
    sa.Column('bucketname', sa.String(length=50), nullable=True),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('created_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('is_free', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courseware_download',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('courseware_id', sa.Integer(), nullable=True),
    sa.Column('download_time', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['courseware_id'], ['coursewares.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courseware_download')
    op.drop_table('coursewares')
    op.drop_table('lesson_play')
    op.drop_table('classcomments')
    op.drop_table('lessons')
    op.drop_table('chapters')
    op.drop_table('user_product_discount')
    op.drop_table('classe_type_relationship')
    op.drop_table('classstudy')
    op.drop_table('classnotes')
    op.drop_table('classfavorites')
    op.drop_table('class_product_relationship')
    op.drop_table('social')
    op.drop_table('product_discount')
    op.drop_table('phonemessages')
    op.drop_table('videos')
    op.drop_table('products_orders_relationship')
    op.drop_table('teacher_student_follows')
    op.drop_table('orders')
    op.drop_table('classes')
    op.drop_table('user_follows')
    op.drop_table('compilations')
    op.drop_table('user_activate_email')
    op.drop_table('banner')
    op.drop_table('friendlink')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('qqgroup')
    op.drop_table('class_types')
    ### end Alembic commands ###
