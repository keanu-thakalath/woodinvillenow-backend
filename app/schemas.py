from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields
from app import db
from app.models import User, Author, Article, Comment, Category, Tag, ArticleAuthorAssociation, CategoryArticleAssociation, TagArticleAssociation, NewsletterEmail

class Schema(SQLAlchemySchema):
    def load(self, *args, **kwargs):
        return super().load(*args, **kwargs, session=db.session)

class UserSchema(Schema):
    class Meta:
        model = User
        ordered = True

    id = auto_field(required=True, dump_only=True)
    username = auto_field(required=True)
    email = auto_field(required=True, dump_only=True)
    password = fields.String(required=True, load_only=True)

class AuthTokenSchema(Schema):
    auth_token = fields.String()

class AuthorSchema(Schema):
    class Meta:
        model = Author
        ordered = True
    
    id = auto_field(required=True, dump_only=True)
    name = auto_field(required=True)
    url_slug = auto_field(required=True, dump_only=True)
    title = auto_field(required=True)
    group = auto_field(required=True)
    bio = auto_field(required=True)
    profile_pic = auto_field(required=True)
    bio_pic = auto_field(required=True)
    active = auto_field(required=True)

class AuthorBasicSchema(AuthorSchema):
    class Meta(AuthorSchema.Meta):
        exclude = ('bio_pic',)

class ArticleAuthorAssociationSchema(Schema):
    class Meta:
        model = ArticleAuthorAssociation
        ordered = True
    
    author = fields.Nested(AuthorBasicSchema, required=True, dump_only=True)

class CommentSchema(Schema):
    class Meta:
        model = Comment
        ordered = True
    
    id = auto_field(required=True, dump_only=True)
    name = auto_field(required=True)
    datetime = auto_field(required=True, dump_only=True)
    content = auto_field(required=True)

class CategorySchema(Schema):
    class Meta:
        model = Category
        ordered = True
    
    id = auto_field(required=True, dump_only=True)
    name = auto_field(required=True)
    url_slug = auto_field(required=True, dump_only=True)

class CategoryArticleAssociationSchema(Schema):
    class Meta:
        model = CategoryArticleAssociation
        ordered = True
    
    category = fields.Nested(CategorySchema, required=True, dump_only=True)

class TagSchema(Schema):
    class Meta:
        model = Tag
        ordered = True
    
    id = auto_field(required=True, dump_only=True)
    name = auto_field(required=True)
    url_slug = auto_field(required=True, dump_only=True)

class TagArticleAssociationSchema(Schema):
    class Meta:
        model = TagArticleAssociation
        ordered = True
    
    tag = fields.Nested(TagSchema, required=True, dump_only=True)

class ArticleSchema(Schema):
    class Meta:
        model = Article
        ordered = True
    
    id = auto_field(required=True, dump_only=True)
    title = auto_field(required=True)
    excerpt = auto_field(required=True)
    cover_img = auto_field(required=True)
    cover_img_caption = auto_field(required=True)
    cover_img_style = auto_field(required=True)
    content = auto_field(required=True)
    draft = auto_field(required=True)
    url_slug = auto_field(required=True, dump_only=True)
    datetime = auto_field(required=True, dump_only=True)
    views = auto_field(required=True, dump_only=True)

    author_ids = fields.List(fields.Integer, required=True, load_only=True)
    authors = fields.List(fields.Nested(ArticleAuthorAssociationSchema), required=True, dump_only=True)

    category_ids = fields.List(fields.Integer, required=True, load_only=True)
    categories = fields.List(fields.Nested(CategoryArticleAssociationSchema), required=True, dump_only=True)

    tag_ids = fields.List(fields.Integer, required=True, load_only=True)
    tags = fields.List(fields.Nested(TagArticleAssociationSchema), required=True, dump_only=True)

class ArticleBasicSchema(ArticleSchema):
    class Meta(ArticleSchema.Meta):
        exclude = ('content', 'cover_img_caption', 'cover_img_style')

    authors = fields.List(fields.Nested(ArticleAuthorAssociationSchema), required=True, dump_only=True)

class NewsletterEmailSchema(Schema):
    class Meta:
        model = NewsletterEmail
        ordered = True

    id = auto_field(required=True, dump_only=True)
    email = auto_field(required=True)
    datetime = auto_field(required=True, dump_only=True)

class AnalyticsSchema(Schema):
    class Meta:
        ordered = True

    article = fields.String(required=True)
    views = fields.Boolean(required=True)

class ArticleQueryArgsSchema(Schema):
    class Meta:
        ordered = True

    sort_by = fields.String()
    author = fields.String()
    category = fields.String()
    tag = fields.String()
    query = fields.String()
    limit = fields.Integer()
    page = fields.Integer()