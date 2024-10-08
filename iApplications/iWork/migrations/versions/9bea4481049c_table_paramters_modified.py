"""table paramters modified

Revision ID: 9bea4481049c
Revises: 44a7952c3c62
Create Date: 2024-09-04 14:54:30.451644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bea4481049c'
down_revision = '44a7952c3c62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('input_parameters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('element_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('constraint', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###

    # Grant permissions
    op.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO zeidwhrc;")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('input_parameters', schema=None) as batch_op:
        batch_op.drop_column('constraint')
        batch_op.drop_column('element_type')

    # ### end Alembic commands ###

    # Revoke permissions if necessary
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM zeidwhrc;")
