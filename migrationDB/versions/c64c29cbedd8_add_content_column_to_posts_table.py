"""add content column to posts table

Revision ID: c64c29cbedd8
Revises: 4a528c0a63c4
Create Date: 2022-07-22 18:13:03.319607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c64c29cbedd8'
down_revision = '4a528c0a63c4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

