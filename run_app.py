#!/usr/bin/env python3
"""
Simple startup script for Beauty Analytics
Completely clean approach without circular imports
"""

import os
import sys

def setup_environment():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

def check_config():
    """Check required environment variables"""
    required = ['DATABASE_URL', 'FLASK_SECRET_KEY']
    missing = [var for var in required if not os.environ.get(var)]
    
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        print("Configure your .env file first")
        return False
    return True

def create_tables():
    """Create database tables"""
    from app_clean import app
    from database import db
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check tables created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created {len(tables)} tables: {', '.join(tables)}")
        return True

def add_sample_data():
    """Add sample data if database is empty"""
    from app_clean import app
    from database import User
    
    with app.app_context():
        if User.query.count() == 0:
            print("Adding sample data...")
            import subprocess
            result = subprocess.run([sys.executable, "seed_clean.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("Sample data added")
            else:
                print("Sample data failed, continuing anyway")

def start_server():
    """Start the Flask development server"""
    from app_clean import app, init_app
    
    init_app()
    
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)

def main():
    print("Beauty Analytics - Starting...")
    
    setup_environment()
    
    if not check_config():
        return
    
    try:
        create_tables()
        add_sample_data()
        start_server()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()