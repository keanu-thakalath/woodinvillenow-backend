from flask.views import MethodView
from flask_smorest import abort
from app.models import Comment
from app.schemas import CommentSchema
from app.resources import comment_bp as bp
from app.resources.article import get_article
from app import httpauth, db

def get_comment(url_slug, id, user):
    article = get_article(url_slug, user)
    comment = Comment.query.get(id)
    if not comment or article.id != comment.article_id:
        abort(404, message='Comment does not exist.')
    return comment

@bp.route('/articles/<url_slug>/comments')
class CommentsView(MethodView):
    @httpauth.login_required(optional=True)
    @bp.response(200, CommentSchema(many=True))
    def get(self, url_slug):
        '''
        Returns comments on an article.

        Authentication optional.
        '''
        article = get_article(url_slug, httpauth.current_user())

        return article.comments.order_by(Comment.datetime.desc()).all()

    @bp.arguments(CommentSchema)
    @bp.response(201, CommentSchema)
    def post(self, comment_data, url_slug):
        article = get_article(url_slug)

        if len(comment_data['name']) == 0:
            abort(400, message='Name cannot be empty.')

        if len(comment_data['content']) == 0:
            abort(400, message='Content cannot be empty.')

        comment = Comment(**comment_data, article_id=article.id)
        db.session.add(comment)
        db.session.commit()
        return comment

@bp.route('/articles/<url_slug>/comments/<id>')
class CommentView(MethodView):
    @httpauth.login_required()
    @bp.response(200)
    def delete(self, url_slug, id):
        comment = get_comment(url_slug, id, httpauth.current_user())
        db.session.delete(comment)
        db.session.commit()
