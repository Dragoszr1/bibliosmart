from flask import Blueprint, jsonify, request, send_from_directory, current_app
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import bcrypt
import os
import glob

from app.database import db
from app.models import Carti, Users, CartiCitite, Recenzii

main_bp = Blueprint('main', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
PROFILE_PICTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'profile_pictures')
BOOK_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'book_images')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Authentication routes structure
@main_bp.route('/auth/login', methods=['POST'])
def login():
    """Login route with bcrypt password verification."""
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    # SQL query used to log in:
    # SELECT username, email, hashed_password FROM users WHERE email = :email
    query = text(
        "SELECT username, email, hashed_password FROM users WHERE email = :email"
    )
    result = db.session.execute(query, {'email': email}).mappings().first()

    if not result:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    hashed_password = result.get('hashed_password')
    if not hashed_password or not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': result.get('username'),
        'email': result.get('email')
    }), 200

@main_bp.route('/auth/profile', methods=['GET'])
def profile():
    """Fetch profile information by email."""
    email = request.args.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400

    query = text(
        "SELECT user_id, username, email, description FROM users WHERE email = :email"
    )
    result = db.session.execute(query, {'email': email}).mappings().first()
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
def books_read():
    """Fetch books read by a user.
    SQL: SELECT c.carte_id, c.titlu, c.autor, c.ISBN
         FROM carti_citite cc
         JOIN carti c ON cc.carte_id = c.carte_id
         WHERE cc.user_id = :user_id
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'user_id is required'}), 400

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
def update_profile():
    """Update user description by email."""
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    description = data.get('description')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400

    update_query = text(
        "UPDATE users SET description = :description WHERE email = :email"
    )
    try:
        result = db.session.execute(update_query, {'description': description, 'email': email})
        db.session.commit()
        if result.rowcount == 0:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update description'}), 500

    return jsonify({'success': True, 'message': 'Description updated'}), 200

@main_bp.route('/auth/register', methods=['POST'])
def register():
    """Registration route with bcrypt password hashing and SQL insert."""
    data = request.get_json(silent=True) or {}
    username = data.get('user') or data.get('username') or data.get('fullName')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'User, email, and password are required'}), 400

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

    return jsonify({'success': True, 'message': 'Registration successful'}), 201


@main_bp.route('/auth/profile-picture', methods=['POST'])
def upload_profile_picture():
    """Upload or replace a user's profile picture.
    Expects multipart/form-data with 'file' and 'email' fields.
    Saves as <username>.<ext> in the profile_pictures folder.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'File type not allowed. Use png, jpg, jpeg, gif, or webp'}), 400

    # Look up the username from the email
    query = text("SELECT username FROM users WHERE email = :email")
    result = db.session.execute(query, {'email': email}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    username = result['username']
    ext = file.filename.rsplit('.', 1)[1].lower()

    # Remove any existing profile picture for this user
    os.makedirs(PROFILE_PICTURES_DIR, exist_ok=True)
    for old_file in glob.glob(os.path.join(PROFILE_PICTURES_DIR, f"{username}.*")):
        os.remove(old_file)

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
    os.makedirs(PROFILE_PICTURES_DIR, exist_ok=True)
    matches = glob.glob(os.path.join(PROFILE_PICTURES_DIR, f"{username}.*"))

    # Filter to only allowed extensions
    matches = [m for m in matches if m.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS]

    if not matches:
        return jsonify({'success': False, 'message': 'No profile picture found'}), 404

    return send_from_directory(PROFILE_PICTURES_DIR, os.path.basename(matches[0]))


@main_bp.route('/books/image', methods=['POST'])
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
    os.makedirs(BOOK_IMAGES_DIR, exist_ok=True)
    for old_file in glob.glob(os.path.join(BOOK_IMAGES_DIR, f"{carte_id}.*")):
        os.remove(old_file)

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
    os.makedirs(BOOK_IMAGES_DIR, exist_ok=True)
    matches = glob.glob(os.path.join(BOOK_IMAGES_DIR, f"{carte_id}.*"))

    # Filter to only allowed extensions
    matches = [m for m in matches if m.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS]

    if not matches:
        return jsonify({'success': False, 'message': 'No book image found'}), 404

    return send_from_directory(BOOK_IMAGES_DIR, os.path.basename(matches[0]))
