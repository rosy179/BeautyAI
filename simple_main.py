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

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except:
        return None

@app.route('/')
def index():
    try:
        # Get featured products
        featured_products = db.session.query(Product).filter_by(is_active=True).limit(6).all()
        return render_template('index.html', products=featured_products)
    except Exception as e:
        logger.error(f"Index route error: {e}")
        return render_template('index.html', products=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = db.session.query(User).filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
        except Exception as e:
            logger.error(f"Login error: {e}")
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
        logger.error(f"Dashboard error: {e}")
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
        
        products = query.paginate(page=page, per_page=12, error_out=False)
        categories = db.session.query(Category).all()
        
        return render_template('products.html', products=products, categories=categories)
    except Exception as e:
        logger.error(f"Products route error: {e}")
        return render_template('products.html', products=[], categories=[])

@app.route('/skin-analysis')
@login_required
def skin_analysis():
    return render_template('skin_analysis.html')

@app.route('/analyze-image', methods=['POST'])
@login_required
def analyze_image():
    try:
        # Import face analysis module
        from face_analysis import FaceAnalyzer
        
        if 'image' not in request.files:
            return jsonify({'error': 'Không có file được tải lên'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Không có file được chọn'}), 400
        
        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            file.save(tmp_file.name)
            
            # Analyze the image
            analyzer = FaceAnalyzer()
            result = analyzer.analyze_skin(tmp_file.name)
            
            # Save analysis to database
            analysis = SkinAnalysis(
                user_id=current_user.id,
                analysis_result=result,
                skin_type=result.get('skin_type'),
                skin_concerns=result.get('concerns'),
                recommended_routine=result.get('routine')
            )
            db.session.add(analysis)
            db.session.commit()
            
            return jsonify(result)
            
    except Exception as e:
        logger.error(f"Image analysis error: {e}")
        return jsonify({'error': 'Có lỗi xảy ra khi phân tích hình ảnh'}), 500

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/blog')
def blog():
    try:
        from database import BlogPost
        posts = db.session.query(BlogPost).filter_by(is_published=True).order_by(BlogPost.date_created.desc()).limit(10).all()
        return render_template('blog.html', posts=posts)
    except Exception as e:
        logger.error(f"Blog route error: {e}")
        return render_template('blog.html', posts=[])

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Database creation failed: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)