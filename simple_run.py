#!/usr/bin/env python3
"""
Completely clean approach - uses subprocess to avoid any SQLAlchemy conflicts
"""

import os
import subprocess
import sys

def main():
    print("Beauty Analytics - Clean Start")
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Check environment
    if not os.environ.get('DATABASE_URL'):
        print("Error: DATABASE_URL missing in .env file")
        return
    
    if not os.environ.get('FLASK_SECRET_KEY'):
        print("Error: FLASK_SECRET_KEY missing in .env file")
        return
    
    # Step 1: Initialize database in a clean subprocess
    print("Step 1: Creating database tables...")
    
    init_script = '''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from werkzeug.security import generate_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Define models
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
    
    # Add basic data if empty
    if db.session.execute(db.select(User)).first() is None:
        admin = User(username='admin', email='admin@beautyapp.com', 
                    full_name='Admin', is_admin=True)
        admin.password_hash = generate_password_hash('admin123')
        
        user = User(username='user', email='user@example.com', full_name='Test User')
        user.password_hash = generate_password_hash('password123')
        
        cat1 = Category(name='Skincare', description='Skin care products')
        cat2 = Category(name='Makeup', description='Makeup products')
        
        db.session.add_all([admin, user, cat1, cat2])
        db.session.commit()
        
        prod1 = Product(name='Gentle Cleanser', price=150000, brand='Beauty Co', 
                       category_id=1, stock_quantity=50)
        prod2 = Product(name='Lipstick Classic', price=200000, brand='Makeup Co', 
                       category_id=2, stock_quantity=30)
        
        db.session.add_all([prod1, prod2])
        db.session.commit()
        
        print("Database initialized with sample data")
    else:
        print("Database already contains data")
'''
    
    # Write and run init script
    with open('temp_init.py', 'w') as f:
        f.write(init_script)
    
    result = subprocess.run([sys.executable, 'temp_init.py'], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Database created successfully!")
        print(result.stdout)
    else:
        print("Database creation failed:")
        print(result.stderr)
        return
    
    # Step 2: Create and run server
    print("\nStep 2: Starting web server...")
    
    server_script = '''
import os
from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Beauty Analytics</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">Beauty Analytics</h1>
            <div class="row">
                <div class="col-md-6 offset-md-3">
                    <div class="card">
                        <div class="card-body text-center">
                            <h5 class="card-title">Web App Running Successfully!</h5>
                            <p class="card-text">Your Supabase database is connected and ready.</p>
                            <div class="d-grid gap-2">
                                <a href="/status" class="btn btn-primary">Check Database Status</a>
                                <a href="/admin" class="btn btn-success">Admin Info</a>
                                <a href="/features" class="btn btn-info">Available Features</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
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
        
        # Get table info
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        tables = cursor.fetchall()
        
        # Get data counts
        cursor.execute('SELECT COUNT(*) FROM "user"')
        user_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM category')
        category_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM product')
        product_count = cursor.fetchone()[0]
        
        conn.close()
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Database Status</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h2>Database Status</h2>
                <div class="alert alert-success">
                    <strong>Connection: Success</strong>
                </div>
                <table class="table">
                    <tr><th>Tables Created</th><td>{len(tables)}</td></tr>
                    <tr><th>Users</th><td>{user_count}</td></tr>
                    <tr><th>Categories</th><td>{category_count}</td></tr>
                    <tr><th>Products</th><td>{product_count}</td></tr>
                </table>
                <h4>Tables:</h4>
                <ul>
                    {"".join(f"<li>{table[0]}</li>" for table in tables)}
                </ul>
                <a href="/" class="btn btn-primary">Back to Home</a>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        return f"""
        <div class="container mt-5">
            <div class="alert alert-danger">Database Error: {e}</div>
            <a href="/" class="btn btn-primary">Back</a>
        </div>
        """

@app.route('/admin')
def admin():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Info</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h2>Admin Account</h2>
            <div class="card">
                <div class="card-body">
                    <h5>Default Admin Login:</h5>
                    <p><strong>Email:</strong> admin@beautyapp.com</p>
                    <p><strong>Password:</strong> admin123</p>
                    <hr>
                    <h5>Test User Login:</h5>
                    <p><strong>Email:</strong> user@example.com</p>
                    <p><strong>Password:</strong> password123</p>
                </div>
            </div>
            <a href="/" class="btn btn-primary mt-3">Back to Home</a>
        </div>
    </body>
    </html>
    """

@app.route('/features')
def features():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Available Features</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h2>Beauty Analytics Features</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">AI Skin Analysis</h5>
                            <p class="card-text">Face++ powered skin analysis with camera capture</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">E-commerce</h5>
                            <p class="card-text">Product catalog with shopping cart and checkout</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">AI Chat</h5>
                            <p class="card-text">Beauty consultation chatbot</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="alert alert-info">
                <strong>Status:</strong> Database initialized and ready for full application deployment
            </div>
            <a href="/" class="btn btn-primary">Back to Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("Server starting at http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
'''
    
    # Write server script
    with open('temp_server.py', 'w') as f:
        f.write(server_script)
    
    print("Server ready. Starting at http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    # Run server
    subprocess.run([sys.executable, 'temp_server.py'])

if __name__ == '__main__':
    main()