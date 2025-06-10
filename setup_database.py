#!/usr/bin/env python3
"""
Clean database setup for Beauty Analytics with Supabase
Avoids SQLAlchemy model conflicts
"""

import os
import sys

def check_environment():
    """Check if environment is properly configured"""
    required_vars = ['DATABASE_URL', 'FLASK_SECRET_KEY']
    missing = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        print("Please configure your .env file first")
        return False
    
    return True

def test_connection():
    """Test database connection without importing models"""
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        db_url = os.environ.get('DATABASE_URL')
        parsed = urlparse(db_url)
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"Connected to: {version[:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def create_tables():
    """Create database tables"""
    try:
        # Fresh import to avoid conflicts
        import importlib
        
        # Clear any cached modules
        modules_to_clear = ['app', 'models']
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]
        
        # Import fresh
        from app import app, db
        
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            
            # Verify tables created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"Table creation failed: {e}")
        return False

def add_sample_data():
    """Add sample data using subprocess to avoid conflicts"""
    try:
        import subprocess
        
        print("Adding sample data...")
        result = subprocess.run([sys.executable, "seed_data.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Sample data added successfully")
            return True
        else:
            print(f"Sample data failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Sample data error: {e}")
        return False

if __name__ == "__main__":
    print("Beauty Analytics Database Setup")
    print("=" * 40)
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("Environment loaded")
    except ImportError:
        print("Note: python-dotenv not available, using system environment")
    
    # Check configuration
    if not check_environment():
        sys.exit(1)
    
    # Test connection
    print("\nTesting database connection...")
    if not test_connection():
        print("Fix database connection first")
        sys.exit(1)
    
    # Create tables
    print("\nCreating tables...")
    if not create_tables():
        print("Fix table creation issues")
        sys.exit(1)
    
    # Add sample data
    print("\nAdding sample data...")
    add_sample_data()
    
    print("\nDatabase setup complete!")
    print("Run: python run_local.py")