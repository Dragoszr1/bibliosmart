import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_COOKIE_NAME = 'access_token'
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_SECURE = False  # Set True in production with HTTPS
    
    # SQLAlchemy Pool Options to prevent "MySQL server has gone away"
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }

    # SMTP / Email configuration (Gmail App Password)
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', '')       # e.g. yourname@gmail.com
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '') # Gmail App Password
    SMTP_FROM = os.environ.get('SMTP_FROM', '')         # defaults to SMTP_USER if blank

    # Groq AI
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # MySQL database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME', 'biblioteca')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    JWT_COOKIE_SECURE = True  # Require HTTPS for cookies
    # MySQL database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME', 'biblioteca')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    CORS_ORIGINS = [
        os.environ.get('SITE_URL', 'https://bibliosmart.online'),
        'https://www.bibliosmart.online',
    ]

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
