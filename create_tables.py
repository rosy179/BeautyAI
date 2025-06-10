#!/usr/bin/env python3
"""
Simple script to create database tables for Beauty Analytics
"""

import os
import sys

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def create_database_tables():
    """Create all database tables"""
    try:
        from app import app, db
        
        with app.app_context():
            # Import models first
            import models
            
            # Create all tables
            db.create_all()
            
            print("Database tables created successfully!")
            
            # List created tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
                
            return True
            
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Creating database tables...")
    
    # Check required environment variables
    if not os.environ.get('DATABASE_URL'):
        print("Error: DATABASE_URL not found in environment")
        print("Make sure your .env file is configured")
        sys.exit(1)
    
    if create_database_tables():
        print("\nNext steps:")
        print("1. Run: python seed_data.py")
        print("2. Run: python run_local.py")
    else:
        print("Failed to create tables")
        sys.exit(1)