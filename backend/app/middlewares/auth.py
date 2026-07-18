from functools import wraps
from flask import request, jsonify, g, current_app
from sqlalchemy import text
from app.database import db
from app.utils.auth import decode_jwt_token
from app.utils.validators import normalize_role
from app.utils.constants import VALID_ROLES

def fetch_user_by_id(user_id):
    query = text(
        "SELECT user_id, username, email, rol, club FROM users WHERE user_id = :user_id"
    )
    result = db.session.execute(query, {'user_id': user_id}).mappings().first()
    if not result:
        return None

    return {
        'user_id': result['user_id'],
        'username': result['username'],
        'email': result['email'],
        'rol': normalize_role(result['rol']),
        'club': bool(result['club'])
    }

def get_current_user():
    """Rezolvă utilizatorul autentificat din cookie-ul JWT și baza de date.
    Cachează rezultatul pe flask.g ca să nu se mai facă query la DB
    pentru apeluri repetate în aceeași cerere.
    """
    if hasattr(g, '_current_user'):
        return g._current_user

    token = request.cookies.get(current_app.config['JWT_COOKIE_NAME'])
    if not token:
        g._current_user = None
        return None

    payload = decode_jwt_token(token)
    if not payload:
        g._current_user = None
        return None

    try:
        user_id = int(payload.get('user_id'))
    except (TypeError, ValueError):
        g._current_user = None
        return None

    g._current_user = fetch_user_by_id(user_id)
    return g._current_user

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'message': 'Autentificare necesară'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated

def role_required(role):
    if role not in VALID_ROLES:
        raise ValueError(f"Rol necunoscut: {role}")

    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            if request.current_user.get('rol') != role:
                return jsonify({'success': False, 'message': f'Necesită rol de {role}'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

bibliotecar_required = role_required('bibliotecar')

def club_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'message': 'Autentificare necesară'}), 401
        request.current_user = user
        if not user.get('club') and user.get('rol') != 'bibliotecar':
            return jsonify({'success': False, 'message': 'Acces restricționat clubului'}), 403
        return f(*args, **kwargs)
    return decorated
