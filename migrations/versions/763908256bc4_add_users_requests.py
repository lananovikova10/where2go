"""add users requests

Revision ID: 763908256bc4
Revises: 607846e54cd4
Create Date: 2021-10-07 16:08:32.818464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '763908256bc4'
down_revision = '16eaf37e2edd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('country_dep', sa.String(length=120), nullable=True),
    sa.Column('country_arr', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_requests_country_arr'), 'users_requests', ['country_arr'], unique=False)
    op.create_index(op.f('ix_users_requests_country_dep'), 'users_requests', ['country_dep'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_requests_country_dep'), table_name='users_requests')
    op.drop_index(op.f('ix_users_requests_country_arr'), table_name='users_requests')
    op.drop_table('users_requests')
    # ### end Alembic commands ###
