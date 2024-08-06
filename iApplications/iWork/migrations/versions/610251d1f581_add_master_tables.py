"""add master tables

Revision ID: 610251d1f581
Revises: d975b24be31f
Create Date: 2024-08-02 14:01:09.226711

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '610251d1f581'
down_revision = 'd975b24be31f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Your autogenerated commands here
    op.create_table('activities_master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('activity_type', sa.String(length=150), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('beneficiaries_type_master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('beneficiary_type', sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('categories_master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('major_heads_master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('major_head', sa.String(length=150), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories_master.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('work_types_master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('work_type', sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('proposed_status_master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('proposed_status', sa.String(length=80), nullable=False),
        sa.Column('work_type_id', sa.Integer(), nullable=False),
        sa.Column('major_head_id', sa.Integer(), nullable=False),
        sa.Column('activity_type_id', sa.Integer(), nullable=False),
        sa.Column('beneficiary_type_id', sa.Integer(), nullable=False),
        sa.Column('master_work_type_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['major_head_id'], ['major_heads_master.id'], ),
        sa.ForeignKeyConstraint(['activity_type_id'], ['activities_master.id'], ),
        sa.ForeignKeyConstraint(['beneficiary_type_id'], ['beneficiaries_type_master.id'], ),
        sa.ForeignKeyConstraint(['master_work_type_id'], ['work_types_master.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    # Grant permissions
    op.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO zeidwhrc;")

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Your autogenerated commands here
    op.drop_table('proposed_status_master')
    op.drop_table('work_types_master')
    op.drop_table('major_heads_master')
    op.drop_table('categories_master')
    op.drop_table('beneficiaries_type_master')
    op.drop_table('activities_master')
    # ### end Alembic commands ###

    # Revoke permissions if necessary
    op.execute("REVOKE ALL PRIVILEGES ON SCHEMA public FROM zeidwhrc;")
