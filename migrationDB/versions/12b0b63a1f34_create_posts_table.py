"""create posts table

Revision ID: 12b0b63a1f34
Revises: 
Create Date: 2022-07-21 15:36:34.854495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12b0b63a1f34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass

