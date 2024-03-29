"""empty message

Revision ID: 1834ac117342
Revises: 46463e660d78
Create Date: 2018-10-14 01:54:41.471738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1834ac117342'
down_revision = '46463e660d78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('avatar', sa.Unicode(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'avatar')
    # ### end Alembic commands ###
