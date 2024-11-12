"""added parameter_order

Revision ID: 1af854534eb4
Revises: 3ebf3c1fe9ef
Create Date: 2024-09-28 16:33:59.740295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af854534eb4'
down_revision = '3ebf3c1fe9ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inputs_and_permissibles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parameter_order', sa.Integer(), nullable=True))

    # ### end Alembic commands ###

    # Grant permissions
    op.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO zeidwhrc;")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inputs_and_permissibles', schema=None) as batch_op:
        batch_op.drop_column('parameter_order')

    # ### end Alembic commands ###

    # Revoke permissions if necessary
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM zeidwhrc;")