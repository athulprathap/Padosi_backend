"""create users table

Revision ID: abf875e858c1
Revises: c64c29cbedd8
Create Date: 2022-07-25 16:41:05.567544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abf875e858c1'
down_revision = 'c64c29cbedd8'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False, primary_key=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('image', sa.String(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass