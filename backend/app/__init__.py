from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from app.database import db

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {
        "origins": app.config.get('CORS_ORIGINS', ['http://localhost:5173', 'http://localhost:3000']),
        "supports_credentials": True
    }})
    
    # Create database tables
    with app.app_context():
        from app.models import Carti, Users, CartiCitite, Recenzii, ImprumuturiActive
    
    # Register blueprints
    from app.routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.books_routes import books_bp, requests_bp
    from app.routes.admin_routes import admin_bp, librarian_bp
    from app.routes.reviews_routes import reviews_bp
    from app.routes.anunturi_routes import anunturi_bp
    from app.routes.ai_routes import ai_bp
    from app.routes.club_routes import club_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(books_bp, url_prefix='/api/books')
    app.register_blueprint(requests_bp, url_prefix='/api/book-requests')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(librarian_bp, url_prefix='/api/librarian')
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
    app.register_blueprint(anunturi_bp, url_prefix='/api/anunturi')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(club_bp, url_prefix='/api/club')
    
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['Content-Security-Policy'] = "default-src 'self' data: blob:; frame-ancestors 'none';"
        return response

    return app
