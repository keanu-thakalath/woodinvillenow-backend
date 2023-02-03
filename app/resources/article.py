from flask.views import MethodView
from flask_smorest import abort
from app.models import Tag, TagArticleAssociation, Category, CategoryArticleAssociation, Author, ArticleAuthorAssociation, Article
from app.schemas import ArticleQueryArgsSchema, ArticleSchema, ArticleBasicSchema
from app.resources import article_bp as bp
from app.resources.utils import validate_slug
from app import httpauth, db

def get_article(url_slug, user=None):
    article = Article.query.filter_by(url_slug=url_slug).first() if user else Article.query.filter_by(url_slug=url_slug, draft=False).first()
    if not article:
        abort(404, message='Article does not exist.')
    return article

def validate_authors(author_ids, article):
    for author_id in author_ids:
        if not Author.query.get(author_id):
            abort(400, message='Unknown author_id.')
        db.session.add(ArticleAuthorAssociation(author_id=author_id, article=article))

def validate_categories(category_ids, article):
    for category_id in category_ids:
        if not Category.query.get(category_id):
            abort(400, message='Unknown category_id.')
        db.session.add(CategoryArticleAssociation(category_id=category_id, article=article))

def validate_tags(tag_ids, article):
    for tag_id in tag_ids:
        if not Tag.query.get(tag_id):
            abort(400, message='Unknown tag_id.')
        db.session.add(TagArticleAssociation(tag_id=tag_id, article=article))

def validate_cover_img_style(cover_img_style):
    if cover_img_style not in Article.cover_img_styles:
        abort(400, message='Unknown cover image style.')

# refactor get_{model} -> utils.py
@bp.route('/articles')
class ArticlesView(MethodView):
    @httpauth.login_required(optional=True)
    @bp.arguments(ArticleQueryArgsSchema, location='query')
    @bp.response(200, ArticleBasicSchema(many=True))
    def get(self, args):
        '''
        Returns basic information about all articles.

        Authentication optional.\n
        sort_by: 'views' | default (datetime)\n
        limit > 0
        '''
        query = Article.query
        
        if not httpauth.current_user():
            query = query.filter_by(draft=False)
        
        if q:=args.get('query'):
            query = query.filter(Article.title.ilike(f'%{q}%'))
        
        if author:=args.get('author'):
            query = query.filter(Article.authors.any(ArticleAuthorAssociation.author.has(Author.url_slug == author)))

        if category:=args.get('category'):
            query = query.filter(Article.categories.any(CategoryArticleAssociation.category.has(Category.url_slug == category)))
        
        if tag:=args.get('tag'):
            query = query.filter(Article.tags.any(TagArticleAssociation.tag.has(Tag.url_slug == tag)))

        if args.get('sort_by') == 'views':
            query = query.order_by(Article.views.desc())
        else:
            query = query.order_by(Article.datetime.desc())
        
        if page:=args.get('page'):
            articles = query.paginate(page=page, per_page=args.get('limit', 1), error_out=False).items
        elif args.get('limit', 0) > 0:
            articles = query.limit(args['limit']).all()
        else:
            articles = query.all()

        return articles
    
    @httpauth.login_required()
    @bp.arguments(ArticleSchema, as_kwargs=True)
    @bp.response(201, ArticleBasicSchema)
    def post(self, tag_ids, category_ids, author_ids, **article_data):
        url_slug = validate_slug(Article, article_data['title'])
        validate_cover_img_style(article_data['cover_img_style'])

        article = Article(**article_data, url_slug=url_slug)
        validate_authors(author_ids, article)
        validate_categories(category_ids, article)
        validate_tags(tag_ids, article)
        db.session.add(article)
        db.session.commit()
        return article

@bp.route('/articles/<url_slug>')
class ArticleView(MethodView):
    @httpauth.login_required(optional=True)
    @bp.response(200, ArticleSchema)
    def get(self, url_slug):
        '''
        Returns all information about an article.

        Authentication optional.
        '''
        return get_article(url_slug, httpauth.current_user())

    @httpauth.login_required()
    @bp.arguments(ArticleSchema, as_kwargs=True)
    @bp.response(200, ArticleBasicSchema)
    def put(self, url_slug, tag_ids, category_ids, author_ids, **article_data):
        article = get_article(url_slug, httpauth.current_user())

        article.delete_authors()
        article.delete_categories()
        article.delete_tags()

        article_data['url_slug'] = validate_slug(Article, article_data['title'], article.id)
        validate_cover_img_style(article_data['cover_img_style'])
        validate_authors(author_ids, article)
        validate_categories(category_ids, article)
        validate_tags(tag_ids, article)

        for field in article_data:
            setattr(article, field, article_data[field])
        db.session.commit()
        return article

    @httpauth.login_required()
    @bp.response(200)
    def delete(self, url_slug):
        article = get_article(url_slug, httpauth.current_user())
        article.delete_authors()
        article.delete_categories()
        article.delete_tags()
        article.delete_comments()
        db.session.delete(article)
        db.session.commit()
