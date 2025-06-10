import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'beauty-analytics-secret-key-2024')

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import database after app creation to avoid circular imports
try:
    from database import db, User, Product, Category, SkinAnalysis
    db.init_app(app)
    logger.info("Database models imported successfully")
except Exception as e:
    logger.error(f"Database import failed: {e}")
    # Fallback - create minimal in-memory storage
    users = {}
    products = []

# Models are imported from database.py to avoid conflicts

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except:
        return None

# Routes
@app.route('/')
def index():
    with app.app_context():
        products = Product.query.limit(6).all()
        categories = Category.query.all()
        user_count = User.query.count()
        product_count = Product.query.count()
        category_count = Category.query.count()
    
    return render_template('index.html', 
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
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email hoặc mật khẩu không đúng', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('index'))

@app.route('/products')
def products():
    with app.app_context():
        all_products = Product.query.all()
        categories = Category.query.all()
    
    return render_template('products.html', products=all_products, categories=categories)

@app.route('/skin-analysis')
def skin_analysis():
    return render_template('skin_analysis.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
