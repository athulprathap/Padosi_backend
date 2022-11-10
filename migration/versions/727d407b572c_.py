"""empty message

Revision ID: 727d407b572c
Revises: 
Create Date: 2022-11-10 13:52:42.814612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '727d407b572c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('popular_search', sa.Column('counter', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('popular_search', 'counter')
    # ### end Alembic commands ###