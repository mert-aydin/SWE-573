"""image column name changed

Revision ID: a37ba311f9e5
Revises: 98538bc27652
Create Date: 2023-05-25 19:46:05.977661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a37ba311f9e5'
down_revision = '98538bc27652'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('base64_image', sa.String(), nullable=True))
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('base64_image')

    # ### end Alembic commands ###