"""create post table

Revision ID: a58aa441c890
Revises: 
Create Date: 2022-08-09 16:22:04.112055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a58aa441c890'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',  sa.Column('id', sa.Integer(), nullable=False, 
                        primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
