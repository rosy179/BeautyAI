import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import db
from models import User, Product, Category, Order, OrderItem, Review, BlogPost, BlogComment, SkinAnalysis, ChatMessage
from forms import LoginForm, RegisterForm, SkinAnalysisForm, ProductForm, ReviewForm, BlogPostForm, CheckoutForm, ChatForm
from face_analysis import face_analyzer

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
products_bp = Blueprint('products', __name__)
chat_bp = Blueprint('chat', __name__)
blog_bp = Blueprint('blog', __name__)

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Create upload directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        return filepath
    return None

# Main routes
@main_bp.route('/')
def index():
    # Get featured products
    featured_products = Product.query.filter_by(is_active=True).limit(8).all()
    
    # Get recent blog posts
    recent_posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_created.desc()).limit(3).all()
    
    return render_template('index.html', 
                         featured_products=featured_products,
                         recent_posts=recent_posts)

@main_bp.route('/skin-analysis', methods=['GET', 'POST'])
@login_required
def skin_analysis():
    form = SkinAnalysisForm()
    
    if form.validate_on_submit():
        # Save uploaded image
        image_file = form.skin_image.data
        image_path = save_uploaded_file(image_file)
        
        if image_path:
            # Perform skin analysis
            analysis_result = face_analyzer.analyze_skin(image_path)
            
            # Save analysis to database
            skin_analysis = SkinAnalysis(
                user_id=current_user.id,
                image_url=image_path,
                analysis_result=analysis_result,
                skin_type=analysis_result.get('skin_type', 'normal'),
                skin_concerns=analysis_result.get('concerns', []),
                recommended_routine=analysis_result.get('recommended_routine', {})
            )
            db.session.add(skin_analysis)
            db.session.commit()
            
            # Redirect to results page
            return redirect(url_for('main.analysis_results', analysis_id=skin_analysis.id))
        else:
            flash('Có lỗi khi tải ảnh lên. Vui lòng thử lại.', 'error')
    
    return render_template('skin_analysis.html', form=form)

@main_bp.route('/analysis-results/<int:analysis_id>')
@login_required
def analysis_results(analysis_id):
    analysis = SkinAnalysis.query.filter_by(id=analysis_id, user_id=current_user.id).first_or_404()
    
    # Get recommended products based on skin type
    recommended_products = Product.query.filter(
        (Product.skin_type == analysis.skin_type) | (Product.skin_type == 'all')
    ).filter_by(is_active=True).limit(6).all()
    
    return render_template('skin_analysis.html', 
                         analysis=analysis, 
                         recommended_products=recommended_products,
                         show_results=True)

@main_bp.route('/profile')
@login_required
def profile():
    user_analyses = SkinAnalysis.query.filter_by(user_id=current_user.id).order_by(SkinAnalysis.date_analyzed.desc()).all()
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_created.desc()).all()
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.date_created.desc()).all()
    
    return render_template('profile.html',
                         analyses=user_analyses,
                         orders=user_orders,
                         reviews=user_reviews)

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Chào mừng {user.full_name or user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Email hoặc mật khẩu không đúng.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email này đã được sử dụng.', 'error')
            return render_template('auth/register.html', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Tên đăng nhập này đã được sử dụng.', 'error')
            return render_template('auth/register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Đăng ký thành công! Chào mừng bạn đến với Beauty App.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đã đăng xuất thành công.', 'info')
    return redirect(url_for('main.index'))

# Product routes
@products_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category')
    skin_type = request.args.get('skin_type')
    search = request.args.get('search')
    
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if skin_type:
        query = query.filter((Product.skin_type == skin_type) | (Product.skin_type == 'all'))
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.description.contains(search))
    
    products = query.order_by(Product.date_added.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.all()
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         current_category=category_id,
                         current_skin_type=skin_type,
                         search_query=search)

@products_bp.route('/<int:product_id>')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.date_created.desc()).all()
    
    # Get related products
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    review_form = ReviewForm()
    
    return render_template('product_detail.html', 
                         product=product, 
                         reviews=reviews,
                         related_products=related_products,
                         review_form=review_form)

@products_bp.route('/<int:product_id>/add-to-cart', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add product to cart
    product_key = str(product_id)
    if product_key in session['cart']:
        session['cart'][product_key] += quantity
    else:
        session['cart'][product_key] = quantity
    
    session.modified = True
    flash(f'Đã thêm {product.name} vào giỏ hàng!', 'success')
    return redirect(url_for('products.detail', product_id=product_id))

@products_bp.route('/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Check if user already reviewed this product
        existing_review = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if existing_review:
            flash('Bạn đã đánh giá sản phẩm này rồi.', 'warning')
        else:
            review = Review(
                user_id=current_user.id,
                product_id=product_id,
                rating=form.rating.data,
                title=form.title.data,
                content=form.content.data
            )
            db.session.add(review)
            db.session.commit()
            flash('Cảm ơn bạn đã đánh giá sản phẩm!', 'success')
    
    return redirect(url_for('products.detail', product_id=product_id))

@main_bp.route('/cart')
def cart():
    cart_items = []
    total = 0
    
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                item_total = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total': item_total
                })
                total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Giỏ hàng của bạn đang trống.', 'warning')
        return redirect(url_for('main.cart'))
    
    form = CheckoutForm()
    
    # Pre-fill form with user data
    if request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.phone.data = current_user.phone
        form.address.data = current_user.address
    
    if form.validate_on_submit():
        # Calculate total
        total = 0
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                total += product.price * quantity
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=form.address.data,
            phone_number=form.phone.data,
            payment_method=form.payment_method.data
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(order_item)
        
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        flash('Đặt hàng thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.', 'success')
        return redirect(url_for('main.profile'))
    
    # Calculate cart total for display
    cart_total = 0
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                cart_total += product.price * quantity
    
    return render_template('checkout.html', form=form, total=cart_total)

# Chat routes
@chat_bp.route('/')
@login_required
def index():
    # Get user's chat history
    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.date_created.asc()).all()
    form = ChatForm()
    return render_template('chat.html', messages=messages, form=form)

@chat_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    form = ChatForm()
    if form.validate_on_submit():
        # Save user message
        user_message = ChatMessage(
            user_id=current_user.id,
            message=form.message.data,
            is_from_user=True,
            session_id=session.get('chat_session_id', str(uuid.uuid4()))
        )
        db.session.add(user_message)
        
        # Generate bot response (simplified)
        bot_response = generate_beauty_advice(form.message.data)
        
        bot_message = ChatMessage(
            user_id=current_user.id,
            message=bot_response,
            is_from_user=False,
            session_id=user_message.session_id
        )
        db.session.add(bot_message)
        db.session.commit()
        
        flash('Tin nhắn đã được gửi!', 'success')
    
    return redirect(url_for('chat.index'))

def generate_beauty_advice(message):
    """Generate simple beauty advice based on keywords"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['mụn', 'acne', 'trứng cá']):
        return """Để điều trị mụn hiệu quả:
        
1. Sử dụng sữa rửa mặt chứa salicylic acid
2. Thoa kem chống nắng hàng ngày
3. Không nặn mụn bằng tay
4. Sử dụng sản phẩm chứa benzoyl peroxide hoặc retinoid
5. Giữ gối và khăn mặt sạch sẽ

Bạn có thể tham khảo các sản phẩm trị mụn trong danh mục skincare của chúng tôi."""
    
    elif any(word in message_lower for word in ['khô', 'dưỡng ẩm', 'moisturizer']):
        return """Cho da khô, bạn nên:
        
1. Sử dụng sữa rửa mặt không chứa sulfate
2. Thoa toner không chứa alcohol
3. Dùng serum hyaluronic acid
4. Kem dưỡng ẩm với ceramide hoặc glycerin
5. Uống đủ nước và sử dụng máy tạo ẩm

Xem các sản phẩm dưỡng ẩm chuyên sâu tại cửa hàng của chúng tôi!"""
    
    elif any(word in message_lower for word in ['chống nắng', 'sunscreen', 'spf']):
        return """Kem chống nắng rất quan trọng:
        
1. Sử dụng SPF ít nhất 30 hàng ngày
2. Thoa lại mỗi 2 tiếng
3. Chọn loại broad-spectrum (chống cả UVA và UVB)
4. Không quên cổ, tai và bàn tay
5. Sử dụng cả khi ở trong nhà

Chúng tôi có nhiều loại kem chống nắng phù hợp với mọi loại da."""
    
    elif any(word in message_lower for word in ['makeup', 'trang điểm', 'son', 'phấn']):
        return """Lời khuyên về trang điểm:
        
1. Luôn tẩy trang trước khi ngủ
2. Sử dụng primer để makeup bền màu
3. Chọn foundation phù hợp với tông da
4. Blend kỹ để tránh vệt
5. Sử dụng setting spray để cố định

Khám phá bộ sưu tập makeup đa dạng của chúng tôi!"""
    
    else:
        return """Cảm ơn bạn đã liên hệ! 

Tôi là chuyên gia tư vấn làm đẹp của Beauty App. Tôi có thể giúp bạn:

• Tư vấn skincare phù hợp với loại da
• Gợi ý sản phẩm makeup
• Hướng dẫn cách sử dụng sản phẩm
• Giải đáp thắc mắc về làm đẹp

Hãy cho tôi biết bạn quan tâm đến vấn đề gì nhé!"""

# Blog routes
@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.date_created.desc()).paginate(
        page=page, per_page=6, error_out=False
    )
    return render_template('blog.html', posts=posts)

@blog_bp.route('/<int:post_id>')
def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    # Increment views
    post.views += 1
    db.session.commit()
    
    # Get comments
    comments = BlogComment.query.filter_by(post_id=post_id).order_by(BlogComment.date_created.desc()).all()
    
    # Get related posts
    related_posts = BlogPost.query.filter(
        BlogPost.id != post.id,
        BlogPost.is_published == True
    ).limit(3).all()
    
    return render_template('blog_post.html', 
                         post=post, 
                         comments=comments,
                         related_posts=related_posts)

@blog_bp.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = BlogPost.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if content:
        comment = BlogComment(
            post_id=post_id,
            user_id=current_user.id,
            content=content
        )
        db.session.add(comment)
        db.session.commit()
        flash('Bình luận của bạn đã được thêm!', 'success')
    
    return redirect(url_for('blog.post_detail', post_id=post_id))

@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            excerpt=form.excerpt.data,
            content=form.content.data,
            featured_image=form.featured_image.data,
            tags=form.tags.data,
            author_id=current_user.id,
            is_published=form.is_published.data
        )
        db.session.add(post)
        db.session.commit()
        
        flash('Bài viết đã được tạo thành công!', 'success')
        return redirect(url_for('blog.post_detail', post_id=post.id))
    
    return render_template('blog_post.html', form=form, is_create=True)
