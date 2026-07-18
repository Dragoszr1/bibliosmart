import jwt
import datetime
from flask import current_app

def create_jwt_token(user_id, username, email):
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def set_jwt_cookie(response, token):
    response.set_cookie(
        current_app.config['JWT_COOKIE_NAME'],
        token,
        httponly=True,
        secure=current_app.config['JWT_COOKIE_SECURE'],
        samesite=current_app.config['JWT_COOKIE_SAMESITE'],
        max_age=int(current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()),
        path='/'
    )
    return response

def clear_jwt_cookie(response):
    response.set_cookie(
        current_app.config['JWT_COOKIE_NAME'],
        '',
        httponly=True,
        secure=current_app.config['JWT_COOKIE_SECURE'],
        samesite=current_app.config['JWT_COOKIE_SAMESITE'],
        max_age=0,
        path='/'
    )
    return response

def decode_jwt_token(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
