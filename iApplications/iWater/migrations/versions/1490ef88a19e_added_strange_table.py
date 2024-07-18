"""added strange table

Revision ID: 1490ef88a19e
Revises: 3f4cbf7c420d
Create Date: 2023-12-21 14:53:22.163269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1490ef88a19e'
down_revision = '3f4cbf7c420d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('strange_runoff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rainfall_in_inches', sa.Integer(), nullable=False),
    sa.Column('rainfall_in_mm', sa.Float(), nullable=False),
    sa.Column('good_runoff', sa.Float(), nullable=False),
    sa.Column('average_runoff', sa.Float(), nullable=False),
    sa.Column('bad_runoff', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('rainfall_in_inches'),
    sa.UniqueConstraint('rainfall_in_mm')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('strange_runoff')
    # ### end Alembic commands ###