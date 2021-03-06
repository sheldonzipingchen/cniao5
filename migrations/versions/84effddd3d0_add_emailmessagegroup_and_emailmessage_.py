"""add EmailMessageGroup and EmailMessage model

Revision ID: 84effddd3d0
Revises: 2cecea8ea55c
Create Date: 2015-05-31 15:24:28.818370

"""

# revision identifiers, used by Alembic.
revision = '84effddd3d0'
down_revision = '2cecea8ea55c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('email_message_groups',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(length=50), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('email_messages',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('email', sa.String(length=150), nullable=True),
    # sa.Column('state', sa.Integer(), nullable=True),
    # sa.Column('created_date', sa.DateTime(), nullable=True),
    # sa.Column('send_date', sa.DateTime(), nullable=True),
    # sa.Column('email_message_group_id', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['email_message_group_id'], ['email_message_groups.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.drop_table(u'user_msg')
    # op.create_unique_constraint(None, 'users', ['email'])
    # op.create_unique_constraint(None, 'users', ['username'])
    ### end Alembic commands ###
    pass


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'users')
    # op.drop_constraint(None, 'users')
    # op.create_table(u'user_msg',
    # sa.Column(u'id', mysql.INTEGER(display_width=11), nullable=False),
    # sa.Column(u'title', mysql.VARCHAR(length=100), nullable=True),
    # sa.Column(u'msg', mysql.VARCHAR(length=500), nullable=True),
    # sa.Column(u'user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    # sa.Column(u'is_read', mysql.INTEGER(display_width=11), server_default='0', autoincrement=False, nullable=True),
    # sa.PrimaryKeyConstraint(u'id'),
    # mysql_default_charset=u'utf8',
    # mysql_engine=u'InnoDB'

    #)
    pass
    # op.drop_table('email_messages')
    # op.drop_table('email_message_groups')
    ### end Alembic commands ###
