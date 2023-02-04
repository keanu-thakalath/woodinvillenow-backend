from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from datetime import timedelta, datetime
import json
from app import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(32))
    email = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_auth_token(self, expires_in=timedelta(days=1).total_seconds()):
        return jwt.encode(
            {'id': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_auth_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['id']
        except Exception as e:
            return None
        return User.query.get(id)

    def __repr__(self):
        return f'<User {self.username}>'

class Author(db.Model):
    with open('app/model-config.json') as f:
        groups = json.load(f)['groups']

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    url_slug = db.Column(db.String(32))
    title = db.Column(db.String(64))
    group = db.Column(db.String(32))
    bio = db.Column(db.String(1024))
    profile_pic = db.Column(db.String(256))
    bio_pic = db.Column(db.String(256))
    active = db.Column(db.Boolean())
    articles = db.relationship('ArticleAuthorAssociation', backref='author', lazy='dynamic')

    def delete_articles(self):
        for article in self.articles:
            db.session.delete(article)

    def __repr__(self):
        return f'<Author {self.name}>'

class Article(db.Model):
    with open('app/model-config.json') as f:
        cover_img_styles = json.load(f)['coverImgStyles']

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(512))
    excerpt = db.Column(db.String(512))
    cover_img = db.Column(db.String(256))
    cover_img_caption = db.Column(db.String(512))
    cover_img_style = db.Column(db.String(32))
    content = db.Column(db.Text())
    draft = db.Column(db.Boolean())
    url_slug = db.Column(db.String(512))
    datetime = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    views = db.Column(db.Integer(), default=lambda: 0)
    authors = db.relationship('ArticleAuthorAssociation', backref='article', lazy='dynamic')
    comments = db.relationship('Comment', backref='article', lazy='dynamic')
    categories = db.relationship('CategoryArticleAssociation', backref='article', lazy='dynamic')
    tags = db.relationship('TagArticleAssociation', backref='article', lazy='dynamic')

    def delete_authors(self):
        for author in self.authors:
            db.session.delete(author)
    
    def delete_categories(self):
        for category in self.categories:
            db.session.delete(category)

    def delete_tags(self):
        for tag in self.tags:
            db.session.delete(tag)

    def delete_comments(self):
        for comment in self.comments:
            db.session.delete(comment)

    def __repr__(self):
        return f'<Article {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    datetime = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    content = db.Column(db.String(1024))
    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'))

    def __repr__(self):
        return f'<Comment {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    url_slug = db.Column(db.String(32))
    articles = db.relationship('CategoryArticleAssociation', backref='category', lazy='dynamic')

    def delete_articles(self):
        for article in self.articles:
            db.session.delete(article)

    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    url_slug = db.Column(db.String(32))
    articles = db.relationship('TagArticleAssociation', backref='tag', lazy='dynamic')

    def delete_articles(self):
        for article in self.articles:
            db.session.delete(article)

    def __repr__(self):
        return f'<Tag {self.name}>'

class NewsletterEmail(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(128))
    datetime = db.Column(db.DateTime(), default=datetime.utcnow)

    def get_auth_token(self):
        return jwt.encode(
            {'id': self.id},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_auth_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['id']
        except Exception as e:
            return None
        return NewsletterEmail.query.get(id)

    def __repr__(self):
        return f'<NewsletterEmail {self.email}>'

class ArticleAuthorAssociation(db.Model):
    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'), primary_key=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('author.id'), primary_key=True)

class CategoryArticleAssociation(db.Model):
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'), primary_key=True)
    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'), primary_key=True)

class TagArticleAssociation(db.Model):
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'), primary_key=True)
    article_id = db.Column(db.Integer(), db.ForeignKey('article.id'), primary_key=True)