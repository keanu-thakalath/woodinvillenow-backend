from flask_smorest import Blueprint

bp = Blueprint('auth', 'auth', url_prefix='/api')

from app.auth import routes, auth