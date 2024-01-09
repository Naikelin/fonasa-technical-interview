"""empty message

Revision ID: f01fcda5d487
Revises: 5f3ccd55089a
Create Date: 2024-01-03 21:56:57.627096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f01fcda5d487'
down_revision = '5f3ccd55089a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paciente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hospital_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'hospital', ['hospital_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paciente', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('hospital_id')

    # ### end Alembic commands ###