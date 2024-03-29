"""empty message

Revision ID: ca53335e510b
Revises: f56b2bc402ec
Create Date: 2023-02-03 21:08:23.861726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca53335e510b'
down_revision = 'f56b2bc402ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comment', 'content', type_=sa.String(1024), existing_type=sa.Text)
    op.alter_column('author', 'bio', type_=sa.String(1024), existing_type=sa.Text)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # ### end Alembic commands ###
    pass
