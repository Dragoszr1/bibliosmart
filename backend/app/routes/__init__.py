from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import bcrypt

from app.database import db
from app.models import Carti, Users, CartiCitite, Recenzii

main_bp = Blueprint('main', __name__, url_prefix='/api')

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
    """Basic books route - implement your queries here"""
    return jsonify({'message': 'Books endpoint - implement your database queries here'}), 200

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
    """Basic reviews route - implement your queries here"""
    return jsonify({'message': 'Reviews endpoint - implement your database queries here'}), 200

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
        "SELECT username, email, description FROM users WHERE email = :email"
    )
    result = db.session.execute(query, {'email': email}).mappings().first()
    if not result:
        return jsonify({'success': False, 'message': 'Profile not found'}), 404

    return jsonify({
        'success': True,
        'username': result.get('username'),
        'email': result.get('email'),
        'description': result.get('description')
    }), 200

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
