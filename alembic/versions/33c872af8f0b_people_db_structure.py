"""people_db_structure

Revision ID: 33c872af8f0b
Revises: 
Create Date: 2022-11-06 22:30:23.464870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '33c872af8f0b'
down_revision = None
branch_labels = None
depends_on = None


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grade_to_child')
    op.drop_table('parent_to_child')
    op.drop_table('roles')
    op.drop_table('item')
    op.drop_index('ix_people_nickname', table_name='people')
    op.drop_table('people')
    op.drop_table('grades')
    # ### end Alembic commands ###


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parent_to_child',
    sa.Column('parent_nickname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('child_nickname', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['child_nickname'], ['people.nickname'], name='parent_to_child_child_nickname_fkey'),
    sa.ForeignKeyConstraint(['parent_nickname'], ['people.nickname'], name='parent_to_child_parent_nickname_fkey')
    )
    op.create_table('grades',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('grades_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('grade_num', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('grade_letter', sa.VARCHAR(length=1), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='grades_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('people',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('people_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('patronymic', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('nickname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('last_seen', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('birth_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('role', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('profile_pic', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='people_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_people_nickname', 'people', ['nickname'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='item_pkey')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='roles_pkey')
    )
    op.create_table('grade_to_child',
    sa.Column('grade_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('child_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['people.id'], name='grade_to_child_child_id_fkey'),
    sa.ForeignKeyConstraint(['grade_id'], ['grades.id'], name='grade_to_child_grade_id_fkey')
    )
    # ### end Alembic commands ###