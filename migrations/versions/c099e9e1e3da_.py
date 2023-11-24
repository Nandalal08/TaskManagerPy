"""empty message

Revision ID: c099e9e1e3da
Revises: c121043a2383
Create Date: 2023-11-22 15:49:13.993545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c099e9e1e3da'
down_revision = 'c121043a2383'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todo', schema=None) as batch_op:
        batch_op.drop_column('title')

    # ### end Alembic commands ###
