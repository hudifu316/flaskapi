"""empty message

Revision ID: 6cd2c0d4c2ae
Revises: 243b864586f8
Create Date: 2020-07-12 15:45:28.847314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cd2c0d4c2ae'
down_revision = '243b864586f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'trips', 'transportation', ['transportation_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trips', type_='foreignkey')
    # ### end Alembic commands ###