#!/usr/bin/env python3
"""
Database initialization script for Beauty Analytics
Creates all tables in Supabase database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    """Initialize database tables"""
    try:
        # Import Flask app components
        from app import app, db
        
        print("🔄 Initializing database tables...")
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # List created tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📋 Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
                
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def seed_sample_data():
    """Add sample data to database"""
    try:
        print("\n🌱 Adding sample data...")
        
        # Run seed script
        import subprocess
        result = subprocess.run([sys.executable, "seed_data.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample data added successfully!")
            return True
        else:
            print(f"❌ Seed data failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Seed data error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Beauty Analytics Database Setup\n")
    
    # Check environment
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found. Please configure .env file first.")
        sys.exit(1)
    
    print(f"📍 Database: {db_url[:50]}...")
    
    # Initialize database
    if init_database():
        # Add sample data
        if seed_sample_data():
            print("\n🎉 Database setup complete!")
            print("👉 Now run: python run_local.py")
        else:
            print("\n⚠️ Database created but sample data failed.")
            print("👉 You can still run: python run_local.py")
    else:
        print("\n❌ Database setup failed. Check your configuration.")
        sys.exit(1)