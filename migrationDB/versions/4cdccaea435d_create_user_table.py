"""create_user_table

Revision ID: 4cdccaea435d
Revises: 3faa5cfc21e9
Create Date: 2022-08-09 16:35:38.447168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cdccaea435d'
down_revision = '3faa5cfc21e9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                        sa.PrimaryKeyConstraint('id'),
                         sa.PrimaryKeyConstraint('email')
        )
    pass


def downgrade():
    op.drop_table('users')
    pass