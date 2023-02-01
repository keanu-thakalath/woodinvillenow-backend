from flask.views import MethodView
from flask_smorest import abort
from app.models import Tag
from app.schemas import TagSchema
from app.resources import tag_bp as bp
from app.resources.utils import validate_slug
from app import httpauth, db

def get_tag(url_slug):
    tag = Tag.query.filter_by(url_slug=url_slug).first()
    if not tag:
        abort(404, message='Tag does not exist.')
    return tag

@bp.route('/tags')
class TagsView(MethodView):
    @bp.response(200, TagSchema(many=True))
    def get(self):
        '''
        Returns all tags
        '''
        return Tag.query.all()

    @httpauth.login_required()
    @bp.arguments(TagSchema)
    @bp.response(201, TagSchema)
    def post(self, tag_data):
        url_slug = validate_slug(Tag, tag_data['name'])
        tag = Tag(**tag_data, url_slug=url_slug)
        db.session.add(tag)
        db.session.commit()
        return tag

@bp.route('/tags/<url_slug>')
class TagView(MethodView):
    @bp.response(200, TagSchema)
    def get(self, url_slug):
        return get_tag(url_slug)
    
    @httpauth.login_required()
    @bp.response(200)
    @bp.arguments(TagSchema)
    @bp.response(200, TagSchema)
    def put(self, tag_data, url_slug):
        tag = get_tag(url_slug)
        tag_data['url_slug'] = validate_slug(Tag, tag_data['name'], tag.id)
        for field in tag_data:
            setattr(tag, field, tag_data[field])
        db.session.commit()
        return tag

    @httpauth.login_required()
    @bp.response(200)
    def delete(self, url_slug):
        tag = get_tag(url_slug)
        tag.delete_articles()
        db.session.delete(tag)
        db.session.commit()
