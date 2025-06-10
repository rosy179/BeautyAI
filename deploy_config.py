#!/usr/bin/env python3
"""
Configuration script for deployment environments
Handles different database configurations and environment settings
"""

import os
from urllib.parse import urlparse

def get_database_config():
    """
    Determine database configuration based on environment
    Returns appropriate SQLAlchemy configuration
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    
    # Parse the database URL
    url = urlparse(database_url)
    
    # Base configuration
    config = {
        'SQLALCHEMY_DATABASE_URI': database_url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_recycle': 300,
            'pool_pre_ping': True,
            'connect_args': {}
        }
    }
    
    # Supabase-specific configuration
    if url.hostname and 'supabase.co' in url.hostname:
        print("Configuring for Supabase database...")
        config['SQLALCHEMY_ENGINE_OPTIONS']['connect_args'] = {
            'sslmode': 'require',
            'connect_timeout': 10
        }
        config['SQLALCHEMY_ENGINE_OPTIONS']['pool_size'] = 5
        config['SQLALCHEMY_ENGINE_OPTIONS']['max_overflow'] = 10
    
    # Local PostgreSQL configuration
    elif url.hostname in ['localhost', '127.0.0.1']:
        print("Configuring for local PostgreSQL...")
        config['SQLALCHEMY_ENGINE_OPTIONS']['pool_size'] = 10
        config['SQLALCHEMY_ENGINE_OPTIONS']['max_overflow'] = 20
    
    # Heroku PostgreSQL configuration
    elif url.hostname and ('heroku' in url.hostname or 'amazonaws.com' in url.hostname):
        print("☁️ Configuring for Heroku/AWS PostgreSQL...")
        config['SQLALCHEMY_ENGINE_OPTIONS']['connect_args'] = {
            'sslmode': 'require'
        }
        config['SQLALCHEMY_ENGINE_OPTIONS']['pool_size'] = 5
    
    return config

def validate_environment():
    """
    Validate that all required environment variables are set
    """
    required_vars = [
        'DATABASE_URL',
        'FLASK_SECRET_KEY',
        'FACEPP_API_KEY',
        'FACEPP_API_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file or environment configuration.")
        return False
    
    print("✅ All required environment variables are set")
    return True

def get_upload_config():
    """
    Configure file upload settings based on environment
    """
    upload_folder = os.environ.get('UPLOAD_FOLDER', 'static/uploads')
    max_content_length = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))  # 16MB default
    
    # Create upload directory if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    
    return {
        'UPLOAD_FOLDER': upload_folder,
        'MAX_CONTENT_LENGTH': max_content_length,
        'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'gif'}
    }

def configure_app(app):
    """
    Apply all configuration to Flask app
    """
    print("🔧 Configuring Flask application...")
    
    # Validate environment
    if not validate_environment():
        raise EnvironmentError("Missing required environment variables")
    
    # Database configuration
    db_config = get_database_config()
    for key, value in db_config.items():
        app.config[key] = value
    
    # Upload configuration
    upload_config = get_upload_config()
    for key, value in upload_config.items():
        app.config[key] = value
    
    # Security configuration
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # WTF CSRF configuration
    app.config['WTF_CSRF_ENABLED'] = os.environ.get('WTF_CSRF_ENABLED', 'True').lower() == 'true'
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY', app.config['SECRET_KEY'])
    
    print("✅ Flask application configured successfully")
    return app

if __name__ == '__main__':
    # Test configuration
    print("Testing configuration...")
    validate_environment()
    print(get_database_config())
    print(get_upload_config())