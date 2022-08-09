"""add content colunm to post table

Revision ID: 3faa5cfc21e9
Revises: a58aa441c890
Create Date: 2022-08-09 16:29:05.407828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3faa5cfc21e9'
down_revision = 'a58aa441c890'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
