from flask import Blueprint, jsonify, request, send_from_directory, current_app, g
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from functools import wraps
import bcrypt
import jwt
import datetime
import os
import logging
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.database import db
from app.models import Carti, Users, CartiCitite, Recenzii, Anunturi, AnunturiAprecieri, CereriCarti

main_bp = Blueprint('main', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = frozenset({'png', 'jpg', 'jpeg', 'gif', 'webp'})
ALLOWED_EMAIL_DOMAIN = 'cni-sv.ro'
VALID_ROLES = frozenset({'user', 'bibliotecar'})
ALLOWED_BOOK_FIELDS = frozenset({'titlu', 'autor', 'ISBN', 'stoc_total', 'stoc_disponibil', 'gen'})
ALLOWED_ANUNT_FIELDS = frozenset({'titlu', 'anunt'})

logger = logging.getLogger(__name__)
ROLE_ALIASES = {
    '1': 'bibliotecar',
    'administrator': 'bibliotecar',
    'admin': 'bibliotecar',
    'bibliotecar': 'bibliotecar',
    'user': 'user'
}
EMAIL_REGEX = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._%+\-]{0,62}[A-Za-z0-9])?@([A-Za-z0-9\-]+\.)+[A-Za-z]{2,63}$")
PROFILE_PICTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'profile_pictures')
BOOK_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'book_images')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _find_files_by_prefix(directory, prefix):
    """Safely find files in directory matching prefix.<allowed_ext>.
    Uses os.listdir instead of glob to avoid glob injection from
    user-controlled strings containing *, ?, or [] characters.
    """
    os.makedirs(directory, exist_ok=True)
    matches = []
    for entry in os.listdir(directory):
        if not entry.startswith(prefix + '.'):
            continue
        ext = entry.rsplit('.', 1)[1].lower() if '.' in entry else ''
        if ext in ALLOWED_EXTENSIONS:
            matches.append(entry)
    return matches


# ── Email Helper ─────────────────────────────────────────────

def send_email(recipients, subject, html_body):
    """Send an email via SMTP (Gmail).

    Reads SMTP_* settings from the current Flask app config.
    Returns True on success, False on failure (logged, never raises).
    """
    cfg = current_app.config
    host = cfg.get('SMTP_HOST', 'smtp.gmail.com')
    port = cfg.get('SMTP_PORT', 587)
    user = cfg.get('SMTP_USER', '')
    password = cfg.get('SMTP_PASSWORD', '')
    sender = cfg.get('SMTP_FROM', '') or user

    if not user or not password:
        logger.error('SMTP credentials not configured — email not sent')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.sendmail(sender, recipients, msg.as_string())
        logger.info('Email sent to %s', recipients)
        return True
    except Exception:
        logger.exception('Failed to send email')
        return False


# ── JWT Helpers ──────────────────────────────────────────────

def normalize_role(raw_role):
    """Normalize legacy role values to the supported set."""
    if raw_role is None:
        return 'user'

    normalized_role = ROLE_ALIASES.get(str(raw_role).strip().lower())
    return normalized_role if normalized_role in VALID_ROLES else 'user'


def normalize_cni_email(email):
    """Return a normalized school email address or None if invalid."""
    if not isinstance(email, str):
        return None

    normalized_email = email.strip().lower()
    if not normalized_email or len(normalized_email) > 254:
        return None

    if not EMAIL_REGEX.fullmatch(normalized_email):
        return None

    local_part, _, domain = normalized_email.rpartition('@')
    if not local_part or '..' in local_part or domain != ALLOWED_EMAIL_DOMAIN:
        return None

    return normalized_email


def fetch_user_by_id(user_id):
    """Load the current user from the database for authorization decisions."""
    query = text(
        "SELECT user_id, username, email, rol FROM users WHERE user_id = :user_id"
    )
    result = db.session.execute(query, {'user_id': user_id}).mappings().first()
    if not result:
        return None

    return {
        'user_id': result['user_id'],
        'username': result['username'],
        'email': result['email'],
        'rol': normalize_role(result['rol'])
    }


def create_jwt_token(user_id, username, email):
    """Create a JWT token with identity claims only."""
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def set_jwt_cookie(response, token):
    """Set the JWT token as an httpOnly cookie on the response."""
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
    """Clear the JWT cookie."""
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
    """Decode and verify a JWT token. Returns payload or None."""
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def get_current_user():
    """Resolve the authenticated user from the JWT cookie and database.
    Caches the result on flask.g so repeated calls in the same request
    don't hit the database again.
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
    """Decorator that enforces a valid JWT cookie."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """Decorator factory that enforces a specific role from the database."""
    if role not in VALID_ROLES:
        raise ValueError(f"Unknown role: {role}")

    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated(*args, **kwargs):
            if request.current_user.get('rol') != role:
                return jsonify({'success': False, 'message': f'{role.capitalize()} privileges required'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator


bibliotecar_required = role_required('bibliotecar')

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

@main_bp.route('/', methods=['GET'])
def index():
    """API index"""
    return jsonify({
        'name': 'School Library API',
        'version': '1.0.0',
        'message': 'Database connection established'
    }), 200

# Basic routing structure - queries to be implemented by user
@main_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books from the carti table"""
    try:
        result = db.session.execute(text('SELECT carte_id, titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen FROM carti'))
        books = []
        for row in result:
            books.append({
                'carte_id': row[0],
                'titlu': row[1],
                'autor': row[2],
                'ISBN': row[3],
                'stoc_total': row[4],
                'stoc_disponibil': row[5],
                'imprumutat': row[6],
                'gen': row[7]
            })
        return jsonify({'books': books}), 200
    except Exception:
        logger.exception('Failed to fetch books')
        return jsonify({'error': 'Failed to fetch books'}), 500


@main_bp.route('/books', methods=['POST'])
@bibliotecar_required
def add_book():
    """Add a new book to the collection. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu')
    autor = data.get('autor')
    isbn = data.get('ISBN')
    stoc_total = data.get('stoc_total', 1)
    stoc_disponibil = data.get('stoc_disponibil', stoc_total)
    gen = data.get('gen')

    if not titlu or not autor or not isbn or not gen:
        return jsonify({'success': False, 'message': 'titlu, autor, ISBN, and gen are required'}), 400

    insert_query = text(
        "INSERT INTO carti (titlu, autor, ISBN, stoc_total, stoc_disponibil, imprumutat, gen) "
        "VALUES (:titlu, :autor, :ISBN, :stoc_total, :stoc_disponibil, :imprumutat, :gen)"
    )
    try:
        db.session.execute(insert_query, {
            'titlu': titlu,
            'autor': autor,
            'ISBN': isbn,
            'stoc_total': stoc_total,
            'stoc_disponibil': stoc_disponibil,
            'imprumutat': stoc_disponibil < stoc_total,
            'gen': gen
        })
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'A book with this ISBN already exists'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to add book'}), 500

    return jsonify({'success': True, 'message': 'Book added successfully'}), 201


@main_bp.route('/books/<int:carte_id>', methods=['PUT'])
@bibliotecar_required
def update_book(carte_id):
    """Update a book's stock or details. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}

    # Build dynamic update
    fields = {}
    for key in ALLOWED_BOOK_FIELDS:
        if key in data:
            fields[key] = data[key]

    if not fields:
        return jsonify({'success': False, 'message': 'No fields to update'}), 400

    set_clause = ', '.join(f"{k} = :{k}" for k in fields)
    fields['carte_id'] = carte_id

    # Auto-update imprumutat flag if stock fields are changing
    if 'stoc_total' in fields or 'stoc_disponibil' in fields:
        set_clause += ', imprumutat = (stoc_disponibil < stoc_total)'

    update_query = text(f"UPDATE carti SET {set_clause} WHERE carte_id = :carte_id")
    try:
        result = db.session.execute(update_query, fields)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Book not found'}), 404
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'ISBN conflict'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update book'}), 500

    return jsonify({'success': True, 'message': 'Book updated successfully'}), 200


@main_bp.route('/books/<int:carte_id>', methods=['DELETE'])
@bibliotecar_required
def delete_book(carte_id):
    """Delete a book from the collection. Requires bibliotecar role."""
    try:
        # Delete related records first
        db.session.execute(text("DELETE FROM recenzii WHERE carte_id = :id"), {'id': carte_id})
        db.session.execute(text("DELETE FROM carti_citite WHERE carte_id = :id"), {'id': carte_id})
        result = db.session.execute(text("DELETE FROM carti WHERE carte_id = :id"), {'id': carte_id})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Book not found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to delete book'}), 500

    return jsonify({'success': True, 'message': 'Book deleted successfully'}), 200


@main_bp.route('/books/<int:carte_id>/request-fizic', methods=['POST'])
@jwt_required
def request_book_fizic(carte_id):
    """Request a physical copy of a book.

    Sends an email to every user with the 'bibliotecar' role
    informing them that this user wants to pick up the book.
    """
    user = request.current_user

    # Look up the book
    book_row = db.session.execute(
        text("SELECT titlu, autor, stoc_disponibil FROM carti WHERE carte_id = :id"),
        {'id': carte_id}
    ).fetchone()

    if not book_row:
        return jsonify({'success': False, 'message': 'Book not found'}), 404

    titlu, autor, stoc_disponibil = book_row
    if stoc_disponibil <= 0:
        return jsonify({'success': False, 'message': 'Book is not available'}), 409

    # Fetch all librarian emails
    rows = db.session.execute(
        text("SELECT email FROM users WHERE rol = 'bibliotecar'")
    ).fetchall()
    librarian_emails = [r[0] for r in rows if r[0]]

    if not librarian_emails:
        logger.warning('No librarians found to notify for book request %d', carte_id)
        return jsonify({'success': False, 'message': 'No librarians available to process your request'}), 503

    subject = f'Cerere împrumut carte — {titlu}'
    html_body = (
        f'<h2>Cerere nouă de împrumut</h2>'
        f'<p>Utilizatorul <strong>{user["username"]}</strong> '
        f'(<a href="mailto:{user["email"]}">{user["email"]}</a>) '
        f'dorește să împrumute cartea:</p>'
        f'<ul>'
        f'<li><strong>Titlu:</strong> {titlu}</li>'
        f'<li><strong>Autor:</strong> {autor}</li>'
        f'<li><strong>ID carte:</strong> {carte_id}</li>'
        f'</ul>'
        f'<p>Stoc disponibil: {stoc_disponibil}</p>'
    )

    # Save the request in the database
    try:
        db.session.execute(
            text("INSERT INTO cereri_carti (user_id, carte_id) VALUES (:uid, :cid)"),
            {'uid': user['user_id'], 'cid': carte_id}
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception('Failed to save book request to DB')
        return jsonify({'success': False, 'message': 'Failed to save request'}), 500

    # Send email notification (best-effort, don't fail the request if email fails)
    send_email(librarian_emails, subject, html_body)

    return jsonify({'success': True, 'message': 'Cererea a fost trimisă!'}), 200


@main_bp.route('/book-requests', methods=['GET'])
@bibliotecar_required
def get_book_requests():
    """List all book borrow requests. Librarians only."""
    status_filter = request.args.get('status')  # optional: pending, approved, rejected
    try:
        sql = (
            "SELECT c.cerere_id, c.user_id, c.carte_id, c.status, c.created_at, "
            "u.username, u.email, ca.titlu, ca.autor "
            "FROM cereri_carti c "
            "JOIN users u ON c.user_id = u.user_id "
            "JOIN carti ca ON c.carte_id = ca.carte_id "
        )
        params = {}
        if status_filter in ('pending', 'approved', 'rejected'):
            sql += "WHERE c.status = :status "
            params['status'] = status_filter
        sql += "ORDER BY c.created_at DESC"

        rows = db.session.execute(text(sql), params).fetchall()
        cereri = []
        for r in rows:
            cereri.append({
                'cerere_id': r[0],
                'user_id': r[1],
                'carte_id': r[2],
                'status': r[3],
                'created_at': r[4].isoformat() if r[4] else None,
                'username': r[5],
                'email': r[6],
                'titlu': r[7],
                'autor': r[8]
            })
        return jsonify({'success': True, 'cereri': cereri}), 200
    except Exception:
        logger.exception('Failed to fetch book requests')
        return jsonify({'success': False, 'error': 'Failed to fetch requests'}), 500


@main_bp.route('/book-requests/<int:cerere_id>', methods=['PUT'])
@bibliotecar_required
def update_book_request(cerere_id):
    """Approve or reject a book request. Librarians only."""
    data = request.get_json(silent=True) or {}
    new_status = data.get('status')
    if new_status not in ('approved', 'rejected'):
        return jsonify({'success': False, 'message': 'Status must be approved or rejected'}), 400

    try:
        result = db.session.execute(
            text("UPDATE cereri_carti SET status = :status WHERE cerere_id = :id"),
            {'status': new_status, 'id': cerere_id}
        )
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Request not found'}), 404
        return jsonify({'success': True, 'message': f'Request {new_status}'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to update book request %d', cerere_id)
        return jsonify({'success': False, 'message': 'Failed to update request'}), 500


@main_bp.route('/users', methods=['GET'])
def get_users():
    """Basic users route - implement your queries here"""
    return jsonify({'message': 'Users endpoint - implement your database queries here'}), 200

@main_bp.route('/books-read', methods=['GET'])
def get_books_read():
    """Basic books read route - implement your queries here"""
    return jsonify({'message': 'Books read endpoint - implement your database queries here'}), 200

@main_bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Get reviews for a specific book by carte_id.
    Returns reviews with username, nota (rating), and comentariu.
    """
    carte_id = request.args.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id is required'}), 400

    try:
        query = text("""
            SELECT r.id, r.nota, r.comentariu, u.username
            FROM recenzii r
            JOIN users u ON r.user_id = u.user_id
            WHERE r.carte_id = :carte_id
            ORDER BY r.id DESC
        """)
        result = db.session.execute(query, {'carte_id': carte_id})
        reviews = []
        for row in result:
            reviews.append({
                'id': row[0],
                'nota': row[1],
                'comentariu': row[2],
                'username': row[3]
            })

        # Calculate average rating
        avg_rating = 0
        if reviews:
            avg_rating = round(sum(r['nota'] for r in reviews) / len(reviews), 1)

        return jsonify({
            'success': True,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'total_reviews': len(reviews)
        }), 200
    except Exception:
        logger.exception('Failed to fetch reviews')
        return jsonify({'success': False, 'error': 'Failed to fetch reviews'}), 500


@main_bp.route('/reviews/user', methods=['GET'])
def get_user_reviews():
    """Get all reviews by a specific user.
    Returns reviews with book title, author, nota, and comentariu.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'user_id is required'}), 400

    try:
        query = text("""
            SELECT r.id, r.nota, r.comentariu, c.titlu, c.autor
            FROM recenzii r
            JOIN carti c ON r.carte_id = c.carte_id
            WHERE r.user_id = :user_id
            ORDER BY r.id DESC
        """)
        result = db.session.execute(query, {'user_id': user_id})
        reviews = []
        for row in result:
            reviews.append({
                'id': row[0],
                'nota': row[1],
                'comentariu': row[2],
                'titlu': row[3],
                'autor': row[4]
            })

        return jsonify({
            'success': True,
            'reviews': reviews,
            'total_reviews': len(reviews)
        }), 200
    except Exception:
        logger.exception('Failed to fetch user reviews')
        return jsonify({'success': False, 'error': 'Failed to fetch reviews'}), 500


# Authentication routes structure
@main_bp.route('/auth/login', methods=['POST'])
def login():
    """Login route with bcrypt password verification. Sets JWT httpOnly cookie."""
    data = request.get_json(silent=True) or {}
    raw_email = data.get('email')
    password = data.get('password')

    if not raw_email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    query = text(
        "SELECT user_id, username, email, hashed_password, rol FROM users WHERE email = :email"
    )
    result = db.session.execute(query, {'email': email}).mappings().first()

    if not result:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    hashed_password = result.get('hashed_password')
    if not hashed_password or not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    token = create_jwt_token(
        user_id=result['user_id'],
        username=result['username'],
        email=result['email']
    )

    normalized_role = normalize_role(result['rol'])

    resp = jsonify({
        'success': True,
        'message': 'Login successful',
        'user': {
            'user_id': result['user_id'],
            'username': result['username'],
            'email': result['email'],
            'rol': normalized_role
        }
    })
    set_jwt_cookie(resp, token)
    return resp, 200

@main_bp.route('/auth/me', methods=['GET'])
@jwt_required
def auth_me():
    """Return the currently authenticated user from the JWT cookie."""
    user = request.current_user
    return jsonify({
        'success': True,
        'user_id': user['user_id'],
        'username': user['username'],
        'email': user['email'],
        'rol': user['rol']
    }), 200


@main_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Clear the JWT cookie."""
    resp = jsonify({'success': True, 'message': 'Logged out'})
    clear_jwt_cookie(resp)
    return resp, 200


@main_bp.route('/auth/profile', methods=['GET'])
@jwt_required
def profile():
    """Fetch profile information from the JWT session."""
    user = request.current_user

    query = text(
        "SELECT user_id, username, email, description FROM users WHERE user_id = :user_id"
    )
    result = db.session.execute(query, {'user_id': user['user_id']}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Profile not found'}), 404

    return jsonify({
        'success': True,
        'user_id': result.get('user_id'),
        'username': result.get('username'),
        'email': result.get('email'),
        'description': result.get('description')
    }), 200

@main_bp.route('/auth/books-read', methods=['GET'])
@jwt_required
def books_read():
    """Fetch books read by the authenticated user."""
    user = request.current_user
    user_id = user['user_id']

    query = text(
        "SELECT c.carte_id, c.titlu, c.autor, c.ISBN "
        "FROM carti_citite cc "
        "JOIN carti c ON cc.carte_id = c.carte_id "
        "WHERE cc.user_id = :user_id"
    )
    rows = db.session.execute(query, {'user_id': user_id}).mappings().all()

    books = []
    for row in rows:
        books.append({
            'carte_id': row.get('carte_id'),
            'titlu': row.get('titlu'),
            'autor': row.get('autor'),
            'ISBN': row.get('ISBN')
        })

    return jsonify({'success': True, 'books': books}), 200

@main_bp.route('/auth/profile', methods=['PUT'])
@jwt_required
def update_profile():
    """Update user description for the authenticated user."""
    user = request.current_user
    data = request.get_json(silent=True) or {}
    description = data.get('description')

    update_query = text(
        "UPDATE users SET description = :description WHERE user_id = :user_id"
    )
    try:
        result = db.session.execute(update_query, {'description': description, 'user_id': user['user_id']})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update description'}), 500

    return jsonify({'success': True, 'message': 'Description updated'}), 200

@main_bp.route('/auth/register', methods=['POST'])
def register():
    """Registration route with bcrypt password hashing. Sets JWT cookie on success."""
    data = request.get_json(silent=True) or {}
    username = data.get('user') or data.get('username') or data.get('fullName')
    raw_email = data.get('email')
    password = data.get('password')

    if not username or not raw_email or not password:
        return jsonify({'success': False, 'message': 'User, email, and password are required'}), 400

    email = normalize_cni_email(raw_email)
    if not email:
        return jsonify({'success': False, 'message': 'Doar emailurile @cni-sv.ro sunt permise'}), 400

    if len(password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    values = {
        'username': username,
        'email': email,
        'hashed_password': hashed_password,
        'rol': 'user',
        'telefon': None
    }

    insert_query = text(
        "INSERT INTO users (username, email, hashed_password, rol, telefon) VALUES (:username, :email, :hashed_password, :rol, :telefon)"
    )

    try:
        db.session.execute(insert_query, values)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'User or email already exists'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

    # Fetch the new user_id so we can issue a token
    query = text("SELECT user_id FROM users WHERE email = :email")
    new_user = db.session.execute(query, {'email': email}).mappings().first()
    token = create_jwt_token(
        user_id=new_user['user_id'],
        username=username,
        email=email
    )

    resp = jsonify({'success': True, 'message': 'Registration successful'})
    set_jwt_cookie(resp, token)
    return resp, 201


@main_bp.route('/auth/profile-picture', methods=['POST'])
@jwt_required
def upload_profile_picture():
    """Upload or replace a user's profile picture.
    Expects multipart/form-data with 'file' field. User determined from JWT.
    """
    user = request.current_user

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed. Use png, jpg, jpeg, gif, or webp'}), 400

    username = user['username']
    ext = file.filename.rsplit('.', 1)[1].lower()

    # Remove any existing profile picture for this user
    for old_file in _find_files_by_prefix(PROFILE_PICTURES_DIR, username):
        os.remove(os.path.join(PROFILE_PICTURES_DIR, old_file))

    # Save the new file as username.ext
    filename = f"{username}.{ext}"
    filepath = os.path.join(PROFILE_PICTURES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Profile picture uploaded',
        'filename': filename
    }), 200


@main_bp.route('/auth/profile-picture/<username>', methods=['GET'])
def get_profile_picture(username):
    """Serve a user's profile picture by username.
    Looks for <username>.* in the profile_pictures folder.
    """
    matches = _find_files_by_prefix(PROFILE_PICTURES_DIR, username)

    if not matches:
        return jsonify({'success': False, 'message': 'No profile picture found'}), 404

    return send_from_directory(PROFILE_PICTURES_DIR, matches[0])


@main_bp.route('/books/image', methods=['POST'])
@bibliotecar_required
def upload_book_image():
    """Upload or replace a book cover image.
    Expects multipart/form-data with 'file' and 'carte_id' fields.
    Saves as <carte_id>.<ext> in the book_images folder.
    """
    carte_id = request.form.get('carte_id')
    if not carte_id:
        return jsonify({'success': False, 'message': 'carte_id is required'}), 400

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed. Use png, jpg, jpeg, gif, or webp'}), 400

    # Verify the book exists
    query = text("SELECT carte_id FROM carti WHERE carte_id = :carte_id")
    result = db.session.execute(query, {'carte_id': carte_id}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Book not found'}), 404

    ext = file.filename.rsplit('.', 1)[1].lower()

    # Remove any existing image for this book
    for old_file in _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id)):
        os.remove(os.path.join(BOOK_IMAGES_DIR, old_file))

    # Save the new file as carte_id.ext
    filename = f"{carte_id}.{ext}"
    filepath = os.path.join(BOOK_IMAGES_DIR, filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'message': 'Book image uploaded',
        'filename': filename
    }), 200


@main_bp.route('/books/image/<int:carte_id>', methods=['GET'])
def get_book_image(carte_id):
    """Serve a book's cover image by carte_id.
    Looks for <carte_id>.* in the book_images folder.
    """
    matches = _find_files_by_prefix(BOOK_IMAGES_DIR, str(carte_id))

    if not matches:
        return jsonify({'success': False, 'message': 'No book image found'}), 404

    return send_from_directory(BOOK_IMAGES_DIR, matches[0])


# ── Announcement Routes ──────────────────────────────────────

@main_bp.route('/anunturi', methods=['GET'])
def get_anunturi():
    """Get all announcements, newest first. Includes whether current user liked each."""
    user = get_current_user()
    user_id = user['user_id'] if user else None

    try:
        query = text("""
            SELECT a.anunt_id, a.titlu, a.anunt, a.data_publicare, a.aprecieri
            FROM anunturi a
            ORDER BY a.data_publicare DESC
        """)
        rows = db.session.execute(query).fetchall()

        liked_set = set()
        if user_id:
            liked_rows = db.session.execute(
                text("SELECT anunt_id FROM anunturi_aprecieri WHERE user_id = :uid"),
                {'uid': user_id}
            ).fetchall()
            liked_set = {r[0] for r in liked_rows}

        anunturi = []
        for row in rows:
            anunturi.append({
                'anunt_id': row[0],
                'titlu': row[1],
                'anunt': row[2],
                'data_publicare': row[3].strftime('%d %B %Y, %H:%M') if row[3] else None,
                'aprecieri': row[4] or 0,
                'liked': row[0] in liked_set
            })

        return jsonify({'success': True, 'anunturi': anunturi}), 200
    except Exception:
        logger.exception('Failed to fetch announcements')
        return jsonify({'success': False, 'error': 'Failed to fetch announcements'}), 500


@main_bp.route('/anunturi', methods=['POST'])
@bibliotecar_required
def create_anunt():
    """Create a new announcement. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}
    titlu = data.get('titlu', '').strip()
    anunt = data.get('anunt', '').strip()

    if not titlu or not anunt:
        return jsonify({'success': False, 'message': 'titlu and anunt are required'}), 400

    try:
        db.session.execute(
            text("INSERT INTO anunturi (titlu, anunt, data_publicare, aprecieri) VALUES (:titlu, :anunt, NOW(), 0)"),
            {'titlu': titlu, 'anunt': anunt}
        )
        db.session.commit()
        return jsonify({'success': True, 'message': 'Announcement created'}), 201
    except Exception:
        db.session.rollback()
        logger.exception('Failed to create announcement')
        return jsonify({'success': False, 'message': 'Failed to create announcement'}), 500


@main_bp.route('/anunturi/<int:anunt_id>', methods=['PUT'])
@bibliotecar_required
def update_anunt(anunt_id):
    """Update an announcement. Requires bibliotecar role."""
    data = request.get_json(silent=True) or {}

    fields = {}
    for key in ALLOWED_ANUNT_FIELDS:
        if key in data and data[key] is not None:
            fields[key] = data[key].strip()

    if not fields:
        return jsonify({'success': False, 'message': 'No fields to update'}), 400

    set_clause = ', '.join(f"{k} = :{k}" for k in fields)
    fields['anunt_id'] = anunt_id

    try:
        result = db.session.execute(text(f"UPDATE anunturi SET {set_clause} WHERE anunt_id = :anunt_id"), fields)
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        return jsonify({'success': True, 'message': 'Announcement updated'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to update announcement %d', anunt_id)
        return jsonify({'success': False, 'message': 'Failed to update announcement'}), 500


@main_bp.route('/anunturi/<int:anunt_id>', methods=['DELETE'])
@bibliotecar_required
def delete_anunt(anunt_id):
    """Delete an announcement. Requires bibliotecar role. Cascade deletes likes."""
    try:
        result = db.session.execute(text("DELETE FROM anunturi WHERE anunt_id = :id"), {'id': anunt_id})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Announcement not found'}), 404
        return jsonify({'success': True, 'message': 'Announcement deleted'}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to delete announcement %d', anunt_id)
        return jsonify({'success': False, 'message': 'Failed to delete announcement'}), 500


@main_bp.route('/anunturi/<int:anunt_id>/like', methods=['POST'])
@jwt_required
def toggle_like_anunt(anunt_id):
    """Toggle like on an announcement. Logged-in users only."""
    user = request.current_user
    user_id = user['user_id']

    try:
        existing = db.session.execute(
            text("SELECT id FROM anunturi_aprecieri WHERE anunt_id = :aid AND user_id = :uid"),
            {'aid': anunt_id, 'uid': user_id}
        ).fetchone()

        if existing:
            db.session.execute(
                text("DELETE FROM anunturi_aprecieri WHERE anunt_id = :aid AND user_id = :uid"),
                {'aid': anunt_id, 'uid': user_id}
            )
            db.session.execute(
                text("UPDATE anunturi SET aprecieri = GREATEST(aprecieri - 1, 0) WHERE anunt_id = :aid"),
                {'aid': anunt_id}
            )
            db.session.commit()
            liked = False
        else:
            db.session.execute(
                text("INSERT INTO anunturi_aprecieri (anunt_id, user_id) VALUES (:aid, :uid)"),
                {'aid': anunt_id, 'uid': user_id}
            )
            db.session.execute(
                text("UPDATE anunturi SET aprecieri = aprecieri + 1 WHERE anunt_id = :aid"),
                {'aid': anunt_id}
            )
            db.session.commit()
            liked = True

        count = db.session.execute(
            text("SELECT aprecieri FROM anunturi WHERE anunt_id = :aid"),
            {'aid': anunt_id}
        ).fetchone()

        return jsonify({'success': True, 'liked': liked, 'aprecieri': count[0] if count else 0}), 200
    except Exception:
        db.session.rollback()
        logger.exception('Failed to toggle like on announcement %d', anunt_id)
        return jsonify({'success': False, 'message': 'Failed to toggle like'}), 500
