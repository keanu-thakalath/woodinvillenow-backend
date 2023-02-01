from flask import g
from flask_httpauth import HTTPTokenAuth as extHTTPTokenAuth
from marshmallow import fields, Schema
from functools import wraps
from copy import deepcopy
import http


class BearerSchema(Schema):
    Authorization = fields.String()

class HTTPTokenAuth(extHTTPTokenAuth):
    def login_required(self, optional=False):
        def decorator(func):
            if optional:
                @wraps(func)
                def decorated(*args, **kwargs):
                    auth = self.get_auth()
                    user = self.authenticate(auth, None)
                    g.flask_httpauth_user = user
                    return func(*args, **kwargs)
            else:
                decorated = super(extHTTPTokenAuth, self).login_required(func)

            decorated._apidoc = deepcopy(getattr(decorated, '_apidoc', {}))
            arg_docs = decorated._apidoc.setdefault('arguments', {})
            arg_docs.setdefault('parameters', [])
            arg_docs.setdefault('responses', {})[401] = http.HTTPStatus(401).name
            arg_docs.setdefault('security', [{'bearerAuth': []}])
            
            return decorated
        return decorator
