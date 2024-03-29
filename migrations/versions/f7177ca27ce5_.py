"""empty message

Revision ID: f7177ca27ce5
Revises: f01fcda5d487
Create Date: 2024-01-03 22:49:17.180402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f7177ca27ce5'
down_revision = 'f01fcda5d487'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('consulta', schema=None) as batch_op:
        batch_op.alter_column('cantPacientes',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('nombreEspecialista',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('tipoConsulta',
               existing_type=mysql.ENUM('GENERAL', 'ESPECIALIZADA'),
               nullable=False)
        batch_op.alter_column('estado',
               existing_type=mysql.ENUM('ACTIVO', 'INACTIVO', 'PENDIENTE'),
               nullable=False)
        batch_op.alter_column('hospital_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    with op.batch_alter_table('paciente', schema=None) as batch_op:
        batch_op.alter_column('nombre',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('edad',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('noHistoriaClinica',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('tipo',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('hospital_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('paciente', schema=None) as batch_op:
        batch_op.alter_column('hospital_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('tipo',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('noHistoriaClinica',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('edad',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('nombre',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    with op.batch_alter_table('consulta', schema=None) as batch_op:
        batch_op.alter_column('hospital_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('estado',
               existing_type=mysql.ENUM('ACTIVO', 'INACTIVO', 'PENDIENTE'),
               nullable=True)
        batch_op.alter_column('tipoConsulta',
               existing_type=mysql.ENUM('GENERAL', 'ESPECIALIZADA'),
               nullable=True)
        batch_op.alter_column('nombreEspecialista',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('cantPacientes',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
