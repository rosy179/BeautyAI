#!/usr/bin/env python3
"""
Fresh start script that completely avoids SQLAlchemy mapper conflicts
Uses a clean subprocess approach
"""

import os
import sys
import subprocess

def setup_environment():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

def check_requirements():
    """Check environment and database connection"""
    required = ['DATABASE_URL', 'FLASK_SECRET_KEY']
    missing = [var for var in required if not os.environ.get(var)]
    
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        print("Please configure your .env file")
        return False
    
    # Test database connection with psycopg2
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
        conn.close()
        print("Database connection successful")
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def create_initialization_script():
    """Create a one-time script to initialize database"""
    script_content = '''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    full_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    stock_quantity = db.Column(db.Integer, default=0)
    skin_type = db.Column(db.String(100))
    image_url = db.Column(db.String(500))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)

class SkinAnalysis(db.Model):
    __tablename__ = 'skin_analysis'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    analysis_result = db.Column(db.JSON)
    date_analyzed = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    
    # Add sample data if empty
    if User.query.count() == 0:
        admin = User(username='admin', email='admin@beautyapp.com', 
                    full_name='Admin User', is_admin=True)
        admin.set_password('admin123')
        
        user = User(username='testuser', email='user@example.com', 
                   full_name='Test User')
        user.set_password('password123')
        
        skincare = Category(name='Chăm sóc da', description='Sản phẩm chăm sóc da')
        makeup = Category(name='Trang điểm', description='Sản phẩm trang điểm')
        
        product1 = Product(name='Sữa rửa mặt Gentle', description='Sữa rửa mặt dịu nhẹ',
                          price=150000, brand='Beauty Brand', category_id=1, stock_quantity=50)
        
        product2 = Product(name='Son môi Classic', description='Son môi màu đỏ cổ điển',
                          price=200000, brand='Makeup Brand', category_id=2, stock_quantity=30)
        
        blog = BlogPost(title='Hướng dẫn chăm sóc da cơ bản', 
                       content='Nội dung hướng dẫn chi tiết...', 
                       author_id=1, is_published=True)
        
        db.session.add_all([admin, user, skincare, makeup, product1, product2, blog])
        db.session.commit()
        print("Database initialized with sample data")
    else:
        print("Database already has data")
'''
    
    with open('init_db_once.py', 'w', encoding='utf-8') as f:
        f.write(script_content)

def run_server_script():
    """Create server script"""
    server_content = '''
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import sys

# Simple app without complex imports
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key")

# Simple routes
@app.route('/')
def index():
    return """
    <h1>Beauty Analytics</h1>
    <p>Web app is running successfully!</p>
    <a href='/test'>Test Database</a> | 
    <a href='/admin'>Admin Login</a>
    """

@app.route('/test')
def test_db():
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
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM "user"')
        user_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM product')
        product_count = cursor.fetchone()[0]
        
        conn.close()
        
        return f"""
        <h2>Database Status</h2>
        <p>Tables: {len(tables)}</p>
        <p>Users: {user_count}</p>
        <p>Products: {product_count}</p>
        <p>All working!</p>
        <a href='/'>Back to Home</a>
        """
        
    except Exception as e:
        return f"Database error: {e}"

@app.route('/admin')
def admin():
    return """
    <h2>Admin Login</h2>
    <p>Default admin account:</p>
    <p>Email: admin@beautyapp.com</p>
    <p>Password: admin123</p>
    <p>Database is ready for your full application!</p>
    <a href='/'>Back to Home</a>
    """

if __name__ == '__main__':
    print("Server starting at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
    
    with open('run_server.py', 'w', encoding='utf-8') as f:
        f.write(server_content)

def main():
    print("Beauty Analytics - Fresh Setup")
    print("-" * 40)
    
    setup_environment()
    
    if not check_requirements():
        return
    
    print("Creating initialization script...")
    create_initialization_script()
    
    print("Initializing database...")
    result = subprocess.run([sys.executable, 'init_db_once.py'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Database initialized successfully!")
        print(result.stdout)
    else:
        print("Database initialization failed:")
        print(result.stderr)
        return
    
    print("Creating server script...")
    run_server_script()
    
    print("\nSetup complete!")
    print("Run: python run_server.py")
    print("Then visit: http://localhost:5000")

if __name__ == '__main__':
    main()