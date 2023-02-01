from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from flask_cors import CORS
from config import Config
import logging
from logging.handlers import SMTPHandler
from app.http_token_auth import HTTPTokenAuth

httpauth = HTTPTokenAuth('Bearer')
db = SQLAlchemy()
migrate = Migrate()
api = Api()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    cors.init_app(app)

    from app.auth import bp as auth_bp
    api.register_blueprint(auth_bp)

    from app.resources import author_bp, article_bp, comment_bp, category_bp, tag_bp, newsletter_bp, analytics_bp
    api.register_blueprint(author_bp)
    api.register_blueprint(article_bp)
    api.register_blueprint(comment_bp)
    api.register_blueprint(category_bp)
    api.register_blueprint(tag_bp)
    api.register_blueprint(newsletter_bp)
    api.register_blueprint(analytics_bp)

    if not app.debug and not app.testing and app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Application Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    return app

from app import models