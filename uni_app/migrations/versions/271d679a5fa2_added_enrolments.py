"""added enrolments

Revision ID: 271d679a5fa2
Revises: 9535af8e35b1
Create Date: 2021-11-24 10:56:05.845321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '271d679a5fa2'
down_revision = '9535af8e35b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('enrolments',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['flasklogin-users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('enrolments')
    # ### end Alembic commands ###
