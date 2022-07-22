"""create posts table

Revision ID: 4a528c0a63c4
Revises: 
Create Date: 2022-07-22 17:57:09.920853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a528c0a63c4'
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

