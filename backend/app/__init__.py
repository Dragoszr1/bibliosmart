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
    app.register_blueprint(main_bp)
    
    return app
