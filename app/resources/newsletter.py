from flask.views import MethodView
from flask_smorest import abort
from app.models import NewsletterEmail
from app.schemas import NewsletterEmailSchema, AuthTokenSchema
from app.resources import newsletter_bp as bp
from app import db

def get_newsletter_email(auth_token):
    email = NewsletterEmail.verify_auth_token(auth_token)
    if not email:
        abort(404, message='The email is not on our list or the token is invalid.')
    return email

@bp.route('/newsletter')
class NewsletterListView(MethodView):
    @bp.arguments(NewsletterEmailSchema)
    @bp.response(201, NewsletterEmailSchema)
    def post(self, email_data):
        email = email_data['email']
        if len(email) == 0:
            abort(400, message='Email cannot be empty.')
        
        if NewsletterEmail.query.filter_by(email=email).first():
            abort(400, message='This email is already on the mailing list.')
        email = NewsletterEmail(**email_data)
        db.session.add(email)
        db.session.commit()
        return email

@bp.route('/newsletteremail')
class NewsletterEmailView(MethodView):
    @bp.arguments(AuthTokenSchema, location='query')
    @bp.response(200, NewsletterEmailSchema)
    def get(self, token):
        return get_newsletter_email(**token)
    
    @bp.arguments(AuthTokenSchema)
    @bp.response(200)
    def delete(self, token):
        email = get_newsletter_email(**token)
        db.session.delete(email)
        db.session.commit()
