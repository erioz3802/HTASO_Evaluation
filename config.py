"""Flask application configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration."""

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + str(BASE_DIR / 'app.db')  # SQLite for local development
    ).replace('postgres://', 'postgresql://', 1)  # Fix for Render's DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Data storage (legacy JSON support for migration)
    DATA_DIR = Path(os.getenv('DATA_DIR', BASE_DIR.parent / 'evaluation_data'))
    ADMIN_CONFIG = Path(os.getenv('ADMIN_CONFIG', DATA_DIR / 'admin_config.json'))
    CRITERIA_PATH = Path(os.getenv('CRITERIA_PATH', BASE_DIR / 'Evaluator Training Eval form.xlsx'))

    # File upload settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB

    # Session settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # Application settings
    LOGO_PATH = BASE_DIR / 'static' / 'images' / 'logo-150.png'
    PORT = int(os.getenv('PORT', 8502))

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Requires HTTPS

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
