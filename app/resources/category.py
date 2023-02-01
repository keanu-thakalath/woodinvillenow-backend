from flask.views import MethodView
from flask_smorest import abort
from app.models import Category
from app.schemas import CategorySchema
from app.resources import category_bp as bp
from app.resources.utils import validate_slug
from app import httpauth, db

def get_category(url_slug):
    category = Category.query.filter_by(url_slug=url_slug).first()
    if not category:
        abort(404, message='Category does not exist.')
    return category

@bp.route('/categories')
class CategoriesView(MethodView):
    @bp.response(200, CategorySchema(many=True))
    def get(self):
        '''
        Returns all categories
        '''
        return Category.query.all()

    @httpauth.login_required()
    @bp.arguments(CategorySchema)
    @bp.response(201, CategorySchema)
    def post(self, category_data):
        url_slug = validate_slug(Category, category_data['name'])
        category = Category(**category_data, url_slug=url_slug)
        db.session.add(category)
        db.session.commit()
        return category

@bp.route('/categories/<url_slug>')
class CategoryView(MethodView):
    @bp.response(200, CategorySchema)
    def get(self, url_slug):
        return get_category(url_slug)
    
    @httpauth.login_required()
    @bp.response(200)
    @bp.arguments(CategorySchema)
    @bp.response(200, CategorySchema)
    def put(self, category_data, url_slug):
        category = get_category(url_slug)
        category_data['url_slug'] = validate_slug(Category, category_data['name'], category.id)
        for field in category_data:
            setattr(category, field, category_data[field])
        db.session.commit()
        return category

    @httpauth.login_required()
    @bp.response(200)
    def delete(self, url_slug):
        category = get_category(url_slug)
        category.delete_articles()
        db.session.delete(category)
        db.session.commit()
