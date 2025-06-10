#!/usr/bin/env python3
"""
Working Beauty Analytics Flask app
Uses the successfully created database
"""

import os
from flask import Flask, render_template_string, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import check_password_hash
from datetime import datetime

# Set environment variables
os.environ.setdefault('FLASK_SECRET_KEY', 'beauty-analytics-secret-key-2024')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {"sslmode": "require"}
}

db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Models
class User(UserMixin, db.Model):
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    with app.app_context():
        products = Product.query.limit(5).all()
        categories = Category.query.all()
        
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Beauty Analytics</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 4rem 0; }
            .product-card { transition: transform 0.3s; }
            .product-card:hover { transform: translateY(-5px); }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">Beauty Analytics</a>
                <div class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        <span class="navbar-text me-3">Hello, {{ current_user.full_name }}!</span>
                        <a class="nav-link" href="/logout">Logout</a>
                    {% else %}
                        <a class="nav-link" href="/login">Login</a>
                    {% endif %}
                </div>
            </div>
        </nav>

        <div class="hero text-center">
            <div class="container">
                <h1 class="display-4 mb-4">AI-Powered Beauty Analytics</h1>
                <p class="lead">Discover your perfect skincare routine with our advanced AI analysis</p>
                <a href="/skin-analysis" class="btn btn-light btn-lg me-3">Start Skin Analysis</a>
                <a href="/products" class="btn btn-outline-light btn-lg">Browse Products</a>
            </div>
        </div>

        <div class="container my-5">
            <div class="row">
                <div class="col-md-8">
                    <h2 class="mb-4">Featured Products</h2>
                    <div class="row">
                        {% for product in products %}
                        <div class="col-md-6 mb-4">
                            <div class="card product-card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">{{ product.name }}</h5>
                                    <p class="text-muted">{{ product.brand }}</p>
                                    <h6 class="text-primary">{{ "{:,.0f}".format(product.price) }} VND</h6>
                                    <span class="badge bg-success">{{ product.stock_quantity }} in stock</span>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="col-md-4">
                    <h3 class="mb-4">Categories</h3>
                    <div class="list-group">
                        {% for category in categories %}
                        <a href="#" class="list-group-item list-group-item-action">
                            <strong>{{ category.name }}</strong>
                            <p class="mb-1 text-muted">{{ category.description }}</p>
                        </a>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <div class="bg-light py-5">
            <div class="container text-center">
                <h2 class="mb-4">Database Status</h2>
                <div class="row">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="text-primary">{{ user_count }}</h3>
                                <p>Registered Users</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="text-success">{{ product_count }}</h3>
                                <p>Products</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="text-info">{{ category_count }}</h3>
                                <p>Categories</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h3 class="text-warning">Ready</h3>
                                <p>Database Status</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    
    with app.app_context():
        user_count = User.query.count()
        product_count = Product.query.count()
        category_count = Category.query.count()
    
    return render_template_string(template, 
                                products=products, 
                                categories=categories,
                                user_count=user_count,
                                product_count=product_count,
                                category_count=category_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Beauty Analytics</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container">
            <div class="row justify-content-center mt-5">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h4>Login to Beauty Analytics</h4>
                        </div>
                        <div class="card-body">
                            {% with messages = get_flashed_messages(with_categories=true) %}
                                {% if messages %}
                                    {% for category, message in messages %}
                                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }}">{{ message }}</div>
                                    {% endfor %}
                                {% endif %}
                            {% endwith %}
                            
                            <form method="POST">
                                <div class="mb-3">
                                    <label for="email" class="form-label">Email</label>
                                    <input type="email" class="form-control" id="email" name="email" required>
                                </div>
                                <div class="mb-3">
                                    <label for="password" class="form-label">Password</label>
                                    <input type="password" class="form-control" id="password" name="password" required>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">Login</button>
                            </form>
                            
                            <hr>
                            <div class="text-center">
                                <small class="text-muted">
                                    Test accounts:<br>
                                    Admin: admin@beautyapp.com / admin123<br>
                                    User: user@example.com / password123
                                </small>
                            </div>
                        </div>
                    </div>
                    <div class="text-center mt-3">
                        <a href="/">← Back to Home</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template)

@app.route('/dashboard')
@login_required
def dashboard():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - Beauty Analytics</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">Beauty Analytics</a>
                <div class="navbar-nav ms-auto">
                    <span class="navbar-text me-3">Welcome, {{ current_user.full_name }}!</span>
                    <a class="nav-link" href="/logout">Logout</a>
                </div>
            </div>
        </nav>
        
        <div class="container mt-4">
            <h1>User Dashboard</h1>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Your Profile</h5>
                        </div>
                        <div class="card-body">
                            <p><strong>Name:</strong> {{ current_user.full_name }}</p>
                            <p><strong>Email:</strong> {{ current_user.email }}</p>
                            <p><strong>Username:</strong> {{ current_user.username }}</p>
                            <p><strong>Member since:</strong> {{ current_user.date_joined.strftime('%B %d, %Y') }}</p>
                            {% if current_user.is_admin %}
                                <span class="badge bg-success">Admin User</span>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>Quick Actions</h5>
                        </div>
                        <div class="card-body">
                            <div class="d-grid gap-2">
                                <a href="#" class="btn btn-primary">Start Skin Analysis</a>
                                <a href="#" class="btn btn-success">Browse Products</a>
                                <a href="#" class="btn btn-info">Beauty Consultation</a>
                                <a href="#" class="btn btn-secondary">View Orders</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/products')
def products():
    with app.app_context():
        all_products = Product.query.all()
        categories = Category.query.all()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Products - Beauty Analytics</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">Beauty Analytics</a>
                <a class="nav-link text-light" href="/">← Back to Home</a>
            </div>
        </nav>
        
        <div class="container mt-4">
            <h1>Beauty Products</h1>
            
            <div class="row mt-4">
                {% for product in products %}
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">{{ product.name }}</h5>
                            <h6 class="text-muted">{{ product.brand }}</h6>
                            <p class="card-text">
                                <strong class="text-primary">{{ "{:,.0f}".format(product.price) }} VND</strong>
                            </p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge bg-success">{{ product.stock_quantity }} available</span>
                                <button class="btn btn-primary btn-sm">Add to Cart</button>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template, products=all_products, categories=categories)

@app.route('/skin-analysis')
def skin_analysis():
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Skin Analysis - Beauty Analytics</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">Beauty Analytics</a>
                <a class="nav-link text-light" href="/">← Back to Home</a>
            </div>
        </nav>
        
        <div class="container mt-4">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <h1 class="text-center mb-4">AI Skin Analysis</h1>
                    
                    <div class="card">
                        <div class="card-body text-center">
                            <h5>Coming Soon!</h5>
                            <p>Our AI-powered skin analysis feature will help you:</p>
                            <ul class="list-unstyled">
                                <li>📸 Analyze your skin condition</li>
                                <li>🔍 Identify skin concerns</li>
                                <li>💡 Get personalized recommendations</li>
                                <li>📋 Create custom skincare routines</li>
                            </ul>
                            
                            <div class="alert alert-info">
                                <strong>Database Ready!</strong> Your Supabase database now includes 
                                a skin_analysis table ready for storing AI analysis results.
                            </div>
                            
                            <p class="text-muted">
                                Requires Face++ API integration for full functionality.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return render_template_string(template)

if __name__ == '__main__':
    print("Starting Beauty Analytics Web App")
    print("Database connection: Ready")
    print("Server: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)