import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Set environment variable
os.environ.setdefault('FLASK_SECRET_KEY', 'beauty-analytics-secret-key-2024')

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

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import database and models from existing database.py
from database import db, User, Product, Category, SkinAnalysis, BlogPost

# Initialize database with app
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except:
        return None

# Routes
@app.route('/')
def index():
    try:
        # Get featured products
        featured_products = db.session.query(Product).filter_by(is_active=True).limit(6).all()
        return render_template('index.html', products=featured_products)
    except Exception as e:
        print(f"Index route error: {e}")
        return render_template('index.html', products=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = db.session.query(User).filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash('Đăng nhập thành công!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
        except Exception as e:
            print(f"Login error: {e}")
            flash('Có lỗi xảy ra khi đăng nhập', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get user's recent analyses
        recent_analyses = db.session.query(SkinAnalysis).filter_by(user_id=current_user.id).order_by(SkinAnalysis.date_analyzed.desc()).limit(3).all()
        return render_template('dashboard.html', analyses=recent_analyses)
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', analyses=[])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất thành công', 'info')
    return redirect(url_for('index'))

@app.route('/products')
def products():
    try:
        page = request.args.get('page', 1, type=int)
        category_id = request.args.get('category')
        search = request.args.get('search')
        
        query = db.session.query(Product).filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        if search:
            query = query.filter(Product.name.contains(search))
        
        # Simple pagination without Flask-SQLAlchemy paginate method
        products_list = query.limit(12).offset((page-1)*12).all()
        categories = db.session.query(Category).all()
        
        return render_template('products.html', products=products_list, categories=categories)
    except Exception as e:
        print(f"Products route error: {e}")
        return render_template('products.html', products=[], categories=[])

@app.route('/skin-analysis')
@login_required
def skin_analysis():
    return render_template('skin_analysis.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/blog')
def blog():
    try:
        posts = db.session.query(BlogPost).filter_by(is_published=True).order_by(BlogPost.date_created.desc()).limit(10).all()
        return render_template('blog.html', posts=posts)
    except Exception as e:
        print(f"Blog route error: {e}")
        return render_template('blog.html', posts=[])

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"Internal server error: {error}")
    return render_template('500.html'), 500

# Create tables on startup
with app.app_context():
    try:
        db.create_all()
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Database initialization warning: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)