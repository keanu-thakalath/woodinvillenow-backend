from flask_smorest import abort
import string

valid_characters = set(string.ascii_letters + string.digits + '-')

def make_url_safe(s):
    s = s.lower().replace(' ', '-')
    safe_string = ''
    for c in s:
        safe_string += c if c in valid_characters else ''
    return safe_string

def validate_slug(model, unsafe_url, id=None):
    url_slug = make_url_safe(unsafe_url)

    if len(url_slug) == 0:
        abort(400, message='URL slug cannot be 0 length.')
    
    conflicting_obj = model.query.filter_by(url_slug=url_slug).first()
    if conflicting_obj and conflicting_obj.id != id:
        abort(400, message='URL slug conflicts with a different object.')
    
    return url_slug
