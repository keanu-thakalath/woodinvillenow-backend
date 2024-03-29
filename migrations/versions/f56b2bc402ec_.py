"""empty message

Revision ID: f56b2bc402ec
Revises: 7a67c6a82e91
Create Date: 2023-02-03 21:06:37.941254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f56b2bc402ec'
down_revision = '7a67c6a82e91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_foreign_key(None, 'article_author_association', 'article', ['article_id'], ['id'])
    # op.create_foreign_key(None, 'article_author_association', 'author', ['author_id'], ['id'])
    # op.create_foreign_key(None, 'category_article_association', 'article', ['article_id'], ['id'])
    # op.create_foreign_key(None, 'category_article_association', 'category', ['category_id'], ['id'])
    # op.create_foreign_key(None, 'comment', 'article', ['article_id'], ['id'])
    # op.create_foreign_key(None, 'tag_article_association', 'article', ['article_id'], ['id'])
    # op.create_foreign_key(None, 'tag_article_association', 'tag', ['tag_id'], ['id'])
    # ### end Alembic commands ###
    pass


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag_article_association', type_='foreignkey')
    op.drop_constraint(None, 'tag_article_association', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'category_article_association', type_='foreignkey')
    op.drop_constraint(None, 'category_article_association', type_='foreignkey')
    op.drop_constraint(None, 'article_author_association', type_='foreignkey')
    op.drop_constraint(None, 'article_author_association', type_='foreignkey')
    # ### end Alembic commands ###
