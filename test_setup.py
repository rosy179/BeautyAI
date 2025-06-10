#!/usr/bin/env python3
"""
Test script for Beauty Analytics database setup
"""

import os
import sys
import subprocess

def load_env():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except ImportError:
        return False

def test_environment():
    """Test environment variables"""
    print("Testing environment variables...")
    
    db_url = os.environ.get('DATABASE_URL')
    secret_key = os.environ.get('FLASK_SECRET_KEY')
    
    if not db_url:
        print("❌ DATABASE_URL missing")
        return False
    
    if not secret_key:
        print("❌ FLASK_SECRET_KEY missing")
        return False
    
    print("✅ Environment variables found")
    print(f"Database: {db_url[:50]}...")
    return True

def test_connection():
    """Test database connection"""
    print("Testing database connection...")
    
    script = '''
import os
import sys
try:
    import psycopg2
    from urllib.parse import urlparse
    
    db_url = os.environ.get('DATABASE_URL')
    parsed = urlparse(db_url)
    
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password,
        connect_timeout=20,
        sslmode='require'
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if result[0] == 1:
        print("Database connection successful")
        sys.exit(0)
    else:
        print("Database connection failed")
        sys.exit(1)
        
except Exception as e:
    print(f"Connection error: {e}")
    sys.exit(1)
'''
    
    with open('temp_test.py', 'w') as f:
        f.write(script)
    
    try:
        result = subprocess.run([sys.executable, 'temp_test.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Database connection successful")
            print(result.stdout)
            return True
        else:
            print("❌ Database connection failed")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Connection test timed out")
        return False
    finally:
        if os.path.exists('temp_test.py'):
            os.remove('temp_test.py')

def create_tables():
    """Create database tables"""
    print("Creating database tables...")
    
    script = '''
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {"sslmode": "require"}
}

db.init_app(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    stock_quantity = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()
    
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"Created {len(tables)} tables")
    for table in tables:
        print(f"  - {table}")
    
    # Add sample data
    if not db.session.execute(db.select(User)).first():
        admin = User(
            username='admin',
            email='admin@beautyapp.com',
            full_name='Admin User',
            is_admin=True
        )
        admin.password_hash = generate_password_hash('admin123')
        
        user = User(
            username='testuser',
            email='user@example.com',
            full_name='Test User'
        )
        user.password_hash = generate_password_hash('password123')
        
        cat = Category(name='Skincare', description='Skin care products')
        
        prod = Product(
            name='Sample Product',
            price=100000,
            brand='Test Brand',
            category_id=1,
            stock_quantity=10
        )
        
        db.session.add_all([admin, user, cat])
        db.session.commit()
        
        db.session.add(prod)
        db.session.commit()
        
        print("Sample data added")
    else:
        print("Data already exists")
    
    print("Database setup complete")
'''
    
    with open('temp_create.py', 'w') as f:
        f.write(script)
    
    try:
        result = subprocess.run([sys.executable, 'temp_create.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Tables created successfully")
            print(result.stdout)
            return True
        else:
            print("❌ Table creation failed")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Table creation timed out")
        return False
    finally:
        if os.path.exists('temp_create.py'):
            os.remove('temp_create.py')

def main():
    print("Beauty Analytics - Database Test")
    print("=" * 40)
    
    # Load environment
    load_env()
    
    # Test environment
    if not test_environment():
        print("Environment test failed")
        return False
    
    # Test connection
    if not test_connection():
        print("Connection test failed")
        return False
    
    # Create tables
    if not create_tables():
        print("Table creation failed")
        return False
    
    print("\n" + "=" * 40)
    print("✅ ALL TESTS PASSED!")
    print("Your database is ready for use")
    print("Admin: admin@beautyapp.com / admin123")
    print("User: user@example.com / password123")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)