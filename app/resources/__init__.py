from flask_smorest import Blueprint

author_bp = Blueprint('author', 'author', url_prefix='/api')
article_bp = Blueprint('article', 'article', url_prefix='/api')
comment_bp = Blueprint('comment', 'comment', url_prefix='/api')
category_bp = Blueprint('category', 'category', url_prefix='/api')
tag_bp = Blueprint('tag', 'tag', url_prefix='/api')
newsletter_bp = Blueprint('newsletter', 'newsletter', url_prefix='/api')
analytics_bp = Blueprint('analytics', 'analytics', url_prefix='/api')

from app.resources import author, article, comment, category, tag, newsletter, analytics, utils