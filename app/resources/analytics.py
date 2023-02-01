from flask.views import MethodView
from app.schemas import AnalyticsSchema
from app.resources import analytics_bp as bp
from app.resources.article import get_article
from app import db

@bp.route('/analytics')
class AnalyticsView(MethodView):
    @bp.arguments(AnalyticsSchema)
    @bp.response(201)
    def post(self, request_data):
        article = get_article(request_data['article'])
        if request_data.get('views'):
            article.views += 1
        db.session.commit()