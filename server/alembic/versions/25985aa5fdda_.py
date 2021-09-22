"""empty message

Revision ID: 25985aa5fdda
Revises: 
Create Date: 2021-09-22 22:15:21.683229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25985aa5fdda'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('yt_channels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('channel_id', sa.String(), nullable=True),
    sa.Column('group', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_yt_channels_channel_id'), 'yt_channels', ['channel_id'], unique=True)
    op.create_index(op.f('ix_yt_channels_first_name'), 'yt_channels', ['first_name'], unique=False)
    op.create_index(op.f('ix_yt_channels_group'), 'yt_channels', ['group'], unique=False)
    op.create_index(op.f('ix_yt_channels_id'), 'yt_channels', ['id'], unique=False)
    op.create_index(op.f('ix_yt_channels_last_name'), 'yt_channels', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_yt_channels_last_name'), table_name='yt_channels')
    op.drop_index(op.f('ix_yt_channels_id'), table_name='yt_channels')
    op.drop_index(op.f('ix_yt_channels_group'), table_name='yt_channels')
    op.drop_index(op.f('ix_yt_channels_first_name'), table_name='yt_channels')
    op.drop_index(op.f('ix_yt_channels_channel_id'), table_name='yt_channels')
    op.drop_table('yt_channels')
    # ### end Alembic commands ###
