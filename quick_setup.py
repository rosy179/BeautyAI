#!/usr/bin/env python3
"""
Quick setup script for Beauty Analytics with Supabase
Resolves SQLAlchemy model conflicts
"""

import os
import sys

def main():
    print("Beauty Analytics - Supabase Setup")
    print("-" * 40)
    
    # Check environment variables
    required_vars = ['DATABASE_URL', 'FLASK_SECRET_KEY']
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        print(f"Missing: {', '.join(missing)}")
        print("Configure .env file first")
        return False
    
    # Test connection with psycopg2 directly
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        db_url = os.environ.get('DATABASE_URL')
        parsed = urlparse(db_url)
        
        print("Testing connection...")
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print("Connection successful")
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
    
    # Create tables using subprocess to avoid import conflicts
    print("Creating database tables...")
    import subprocess
    
    result = subprocess.run([
        sys.executable, "-c",
        "from app import app, db; app.app_context().push(); db.create_all(); print('Tables created')"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Table creation failed: {result.stderr}")
        return False
    
    print(result.stdout.strip())
    
    # Add sample data
    print("Adding sample data...")
    result = subprocess.run([sys.executable, "seed_data.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Sample data added")
    else:
        print("Sample data failed, but tables are ready")
    
    print("\nSetup complete! Run: python run_local.py")
    return True

if __name__ == "__main__":
    # Load environment if dotenv available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    main()