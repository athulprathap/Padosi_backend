"""empty message

Revision ID: fdadadbe23f4
Revises: 
Create Date: 2022-11-18 18:59:19.226135

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fdadadbe23f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('codes')
    op.drop_table('base')
    op.drop_table('my_otp_blocks')
    op.drop_table('my_otps')
    op.drop_table('blacklist')
    op.drop_table('my_codes')
    op.drop_table('my_rooms')
    op.drop_table('post')
    op.drop_table('my_bookings')
    op.drop_table('my_users')
    op.drop_table('my_blacklists')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_blacklists',
    sa.Column('token', sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('token', name='my_blacklists_pkey')
    )
    op.create_table('my_users',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('fullname', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='my_users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('my_bookings',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('agenda', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('start_date', sa.VARCHAR(length=10), autoincrement=False, nullable=True),
    sa.Column('start_time', sa.VARCHAR(length=6), autoincrement=False, nullable=True),
    sa.Column('end_time', sa.VARCHAR(length=6), autoincrement=False, nullable=True),
    sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('register_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='my_bookings_pkey')
    )
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('published', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['my_users.id'], name='post_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='post_pkey')
    )
    op.create_table('my_rooms',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='my_rooms_pkey')
    )
    op.create_table('my_codes',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('reset_code', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.Column('expired_in', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='my_codes_pkey')
    )
    op.create_table('blacklist',
    sa.Column('token', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.UniqueConstraint('token', name='blacklist_token_key')
    )
    op.create_table('my_otps',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('recipient_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('session_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('otp_code', sa.VARCHAR(length=6), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('otp_failed_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='my_otps_pkey')
    )
    op.create_table('my_otp_blocks',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('recipient_id', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='my_otp_blocks_pkey')
    )
    op.create_table('base',
    sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('created_by', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('updated_by', sa.VARCHAR(length=50), autoincrement=False, nullable=True)
    )
    op.create_table('codes',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('reset_code', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('expired_in', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='codes_pkey')
    )
    # ### end Alembic commands ###