from app import httpauth
from app.models import User

@httpauth.verify_token
def verify_token(token):
    return User.verify_auth_token(token)
