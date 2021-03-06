"""empty message

Revision ID: 97574b96bf6f
Revises: 5ec2ae6fadcb
Create Date: 2020-07-12 13:11:10.836064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97574b96bf6f'
down_revision = '5ec2ae6fadcb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'activities', 'plans', ['plan_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'activities', type_='foreignkey')
    # ### end Alembic commands ###
