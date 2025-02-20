"""abstract user

Revision ID: f0745e889093
Revises: 690a9736b35f
Create Date: 2025-02-20 19:49:57.598625

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0745e889093'
down_revision: Union[str, None] = '690a9736b35f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students')
    op.drop_table('teachers')
    op.add_column('users', sa.Column('type', sa.String(length=50), nullable=False))
    op.add_column('users', sa.Column('education_programm', sa.String(), nullable=True))
    op.add_column('users', sa.Column('course', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'course')
    op.drop_column('users', 'education_programm')
    op.drop_column('users', 'type')
    op.create_table('teachers',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='teachers_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='teachers_pkey'),
    sa.UniqueConstraint('user_id', name='teachers_user_id_key')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('education_programm', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('course', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='students_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='students_pkey'),
    sa.UniqueConstraint('user_id', name='students_user_id_key')
    )
    # ### end Alembic commands ###
