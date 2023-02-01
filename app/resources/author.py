from flask.views import MethodView
from flask_smorest import abort
from app.models import Author
from app.schemas import AuthorSchema, AuthorBasicSchema
from app.resources import author_bp as bp
from app.resources.utils import validate_slug
from app import httpauth, db

def get_author(url_slug):
    author = Author.query.filter_by(url_slug=url_slug).first()
    if not author:
        abort(404, message='Author does not exist.')
    return author

def validate_group(group):
    if group not in Author.groups:
        abort(400, message='Unknown group.')

@bp.route('/authors')
class AuthorsView(MethodView):
    @bp.response(200, AuthorBasicSchema(many=True))
    def get(self):
        '''
        Returns basic information about all authors.
        '''
        return Author.query.all()
    
    @httpauth.login_required()
    @bp.arguments(AuthorSchema)
    @bp.response(201, AuthorBasicSchema)
    def post(self, author_data):
        url_slug = validate_slug(Author, author_data['name'])
        validate_group(author_data['group'])
        author = Author(**author_data, url_slug=url_slug)
        db.session.add(author)
        db.session.commit()
        return author

@bp.route('/authors/<url_slug>')
class AuthorView(MethodView):
    @bp.response(200, AuthorSchema)
    def get(self, url_slug):
        '''
        Returns all information about an author.
        '''
        return get_author(url_slug)

    @httpauth.login_required()
    @bp.response(200)
    @bp.arguments(AuthorSchema)
    @bp.response(200, AuthorBasicSchema)
    def put(self, author_data, url_slug):
        author = get_author(url_slug)
        author_data['url_slug'] = validate_slug(Author, author_data['name'], author.id)
        validate_group(author_data['group'])
        for field in author_data:
            setattr(author, field, author_data[field])
        db.session.commit()
        return author

    @httpauth.login_required()
    @bp.response(200)
    def delete(self, url_slug):
        author = get_author(url_slug)
        author.delete_articles()
        db.session.delete(author)
        db.session.commit()
