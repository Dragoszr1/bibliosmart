import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_COOKIE_NAME = 'access_token'
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_SECURE = False  # Set True in production with HTTPS

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # MySQL database configuration
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'admin'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'proiectbiblioteca26'
    DB_NAME = os.environ.get('DB_NAME') or 'biblioteca'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # MySQL database configuration
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'admin'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'proiectbiblioteca26'
    DB_NAME = os.environ.get('DB_NAME') or 'biblioteca'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
